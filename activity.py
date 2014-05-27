#Activity object to hold the details of each activity.
#Used in person and referenced in consecutive.

class Activity(object):
    'Holds detail information on a activity'
    def __init__(self, location, activity_name, activity_id, start_date, end_date):
        self.activity_name = activity_name
        self.activity_id = activity_id
        self.start_date = start_date
        self.end_date = end_date
        self.location = location