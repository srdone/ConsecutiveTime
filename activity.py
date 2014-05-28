#! usr/bin/env python3

#Activity object to hold the details of each activity.
#Used in person and referenced in consecutive.

#imports
from datetime import datetime, timedelta

class Activity(object):
    'Holds detail information on a activity'
    def __init__(self, location, activity_name, activity_id, start_date, end_date):
        self.activity_name = activity_name
        self.activity_id = activity_id
        self.start_date = datetime.strptime(start_date, '%m/%d/%Y').date()
        self.end_date = datetime.strptime(end_date, '%m/%d/%Y').date()
        self.location = location
        
if __name__ == '__main__':
	print(test_activity())

def test_activity():
	test_activity = Activity('UVU', 'OpenWest', '2014', '4/4/2014', '4/8/2014')
	if test_activity.location != 'UVU':
		return False
	elif test_activity.activity_name != 'OpenWest':
		return False
	elif test_activity.activity_id != '2014':
		return False
	elif test_activity.start_date != datetime.strptime('4/4/2014', '%m/%d/%Y').date():
		return False
	elif test_activity.start_date != datetime.strptime('4/8/2014', '%m/%d/%Y').date():
		return False
	else:
		return True