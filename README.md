Dividends Analysis for a given Period
===

Sockets and the socket API are used to send messages across a network. These python files provide basic examples of how 
to use some of the socket module features.

Files
---
- guess_number_single_client.py
- guess_number_multi_client.py
- guess_number_multi_client_global.py
- guess_number_multi_client_events.py

How to use them
---
1. guess_number_single_client:
   Run the script. In any terminal write `telnet localhost 2000`. It will connect via socket with the program. Follow instructions.
   It's made with socket's bind, listen and accept. It also sends data to terminal. Only single client allowed to connect.
2. guess_number_multi_client:
   Run the script. In any terminal write `telnet localhost 2000`. It will connect via socket with the program. Follow instructions.
   It's made with socket's bind, listen and accept. It also sends data to terminal. Multiclient allowed, so you can 
connect with more than one terminal. It uses multithreading to do so.
3. guess_number_multi_client_global:
   Run the script. In any terminal write `telnet localhost 2000`. It will connect via socket with the program. Follow instructions.
   It's made with socket's bind, listen and accept. It also sends data to terminal. Multiclient allowed, so you can 
connect with more than one terminal. It uses multithreading to do so. It stops all running thread and reports winner on 
terminal/thread. It uses global variables to do so.
4. guess_number_multi_client_events.py:
   Pretty similar yo previous file, but it uses Event class of `threading` module for threads flags instead of global variables.
   


These examples are pretty simple but fully operational. You can try them to understand the basics of socket module and 
improve them according your needs.

