#!/usr/bin/env python3
# a simple analyzer for attendance reports of Microsoft 365 meetings.
# Version 0.0.1, initial release at 2020-07-05
# https://so-okada.github.io/noshow/
# Written by So.Okada, so.okada@gmail.com

import re
import csv
import glob
import pandas as pd
import datetime
from dateutil.parser import parse


def attendance_report(att_r):
    att = pd.read_csv(att_r, sep='\t')
    att = att.values.tolist()
    att = [[each[0], each[1], parse(each[2])] for each in att]
    return att


def delete_spaces(text):
    text = re.sub(r'\s+$', '', text)
    text = re.sub(r'^\s+', '', text)
    return text


def fullnames(enrolled):
    fullnames = pd.read_csv(enrolled)
    fullnames = fullnames.values.tolist()
    fullnames = [delete_spaces(name[0]) for name in fullnames]
    return fullnames


def noshow(fullnames_l, att_r, time_b, time_a, time_d, time_m, out_f):
    noshowlist = []
    if time_m == '':
        if time_b == '' and time_a == '' and time_d == '':
            noshowlist = noshow_atall(fullnames_l, att_r)
        elif time_b != '' and time_a == '' and time_d == '':
            noshowlist = noshow_before(fullnames_l, att_r, time_b)
        elif time_b == '' and time_a != '' and time_d == '':
            noshowlist = noshow_after(fullnames_l, att_r, time_a)
        elif time_b != '' and time_a != '' and time_d == '':
            noshowlist_b = noshow_before(fullnames_l, att_r, time_b)
            noshowlist_a = noshow_after(fullnames_l, att_r, time_a)
            noshowlist = list(set(noshowlist_b).intersection(noshowlist_a))
        elif time_b == '' and time_a == '' and time_d != '':
            noshowlist = noshow_during(fullnames_l, att_r, time_d)
        else:
            raise Exception('not valid options')
    elif time_b == '' and time_a == '' and time_d == '':
        noshowlist = noshow_min(fullnames_l, att_r, time_m)
    else:
        raise Exception('not valid options')

    if out_f != '':
        file_present = glob.glob(out_f)
        if file_present:
            text = out_f + ' already exists. Not writing output to a file.'
            print(text)
        else:
            csvf = csv.writer(open(out_f, 'w'))
            csvf.writerow(['Full name'])
            for entry in noshowlist:
                csvf.writerow([entry])
    return noshowlist


def noshow_atall(fullnames_l, att_r):
    noshowlist = []
    att_fullnames_l = [row[0] for row in att_r]
    for person in fullnames_l:
        if person not in att_fullnames_l:
            noshowlist.append(person)
    return noshowlist


def noshow_before(fullnames_l, att_r, time_b):
    noshowlist = []
    showlist = []
    tbefore = parse(time_b)
    for person in fullnames_l:
        for entry in att_r:
            if person == entry[0]:
                if entry[2] <= tbefore and 'Joined' in entry[1]:
                    showlist.append(person)
    for person in fullnames_l:
        if person not in showlist:
            noshowlist.append(person)
    return noshowlist


def noshow_after(fullnames_l, att_r, time_a):
    noshowlist = []
    tafter = parse(time_a)
    len_a = len(att_r)
    for person in fullnames_l:
        for num in range(len_a):
            entry = att_r[num]
            if person == entry[0]:
                if entry[2] < tafter and entry[1] == 'Left':
                    if person in noshow_atall(fullnames_l,
                                              att_r[num + 1:]):
                        noshowlist.append(person)
    return list(set(noshowlist)| \
          set(noshow_atall(fullnames_l,att_r)))


def noshow_during(fullnames_l, att_r, time_d):
    times = time_d.split('to')
    times = [delete_spaces(times[0]), delete_spaces(times[1])]
    noshowlist = []
    t_from = parse(times[0])
    t_to = parse(times[1])
    len_a = len(att_r)
    for person in fullnames_l:
        for num in range(len_a):
            entry = att_r[num]
            if person == entry[0]:
                if entry[2] < t_from and entry[1] == 'Left':
                    if person in noshow_before(fullnames_l,
                                               att_r[num + 1:],
                                               times[1]):
                        noshowlist.append(person)
    return list(set(noshowlist) | 
          set(noshow_atall(fullnames_l, att_r)))


def noshow_min(fullnames_l, att_r, time_m):
    times = time_m.split('until')
    times = [delete_spaces(times[0]), delete_spaces(times[1])]
    noshowlist = []
    timespent = {}
    t_min = parse(times[0]) - parse('00:00:00')
    t_until = parse(times[1])
    len_a = len(att_r)
    for person in fullnames_l:
        timespent[person] = datetime.timedelta(0)
        for num in range(len_a):
            entry = att_r[num]
            if person == entry[0]:
                if entry[2] <= t_until and 'Joined' in entry[1]:
                    if num < len_a - 2:
                        num += 1
                        next_entry = att_r[num]
                        if person == next_entry[0]:
                            timespent[person] = timespent[
                                person] + next_entry[2] - entry[2]
                        else:
                            timespent[person] = timespent[
                                person] + t_until - entry[2]
                    else:
                        timespent[person] = timespent[
                            person] + t_until - entry[2]
    for person in timespent:
        if timespent[person] < t_min:
            noshowlist.append(person)
    return (noshowlist)
