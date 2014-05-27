#! /usr/bin python3

#Script to find the people who are working consecutively more than a pre-determined amount of time
#Created 5/19/2014

#imports
import csv
import tkinter
from tkinter import filedialog
from datetime import datetime, timedelta

#Break days
#Used to identify a stretch of time that should not be counted as a break in working
LAST_DAY_BEFORE_BREAK = datetime.strptime('12/23/2013', '%m/%d/%Y').date()
LAST_DAY_OF_BREAK = datetime.strptime('1/6/2014', '%m/%d/%Y').date()

#Constants
PICK_FILE_TEXT = 'Select the raw data file'
SAVE_FILE_TEXT = 'Save the results as'
SAVE_FILE_TITLE = 'Save as'
HEADERS = ['Location', 'Person ID', 'Person Name', 'Activity Type', 'Activity ID', 'Start Date', 'End Date', 'Included for Break']
ALL_DONE_TEXT = 'Processed all rows'
STATUS_HEADER_TEXT = 'Processing Status'

#Threshold for number of days of consecutive work
#Change if we want to look at a different time threshold for inclusion in report.
MONTH_THRESHOLD = 4
DAYS_IN_MONTH = 30
DAY_THRESHOLD = DAYS_IN_MONTH * MONTH_THRESHOLD

def modify_for_break(date):
    '''If a date is equal to the last day before the break window we are ignoring,
    replace it with the last day of the break. This allows us to treat the ignored
    break as if it isn't there when we are looking at consecuive dates.'''
    if date == LAST_DAY_BEFORE_BREAK:
        return LAST_DAY_OF_BREAK
    else:
        return date

def read_person():
    'Reads in person and their activities from the external file'
    with open(filedialog.askopenfilename(defaultextension='.csv'
                                         , filetypes=[('CSV', '*.csv')]
                                         , title=PICK_FILE_TEXT), 'r', newline='') as base_file:
        reader = csv.DictReader(base_file)
        person = [] #Initialize the list of person
        for line in reader:
            #If we already have read a person in, check to see if there is already a person with the same person_id.
            #If there is, attach that person  to the 'a_person' variable. Otherwise, set a_person to empty
            if person:
                a_person = [a_person for a_person in person if a_person.person_id == line['person_id']]
            else:
                a_person = []
                
            #if we found an existing person , add the activity on this line to the person's activity list
            if a_person:
                a_person[0].add_activity(Activity(line['Location'], line['Activity Type']
                                            , line['Activity ID']
                                            , datetime.strptime(line['Start Date'], '%m/%d/%Y').date()
                                            , datetime.strptime(line['End Date'], '%m/%d/%Y').date()))

            #If there wasn't an existing person, create a new instance and add the activity on this line
            else:
                new_person = Person(line['Person ID'], line['Person Name'])
                new_person.add_activity(Activity(line['Location'], line['Activity Type']
                                            , line['Activity ID']
                                            , datetime.strptime(line['Start Date'], '%m/%d/%Y').date()
                                            , datetime.strptime(line['End Date'], '%m/%d/%Y').date()))
                #Append the new person to the person list
                person.append(new_person)
        return person

def write_person(person):
    'Writes the person who are marked to be included to a new .csv file'
    with open(filedialog.asksaveasfileperson_name(defaultextension='.csv'
                                           , filetypes=[('CSV', '*.csv')]
                                           , initialfile='Processed.csv'
                                           , title=SAVE_FILE_TEXT)
              , 'w', newline='') as save_file:
        writer = csv.writer(save_file)
        writer.writerow(HEADERS)

        #Iterate through each person. If they should be included in the output,
        #write out their person_name and person_id with their activities. One line per activity.
        for a_person in person:
            #Make only write person who should be included
            if a_person.include():
                #Write out the activity information with person identifiers
                for activity in a_person.activities:
                    row = [activity.location
                           , a_person.person_id
                           , a_person.person_name
                           , activity.activity_name
                           , activity.activity_id
                           , activity.start_date
                           , activity.end_date
                           , a_person.included_for_break()]
                    writer.writerow(row)

if __person_name__ == '__main__':
    person = read_person()
    write_person(person)
    print(ALL_DONE_TEXT)
