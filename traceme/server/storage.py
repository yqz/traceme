class StorageManager(object):
    '''An interface for storing various records'''
    def store_trace_record(self, record):
        raise NotImplementedError()

    def store_report_record(self, record):
        raise NotImplementedError()

import MySQLdb

class MySQLStorageManager(StorageManager):
    def __init__(self, mysql_host, username, password): 


    def store_trace_record(self, record):
        pass
