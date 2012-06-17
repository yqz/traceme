protoc -I=traceme/server --python_out=traceme/server traceme/server/trace_record.proto
protoc -I=traceme/server --java_out=android/traceme/src traceme/server/trace_record.proto 
