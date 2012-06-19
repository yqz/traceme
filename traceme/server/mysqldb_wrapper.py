import MySQLdb
import functools
import logging
from _mysql_exceptions import OperationalError

class MySQLConnectionError(Exception):
    def __init__(self, msg = None):
        Exception.__init__(self, msg)

class MySQLConnection(object):
    ''' This is a simple wrapper around MySQLdb package and providing
    more retry functions for query'''
    def __init__(self, *pargs, **kargs):
        self._con = MySQLdb.connect(*pargs, **kargs)
        self._con.autocommit(True)

    def _run_query(self, query, params):
        ''' Run a query with params. Return the result of cursor.execute
            and the cursor it self as a pair.
            This function will try to reconnect if the first try failed with
            OperationalError. 
            Remember to close the cursor in user code.
        '''
        if self._con is None:
            raise MySQLConnectionError('Conncection is already closed')

        try:
            cursor = self._con.cursor()
            return cursor, cursor.execute(query, params)
        except OperationalError:
            # Query again after reconnection
            cursor.close()
            # Try reconnect if connection was lost
            self._reconnect()
            # Try query again.
            cursor = self._con.cursor()
            return cursor, cursor.execute(query, params)

    def query(self, query, params):
        '''Run a query and return the number of affected/returned rows'''
        cursor, result = self._run_query(query, params)
        # Just close the cursor
        cursor.close()
        return result 

    def query_with_results(self, query, params, n=None):
        '''Run a query and return the results. usually for select statements'''
        cursor, result = self._run_query(query, params)
        try:
            if n is not None:
                return cursor.fetchmany(n)
            else:
                return cursor.fetchall()
        finally:
            cursor.close()

    def _reconnect(self):
        ''' reconnect to mysql'''
        # ping function will try to reconnect to server
        # if possible, otherwise exception will be thrown
        try:
            self._con.ping(True)
        except:
            raise MySQLConnectionError("Can't connect to server!")

    def close(self):
        ''' close db connection'''
        try:
            self._con.close()
            self._con = None
        except:
            pass

    def __del__(self):
        self.close()
        
