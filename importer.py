#! usr/bin/env python3

#Imports persons from list of consecutive activities

#imports
import csv
import tkinter
from tkinter import filedialog
import person
import activity

#Constants
PICK_FILE_TEXT = 'Select the raw data file'

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