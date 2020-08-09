#!/usr/bin/env python3
# a simple analyzer for attendance reports of Microsoft 365 teams meetings.
# Version 0.0.1, initial release at 2020-07-05
# https://so-okada.github.io/noshow/
# Written by So.Okada, so.okada@gmail.com

import argparse
import noshow_commands as nosc
aparser = argparse.ArgumentParser(
    description="This is a simple analyzer for attendance"
    "reports of Microsoft 365 teams meetings."
    "This is not affiliated with Microsoft and has no guarantee.")

aparser.add_argument(
    "--enrolled",
    "-e",
    required=True,
    default='',
    help="This reads a file for a column list of full names."
    "The first line is ignored.")

aparser.add_argument("--att",
                     "-a",
                     required=True,
                     default='',
                     help="This reads an attendance report.")

aparser.add_argument("--out",
                     "-o",
                     default='',
                     help="This writes to a file with returned"
                     " full names in a column. An example: "
                     "--out noshow-2020-07-04.csv")

aparser.add_argument(
    "--before",
    "-bf",
    default='',
    help="This checks if somebody enrolled did not appear"
    "in an attendance report before a certain time. An example: "
    "--before '2020-07-04 10:00'")

aparser.add_argument(
    "--after",
    "-af",
    default='',
    help="This checks if somebody enrolled did not appear"
    " in an attendance report"
    " after a certain time. An example: "
    " --after '2020-07-04 10:40'")

aparser.add_argument(
    "--during",
    "-du",
    default='',
    help="This checks if somebody enrolled did not appear"
    " in an attendance report during sometime. An example:"
    " --during '2020-07-04 10:40 to 2020-07-04 10:55'")

aparser.add_argument(
    "--min",
    "-m",
    default='',
    help="This returns people enrolled who appeared less"
    " than a minimum time in an attendance report."
    " This needs to specify an ending time, because attendance"
    " reports have neither downloading nor ending time data."
    " An example:  --min '00:50:00 until 2020-07-04 11:30'")

args = aparser.parse_args()
enrolled = args.enrolled
att = args.att
time_before = args.before
time_after = args.after
time_during = args.during
time_min = args.min
out_f = args.out

fullnames = nosc.fullnames(enrolled)
att = nosc.attendance_report(att)

noshow = nosc.noshow(fullnames, att, time_before, time_after,
                     time_during, time_min, out_f)

print(noshow)
