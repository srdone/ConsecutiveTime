#! usr/bin/env python3

#Person object to hold the activities and identification information for each person.

#imports
from datetime import datetime, timedelta
import activity
import unittest

#Break days
#Used to identify a stretch of time that should not be counted as a break in working
LAST_DAY_BEFORE_BREAK = datetime.strptime('12/23/2013', '%m/%d/%Y').date()
LAST_DAY_OF_BREAK = datetime.strptime('1/6/2014', '%m/%d/%Y').date()

#Threshold for number of days of consecutive work
#Change if we want to look at a different time threshold for inclusion in report.
MONTH_THRESHOLD = 4
DAYS_IN_MONTH = 30
DAY_THRESHOLD = DAYS_IN_MONTH * MONTH_THRESHOLD

class Person(object):
	'Holds the list of activities and identifier information for a person'
	def __init__(self, person_id, person_name):
		self.person_id = person_id
		self.person_name = person_name
		self.activities = []
		self.consecutive_start = ''
		self.consecutive_end = ''

	def include(self, ignore_break=True):
		'''Returns true if person has worked consecutively for at least a predetermined time.
		ignore_break determines whether we treat the ignored break as a break or not.
		True is default and treats the ignored break as if it weren't there'''
		self.resort_activities(ignore_break)
		if (self.consecutive_end - self.consecutive_start) >= timedelta(days = (DAYS_IN_MONTH * MONTH_THRESHOLD - 1)):
			return True
		else:
			return False

	def included_for_break(self):
		'Return true if the instructor was only included because we ignored the holiday break'
		#Passing False to self.include indicates whether the instructor would be
		#included if we did not treat the holiday break as if it was not there
		#A person  who is included while ignoring the break,
		#but is not included otherwise is someone who was only included because we ignored the break
		if self.include(True) and not self.include(False):
			return True
		else:
			return False

	def add_activity(self, activity):
		'Adds a activity to the activities list'
		self.activities.append(activity)
		self.resort_activities(self)

	def resort_activities(self, ignore_break=True):
		'Sorts the instructor activities by start date/end date'
		self.activities.sort(key=lambda activity:
						  (activity.start_date, (self.modify_for_break(activity.end_date) if ignore_break else activity.end_date)))
		self.consecutive_start = self.activities[0].start_date
		self.reset_consecutive_dates(ignore_break)

	def reset_consecutive_dates(self, ignore_break=True):
		'''Resets the start and end of the consecutive amount for the instructor.
		This should is called by resort_activities every time a activity is added'''
		if len(self.activities) == 1:
			self.consecutive_start = self.activities[0].start_date
			self.consecutive_end = self.activities[0].end_date
		
		for index, activity in enumerate(self.activities):
			
			#Make sure we don't go out of bounds
			if index + 1 >= len(self.activities):
				break
			
			#Set dates to examine, modifying the end dates as needed if we are ignoring the holiday break
			current_end_date = (self.modify_for_break(activity.end_date) if ignore_break else activity.end_date)
			next_end_date = (self.modify_for_break(self.activities[index + 1].end_date) if ignore_break else self.activities[index + 1].end_date)
			next_start_date = self.activities[index + 1].start_date
	
			#Determine if there is a break.
			#Reset the consecutive start if there is.
			#If not, set the consecutive end out to the end date of the next activity
			if (current_end_date + timedelta(days=1)) >= next_start_date:
				self.consecutive_end = next_end_date
			else:
				self.consecutive_start = next_start_date
			
	def modify_for_break(self, date):
		'''If a date is equal to the last day before the break window we are ignoring,
		replace it with the last day of the break. This allows us to treat the ignored
		break as if it isn't there when we are looking at consecuive dates.'''
		if date == LAST_DAY_BEFORE_BREAK:
			return LAST_DAY_OF_BREAK
		else:
			return date

class TestPerson(unittest.TestCase):
	
	def setUp(self):
		self.ID = 1234
		self.Name = 'Fred'
		self.person_test = Person(self.ID, self.Name)
		self.activity_1 = activity.Activity('UVU', 'Beginning Python', '00000'
										, '12/1/2013', '12/30/2013')
		self.activity_2 = activity.Activity('UVU', 'Beginning Python', '00000'
										, '12/15/2013', '1/20/2014')
	
	def test_person_creation(self):
		self.assertEqual(self.person_test.person_id, self.ID)
		self.assertEqual(self.person_test.person_name, self.Name)
	
	def test_add_activity(self):
		self.person_test.add_activity(self.activity_1)
		self.assertEqual(self.person_test.activities[0], self.activity_1)
		self.assertEqual(self.person_test.consecutive_start, self.activity_1.start_date)
		self.assertEqual(self.person_test.consecutive_end, self.activity_1.end_date)
	
	def test_two_concurrent_activities(self):
		'''Verifies that when we add a concurrent activity, the activity is sorted
		correctly, and the consecutive start matches the start date of the oldest course
		and the consecutive end matches the end date of the newest course'''
		self.person_test.add_activity(self.activity_1)
		self.assertEqual(self.person_test.activities[0], self.activity_1)
		self.person_test.add_activity(self.activity_2)
		self.assertEqual(self.person_test.activities[1], self.activity_2)
		self.assertEqual(self.person_test.consecutive_start, self.activity_1.start_date)
		self.assertEqual(self.person_test.consecutive_end, self.activity_2.end_date)
	
	#def test_two_non_concurrent_activities
	#def test_three_activities_one_break
	#def test_break_over_break_ignore
	#def test_break_over_break_not_ignore
	#Need to test each function, but also interaction between different functions

if __name__ == '__main__':
	unittest.main()