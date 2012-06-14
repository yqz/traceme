protoc -I=traceme/server --python_out=traceme/server traceme/server/trace_record.proto
protoc -I=traceme/server --java_out=. traceme/server/trace_record.proto 
