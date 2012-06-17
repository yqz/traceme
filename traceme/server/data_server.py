#!/usr/bin/python

import logging
import functools

from tornado.options import define, options
from tornado.netutil import TCPServer
from tornado.ioloop import IOLoop
from trace_record_pb2 import DataPack

define("port", default=8888, help="The port number which the server listens to")
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
        dp = DataPack()
        try:
            dp.ParseFromString(data)
            if dp.IsInitialized():
                self._handle_dp(dp)
        finally:
            stream.close()

    def _handle_dp(self, dp):
        '''Handle a DataPacket.'''
        if dp.recordType == DataPack.TRACE_RECORD:
            self._handle_trace_record(dp.traceRecord)
        elif dp.recordType == DataPack.REPORT_RECORD:
            self._handle_report_record(dp.reportRecord)

    def _handle_trace_record(self, record):
        print record.cid

    def _handle_report_record(self, record):
        pass

if __name__ == '__main__':
    options.parse_command_line()

    server = DataServer()
    server.bind(options.port)
    server.start(options.number_of_process)
    IOLoop.instance().start()
