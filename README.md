# Application Info

This application "noshow" provides a simple analyzer for attendance reports of Microsoft 365 teams meetings. We use python3 scripts. This project is not affiliated with Microsoft. 

## Setup

* Install pandas and dateutil. 

```bash
% pip3 install pandas

% pip3 install python-dateutil
```

* Let noshow.py be executable.

```bash
% chmod +x noshow.py
```
* Put noshow.py and noshow_commands.py in the same directory.

## Usage

We need two csv files:

* a column list of full names of all enrolled people (the first line is ignored),

* an attendance report.

We assume that encodings of these csv files are utf-8. Samples are 
 in the tests directory. Please refer to
https://support.office.com/article/download-attendance-reports-in-teams-ae7cf170-530c-47d3-84c1-3aedac74d310 and https://microsoftteams.uservoice.com/forums/555103-public/suggestions/33989875-view-or-export-a-list-of-users-who-attended-a-meet for downloading attendance reports of your meetings.


```
usage: noshow.py [-h] --enrolled ENROLLED --att ATT
	                          [--out OUT] [--before BEFORE]
                              [--after AFTER] [--during DURING]
                              [--min MIN]

optional arguments:
  -h, --help        show this help message and exit
  --enrolled ENROLLED, -e ENROLLED
This reads a file for a column list of full names. The first line is ignored.
  --att ATT, -a ATT
This reads an attendance report.
  --out OUT, -o OUT
This writes an output to a file.
An example: --out noshow-2020-07-04.csv
  --before BEFORE, -bf BEFORE
This checks if somebody enrolled did not appear in an attendance report before a certain time.
An example: --before '2020-07-04 10:00'
  --after AFTER, -af AFTER
This checks if somebody enrolled did not appear in an attendance report after a certain time.
An example: --after '2020-07-04 10:40'
  --during DURING, -du DURING
This checks if somebody enrolled did not appear in an attendance report during sometime.
An example: --during '2020-07-04 10:40 to 2020-07-04 10:55'
  --min MIN, -m MIN
This returns people enrolled who appeared less than a minimum time in an attendance report. This needs to specify an ending time, because attendance reports have neither downloading nor ending time data.
An example: --min '00:50:00 until 2020-07-04 11:30'
```
## Sample outputs:


```bash
%./noshow.py -e tests/names.csv -a tests/att.csv 
['Rakot Bann']


% ./noshow.py -e tests/names.csv -a tests/att.csv --before '2020-07-04 9:54'
['Mouma Neew', 'Taraya da Silvane', 'Rakot Bann']


% ./noshow.py -e tests/names.csv -a tests/att.csv --after '2020-07-04 10:43'
['Rakot Bann', 'Bowge Syr', 'Makota Teeni']


% ./noshow.py -e tests/names.csv -a tests/att.csv --during '2020-07-04 10:35:12 to 2020-07-04 10:35:20'
['Rakot Bann', 'Sarako Thoma', 'Bowge Syr']


% ./noshow.py -e tests/names.csv -a tests/att.csv --min '00:50 until 2020-07-04 11:30'
['Bowge Syr', 'Rakot Bann']
```

## Version history

* 0.0.1

  * 2020-07-15, initial release.
 
## Author
So Okada, so.okada@gmail.com, https://so-okada.github.io/

## Contributing
Pull requests are welcome. For major changes, please open an 
issue first to discuss what you would like to change.

## License
[MIT](https://choosealicense.com/licenses/mit/)
