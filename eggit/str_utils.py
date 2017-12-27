class DTFormat(object):
    date_format = None
    datetime_format = None

    def __init__(self, date_format='%Y-%m-%d', datetime_format='%Y-%m-%d %H:%M:%S'):
        self.date_format = date_format
        self.datetime_format = datetime_format
