#! usr/bin/env python3

#Activity object to hold the details of each activity.
#Used in person and referenced in consecutive.

#imports
import unittest
from datetime import datetime, timedelta

class Activity(object):
	'Holds detail information on a activity'
	
	def __init__(self, location, activity_name, activity_id, start_date, end_date, pattern='%m/%d/%Y'):
		self._start_date = None
		self._end_date = None
		
		self.activity_name = activity_name
		self.activity_id = activity_id
		self.pattern = pattern
		self.start_date = start_date
		self.end_date = end_date
		self.location = location
		
	@property
	def start_date(self):
		return self._start_date
	
	@start_date.setter
	def start_date(self, start_date):
		if type(start_date) == str:
			self._start_date = datetime.strptime(start_date, self.pattern).date()
		else:
			#assumes start date is a date. need error handling
			self._start_date = start_date
	
	@property
	def end_date(self):
		return self._end_date
	
	@end_date.setter
	def end_date(self, end_date):
		if type(end_date) == str:
			self._end_date = datetime.strptime(end_date, self.pattern).date()
		else:
			#assumes end date is a date. need error handling
			self._end_date = end_date
	

