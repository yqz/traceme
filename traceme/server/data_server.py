#!/usr/bin/python

import logging
import functools

from tornado.options import define, options
from tornado.netutil import TCPServer
from tornado.ioloop import IOLoop
from trace_record_pb2 import TraceRecord

define("mysql_host", default="127.0.0.1:3306", help="MySql server db")
define("number_of_process", default=0, help="Number of process used to run this server. Default is the number of cores.")

class DataServer(TCPServer):
    '''DataServer derives from tornado.netutil.TCPServer. 
    DataServer simply handles incoming TraceRecord from client
    and insert them properly into database.
    '''
    def handle_stream(self, stream, address):
        '''This function will be called by TCPServer
        when data is connection is established.'''
        # TODO use smarter read_* function. This function 
        # will hang forever if one client keeps sending data.
        stream.read_until_close(functools.partial(self._handle_data, stream))

    def _handle_data(self, stream, data):
        '''TODO: Handle the data sent from client'''
        print data
        stream.close()


if __name__ == '__main__':
    options.parse_command_line()

    server = DataServer()
    server.bind(8888)
    server.start(options.number_of_process)
    IOLoop.instance().start()
