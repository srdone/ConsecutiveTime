#! /usr/bin/env Python3

import unittest
import person
import activity
from person import Person
from activity import Activity
from datetime import datetime, timedelta

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
		

class TestPerson(unittest.TestCase):
	
	def setUp(self):
		self.ID = 1234
		self.Name = 'Fred'
		self.activity_1 = Activity('UVU', 'Beginning Python', '00000'
										, '12/1/2013', '12/30/2013')
		self.activity_2 = Activity('UVU', 'Beginning Python', '00000'
										, '12/15/2013', '1/20/2014')
		self.activity_3 = Activity('UVU', 'Beginning Python', '00000'
										, '1/22/2014', '1/30/2014')
		self.activity_end_on_break = Activity('UVU', 'Beginning Python', '00000'
										, person.LAST_DAY_BEFORE_BREAK - timedelta(days = 60)
										, person.LAST_DAY_BEFORE_BREAK)
		self.activity_start_after_break = Activity('UVU', 'Beginning Python', '00000'
										, person.LAST_DAY_OF_BREAK + timedelta(days = 1)
										, person.LAST_DAY_OF_BREAK + timedelta(days = 60))
		self.activity_end_before_activity_1 = Activity('UVU', 'Beginning Python', '00000'
										, '12/1/2013', '12/10/2013')
	
	def test_person_creation(self):
		'Successful creation of person'
		self.person_test = Person(self.ID, self.Name)
		self.assertEqual(self.person_test.person_id, self.ID)
		self.assertEqual(self.person_test.person_name, self.Name)
	
	def test_add_activity(self):
		'Adding one activity sets consecutive dates to start and end of activity'
		self.person_test = Person(self.ID, self.Name)
		self.person_test.add_activity(self.activity_1)
		self.assertEqual(self.person_test.activities[0], self.activity_1)
		self.assertEqual(self.person_test.consecutive_start, self.activity_1.start_date)
		self.assertEqual(self.person_test.consecutive_end, self.activity_1.end_date)
	
	def test_two_concurrent_activities(self):
		'''Verifies that when we add a concurrent activity, the activity is sorted
		correctly, and the consecutive start matches the start date of the oldest course
		and the consecutive end matches the end date of the newest course'''
		person_test = Person(self.ID, self.Name)
		person_test.add_activity(self.activity_1)
		self.assertEqual(person_test.activities[0], self.activity_1)
		person_test.add_activity(self.activity_2)
		self.assertEqual(person_test.activities[1], self.activity_2)
		self.assertEqual(person_test.consecutive_start, self.activity_1.start_date)
		self.assertEqual(person_test.consecutive_end, self.activity_2.end_date)
	
	def test_two_non_concurrent_activities(self):
		'''Two non concurrent activities result in consecutive start and end equal to 
		start and end of second activity'''
		person_test = Person(self.ID, self.Name)
		person_test.add_activity(self.activity_1)
		person_test.add_activity(self.activity_3)
		self.assertEqual(person_test.consecutive_start, self.activity_3.start_date)
		self.assertEqual(person_test.consecutive_end, self.activity_3.end_date)
		
	def test_three_activities_one_break(self):
		'''When adding three activities with a break after second, consecutive dates are 
		equal to third activity start end dates'''
		person_test = Person(self.ID, self.Name)
		person_test.add_activity(self.activity_1)
		person_test.add_activity(self.activity_2)
		person_test.add_activity(self.activity_3)
		self.assertEqual(person_test.consecutive_start, self.activity_3.start_date)
		self.assertEqual(person_test.consecutive_end, self.activity_3.end_date)
		
	def test_break_over_break(self):
		'Courses counted as consecutive when landing on break unless ignore break false'
		person_test = Person(self.ID, self.Name)
		person_test.add_activity(self.activity_end_on_break)
		person_test.add_activity(self.activity_start_after_break)
		self.assertEqual(person_test.consecutive_start, self.activity_end_on_break.start_date)
		self.assertEqual(person_test.consecutive_end, self.activity_start_after_break.end_date)
		self.assertTrue(person_test.include())
		self.assertTrue(person_test.include(True))
		self.assertTrue(person_test.included_for_break())
		#Testing for include==False when we don't ignore break
		self.assertFalse(person_test.include(False))
		#now that we sent an include(False) call, the consecutive dates should be for last course
		self.assertEqual(person_test.consecutive_start, self.activity_start_after_break.start_date)
		self.assertEqual(person_test.consecutive_end, self.activity_start_after_break.end_date)
	
	def test_sort_1(self):
		'Sort orders each activity oldest to newest by start date'
		person_test = Person(self.ID, self.Name)
		person_test.add_activity(self.activity_1)
		person_test.add_activity(self.activity_3)
		person_test.add_activity(self.activity_2)
		self.assertEqual(person_test.activities[0], self.activity_1)
		self.assertEqual(person_test.activities[1], self.activity_2)
		self.assertEqual(person_test.activities[2], self.activity_3)
	
	def test_sort_2(self):
		'Sort orders activities with the same start, but different end dates with oldest end date activity last'
		person_test = Person(self.ID, self.Name)
		person_test.add_activity(self.activity_1)
		person_test.add_activity(self.activity_end_before_activity_1)
		self.assertEqual(person_test.activities[0], self.activity_end_before_activity_1)
		self.assertEqual(person_test.activities[1], self.activity_1)
	
	def test_modify_for_break(self):
		'modify_for_break modifies last day before break to last day of break'
		test_date = datetime.strptime('12/1/2013', '%m/%d/%Y').date()
		person_test = Person(self.ID, self.Name)
		self.assertEqual(person_test.modify_for_break(person.LAST_DAY_BEFORE_BREAK),person.LAST_DAY_OF_BREAK)
		self.assertEqual(person_test.modify_for_break(test_date),test_date)

if __name__ == '__main__':
	unittest.main()