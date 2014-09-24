# mewa-diag

This is a simple diagnostic utility written in Python. When started it scans the specified channel for devices and services their expose. The result is printed in the tree-like form.


##Synopsis

```python
Usage: python mewa-diag.py { -s <server_url> } <channel_name> <channel_password>  

       channel_name ::= string
               fully qualified channel name

       channel_password ::= string
               channel access password set by the channel owner

       server_url ::= string, URL
               if this option is missing the default URL is used: "ws://channels.followit24.com/ws"

```

**Example output of the mewa-diag script:**

```
Connected to channel 'anthill.example', discovering devices and their services...

PO-switch-16
  └─org.fi24.discovery
  └─org.fi24.switch
PO-light-15
  └─org.fi24.discovery
  └─org.fi24.light
PO-light-18
  └─org.fi24.discovery
  └─org.fi24.light
Portal35
  └─ERROR: this device failed to provide list of services

```



