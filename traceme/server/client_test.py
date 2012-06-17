#!/usr/bin/python

import socket
import logging
import random

from tornado.options import define, options
from trace_record_pb2 import TraceRecord, DataPack

define("port", default=8888, help="The port number which the server listens to")
define("host", default="127.0.0.1", help="The host ip")

options.parse_command_line()

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Generate a random TraceRecord
dp = DataPack()
dp.recordType = DataPack.TRACE_RECORD
dp.traceRecord.cid = 'abcdefg12345'
dp.traceRecord.state = random.randint(0, 4)
dp.traceRecord.longitude = random.uniform(-180, 180)
dp.traceRecord.latitude = random.uniform(-180, 180)
dp.traceRecord.timestamp = random.randint(0,10000)
dp.traceRecord.altitude = random.uniform(-180, 180)
dp.traceRecord.speed = random.uniform(0, 180)


data = dp.SerializeToString()

try:
    sock.connect((options.host, options.port))
    logging.info('Sending data...')
    sock.sendall(data)
finally:
    sock.close()
    logging.info('Socket closed.')
