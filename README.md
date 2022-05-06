# http-hex-gen
  Generates a unique 8-digit HEX number without leet/hex speak
  
  It uses a simple HTTP server, and creates a 'database' in the same directory to prevent duplicates
 
 
  Update `PORT = xxxxx` settings to change listening port. 'Ctrl-C' to stop.

Usage (linux bash):
```
~> python3 hex_create.py &
~> curl localhost:12345
0x4DD97F42
~>fg
python3 hex_create.py
^C
KeyboardInterrupt — Exiting...
Bye!
~>_
```
