#! usr/bin/env python3

#Activity object to hold the details of each activity.
#Used in person and referenced in consecutive.

#imports
import unittest
from datetime import datetime, timedelta

class Activity(object):
    'Holds detail information on a activity'
    def __init__(self, location, activity_name, activity_id, start_date, end_date, pattern='%m/%d/%Y'):
        self.activity_name = activity_name
        self.activity_id = activity_id
        if type(start_date) == str:
        	self.start_date = datetime.strptime(start_date, pattern).date()
        else:
        	#assumes start date is a date. need error handling
        	self.start_date = start_date
        if type(end_date) == str:
        	self.end_date = datetime.strptime(end_date, pattern).date()
        else:
        	#assumes end date is a date. need error handling
        	self.end_date = end_date
        self.location = location
	

