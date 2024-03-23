# This program takes in your classes by reading the classes from schedule.csv and
# creates a .ics file called classes.ics that you can add you your calendar of choice.

# Get Calendar and Event objects from the ics library
from ics import Calendar, Event
from ics.alarm.base import BaseAlarm

# Get the csv library to parse the schedule
import csv

# Get the date stuff to traverse the days in the quarter
from dateutil import rrule
from datetime import datetime, timedelta
import pytz

tz = pytz.timezone('America/Los_Angeles')

# reads in unformatted csv data and makes a formatted csv file with the desired fields
def formatCSV():
  fields = []
  rows = []

  # read the fields and the rows that we care about into lists
  with open('schedule.csv', 'r') as csvfile:
    csvreader = csv.reader(csvfile)

    currLine = next(csvreader)
    while not currLine[0][0:5].isdigit():
      fields.append(currLine)
      currLine = next(csvreader)
    fields = ['SLN', 'Course', 'Type', 'Credits', 'Title', 'Days', 'Begin', 'End', 'Location', 'Instructor']

    while currLine[0][0:5].isdigit():
      if currLine[6] != '':
        rows.append(currLine[0:9])
      currLine = next(csvreader)

    for [index, row] in enumerate(rows):
      Time = row[6].split('-')
      Time[0] = int(Time[0].strip())
      Time[1] = int(Time[1].strip())
      if Time[0] < 830:
        Time[0] = Time[0] + 1200
        Time[1] = Time[1] + 1200
      if Time[0] < 1000:
        Time[0] = '0' + str(Time[0])
      if Time[1] < 1000:
        Time[1] = '0' + str(Time[1])
      row = row[0:6] + [Time[0]] + [Time[1]] + row[7:]
      rows[index] = row
  
  # write the formatted rows and fieldnames to formatted.csv
  with open('formatted.csv', 'w') as csvfile:
    csvwriter = csv.writer(csvfile)
    csvwriter.writerow(fields)
    csvwriter.writerows(rows)

# writes all the class events into the calendar
def writeToCal():
  fields = []
  rows = []

  # read the fields and the rows that we care about into lists
  with open('formatted.csv', 'r') as csvfile:
    csvreader = csv.reader(csvfile)

    fields = next(csvreader)

    for row in csvreader:
      rows.append(row)

  print("Go to this website: https://www.washington.edu/students/reg/calendar.html")
  print("and find your quarter's first and last day of instruction")
  # uncomment this after testing
  # start = input("Instruction begins (e.g. 'Mar 25, 2024'): ")
  # end = input("Last day of instruction (e.g. 'May 31, 2024'): ")
  start = 'Mar 25, 2024'
  end = 'May 31, 2024'

  months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
  startDate = datetime(year=int(start[-4:]), month=months.index(start[0:3])+1, day=int(start.split(" ")[1].split(",")[0])).astimezone(tz)
  endDate = datetime(year=int(end[-4:]), month=months.index(end[0:3])+1, day=int(end.split(" ")[1].split(",")[0])).astimezone(tz)

  for [index, row] in enumerate(rows):
    row[5] = row[5].replace('Th', '3')
    row[5] = row[5].replace('M', '0')
    row[5] = row[5].replace('T', '1')
    row[5] = row[5].replace('W', '2')
    row[5] = row[5].replace('F', '4')
    rows[index] = row
  
  c = Calendar()
  for dt in rrule.rrule(rrule.DAILY, dtstart=startDate, until=endDate):
    for row in rows:
      if str(dt.weekday()) in row[5]:
        e = Event()
        e.name = row[1]
        e.begin = str(dt.date()) + ' ' + row[6][:-2] + ':' + row[6][-2:] + ':00'
        e.end = str(dt.date()) + ' ' + row[7][:-2] + ':' + row[7][-2:] + ':00'
        alarmTime = datetime(year=dt.year, month=dt.month, day=dt.day, hour=int(row[6][:-2]), minute=int(row[6][-2:])).astimezone(tz) - timedelta(minutes=30)
        alarm = BaseAlarm
        alarm.trigger = alarmTime
        e.alarms = [alarm]
        e.location = row[8]
        print(e)
        c.events.add(e)
  
  with open('classes.ics', 'w') as file:
    file.writelines(c.serialize_iter())


formatCSV()
writeToCal()
