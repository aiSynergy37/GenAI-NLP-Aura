"""
Real-time Log Tail + Alert (Very Common)
Simulate tail -f behavior on a growing log file.
Task: Write a script that:

Monitors server.log
Every time a new line appears containing "ERROR" or "CRITICAL"
Prints: [ALERT] {timestamp} {message}
If more than 5 errors in 60 seconds → print "!!! HIGH ERROR RATE DETECTED !!!"
"""