#! usr/bin/env python3

#Provides methods for exporting list of persons and their activities where the
#person's include method indicates they should be included.

#imports
import csv
import tkinter
from tkinter import filedialog
import person
import activity

#Constants
SAVE_FILE_TEXT = 'Save the results as'
SAVE_FILE_TITLE = 'Save as'
HEADERS = ['Location', 'Person ID', 'Person Name', 'Activity Type', 'Activity ID'
			, 'Start Date', 'End Date', 'Included for Break']

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
        #write out their person_name and person_id with their activities.
        #One line per activity.
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