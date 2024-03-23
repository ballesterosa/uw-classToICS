# uw-classToICS
Python program that creates an ICS calendar file from a csv version of the UW class schedule table.
You can find the table at this link: https://sdb.admin.uw.edu/sisStudents/uwnetid/schedule.aspx
All you need to do for the setup is to copy the table into google sheets and then go to the file tab
and download the file as a csv file and place it in the same directory as the script.

Dependencies:
* python ics library:
`pip install ics`

* python timezone library:
`pip install pytz`