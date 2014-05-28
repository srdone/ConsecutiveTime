#! /usr/bin/env python3

#Script to find the people who are working consecutively more than a pre-determined amount of time
#Created 5/19/2014

#Constants
ALL_DONE_TEXT = 'Processed all rows'

if __name__ == '__main__':
    person = read_person()
    write_person(person)
    print(ALL_DONE_TEXT)
