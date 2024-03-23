# This program takes in your classes by reading the classes from schedule.csv and
# creates a .ics file called classes.ics that you can add you your calendar of choice.

# Get Calendar and Event objects from the ics library
from ics import Calendar, Event

# Get the csv library to parse the schedule
import csv

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
    print(fields)

    for row in csvreader:
      rows.append(row)
      print(row)

  print("Go to this website: https://www.washington.edu/students/reg/calendar.html")
  print("and find your quarter's first and last day of instruction")
  start = input("Instruction begins (e.g. 'Mar 25, 2024'): ")
  end = input("Last day of instruction (e.g. 'May 31, 2024'): ")
  print(start)
  print(end)

formatCSV()
writeToCal()
