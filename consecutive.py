#! /usr/bin/env python3

#Script to find the people who are working consecutively more than a pre-determined amount of time
#Created 5/19/2014

#imports
import importer
import exporter

#Constants
ALL_DONE_TEXT = 'Processed all rows'

if __name__ == '__main__':
    person = importer.read_person()
    exporter.write_person(person)
    print(ALL_DONE_TEXT)
