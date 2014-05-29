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
        self.start_date = datetime.strptime(start_date, pattern).date()
        self.end_date = datetime.strptime(end_date, pattern).date()
        self.location = location
	
class TestActivity(unittest.TestCase):
	
	def setUp(self):
		self.pattern = '%m/%d/%Y'
		#Activity using a defined date pattern
		self.activity_pattern = Activity('UVU', 'Beginning Python', '00000'
										, '12/1/2013', '12/30/2013', self.pattern)
		#Activity using default date pattern
		self.activity_no_pattern = Activity ('UVU', 'Beginning Python', '00000'
										, '12/1/2013', '12/30/2013')
	
	def test_activity_pattern(self):
		'Test activity creation with a defined date pattern'
		self.assertEqual(self.activity_pattern.location, 'UVU')
		self.assertEqual(self.activity_pattern.activity_id, '00000')
		self.assertEqual(self.activity_pattern.start_date, datetime.strptime('12/1/2013', self.pattern).date())
		self.assertEqual(self.activity_pattern.end_date, datetime.strptime('12/30/2013', self.pattern).date())
	
	def test_activity_no_pattern(self):
		'Test activity creation using the default date pattern'
		self.assertEqual(self.activity_no_pattern.location, 'UVU')
		self.assertEqual(self.activity_no_pattern.activity_id, '00000')
		self.assertEqual(self.activity_no_pattern.start_date, datetime.strptime('12/1/2013', self.pattern).date())
		self.assertEqual(self.activity_no_pattern.end_date, datetime.strptime('12/30/2013', self.pattern).date())
	
	def tearDown(self):
		del self.activity_pattern
		del self.activity_no_pattern

if __name__ == '__main__':
	unittest.main()
	

