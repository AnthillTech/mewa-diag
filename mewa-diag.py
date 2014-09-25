'''
Created on Sep 18, 2014
@author: Piotr Orzechowski
@copyright: Anthill Technology
@version: 1.0
'''

import sys
import os
import getopt
from mewa.client import Connection
import time

'''Defs'''
URI_DISCOVERY             = "org.fi24.discovery"
URI_DISCOVERY_GETSERVICES = "org.fi24.discovery.GetServices"
URI_DISCOVERY_SERVICELIST = "org.fi24.discovery.ServiceList"
MY_DEVICE_NAME = "mewa-diag"
DEFAULT_SERVER_URL = "ws://channels.followit24.com/ws"

'''Global variables'''
g_Connection = Connection
g_ConnectFlag = ()
g_Devices = []
g_DevicesReadyFlag =0
g_CurIndentLevel = 0
g_ServiceListMsgFlag =0

def onConnected():
    global  g_ConnectFlag
    g_ConnectFlag = ('ok',)
    
def onError(reason):
    global  g_ConnectFlag
    g_ConnectFlag = ('error',reason)
    
def onDeviceJoinedChannel(timestamp, name):
    pass

def onDeviceLeftChannel(timestamp, name):
    pass

def onEvent(timestamp, device, eventId, params):
    pass
    
def onMessage(timestamp, device, msgId, params):
    global g_CurIndentLevel
    global g_ServiceListMsgFlag
    
    if msgId == URI_DISCOVERY_SERVICELIST:
        for srvURI in params:
            printIndented(g_CurIndentLevel, srvURI)
        g_ServiceListMsgFlag = 1

def onDevicesEvent(timestamp, devices):
    global g_Devices
    global g_DevicesReadyFlag
    for i in range(0,len(devices)):
        if devices[i] != 'mewa-diag': 
            g_Devices.append(devices[i])
    g_DevicesReadyFlag = 1        
    
def displayServices(devname):
    global g_Connection
    global g_CurIndentLevel
    global g_ServiceListMsg
    global g_ServiceListMsgFlag
    
    g_CurIndentLevel =1 
    g_ServiceListMsgFlag = 0
    g_Connection.sendMessage(devname, URI_DISCOVERY_GETSERVICES , '')
    wc = 0
    while g_ServiceListMsgFlag == 0 and wc <= 5:
        time.sleep(0.5)
        wc+=1
    if wc > 5:
        printIndented(g_CurIndentLevel, "ERROR: this device failed to provide list of services")

def printIndented(level,text):
    if level == 0:
        print text
    else:
        prefix='  '
        for i in range (0,level-1):
            prefix = prefix + '    '

        prefix = prefix + unichr(9492) + unichr(9472)
        print prefix+text 


def usage():
    print ("\nUsage: python %s { -s <server_url> } <channel_name> <channel_password>  \n" % (os.path.basename(sys.argv[0])))
    print ("       channel_name ::= string")
    print ("               fully qualified channel name\n")
    print ("       channel_password ::= string")
    print ("               channel access password set by the channel owner\n")
    print ("       server_url ::= string, URL")
    print ("               if this option is missing the default URL is used: \n")

def main():

    global g_Devices
    global g_DevicesReadyFlag
    global g_Connection
    global g_CurIndentLevel

    channel_name = ""
    channel_password = ""
    serverURL = DEFAULT_SERVER_URL

    
    try:
        opts,args = getopt.getopt(sys.argv[1:],"s:")
    except :
        usage()
        sys.exit(2)
 
    #read command line arguments
    if len(args) != 2:
        usage()
        sys.exit (2)
    else:
        channel_name = args[0]
        channel_password = args[1]
    
    #read command line options
    for opt,arg in opts:
        if opt == "-s":
            try:
                serverURL = arg
            except:
                usage ()
                sys.exit (2)

    g_Connection = Connection(serverURL)
    g_Connection.onConnected = onConnected
    g_Connection.onDevicesEvent = onDevicesEvent
    g_Connection.onError = onError
    g_Connection.onEvent = onEvent
    g_Connection.onMessage = onMessage
    
    g_Connection.connect(channel_name, MY_DEVICE_NAME, channel_password)
    
    while len(g_ConnectFlag) == 0:
        time.sleep(0.5)
    
    if g_ConnectFlag[0] == 'ok':
        print "\nConnected to channel '%s', discovering devices and their services...\n" % channel_name
    elif g_ConnectFlag[0] == 'error':
        print g_ConnectFlag
   
    g_Connection.getDevices()
    cnt=0
    while g_DevicesReadyFlag == 0:
        time.sleep(0.5)
        cnt+=1
        if cnt > 10:
            print "ERROR: getDevices() timed out. Exiting"
            exit(1)
    
    for i in range(0,len(g_Devices)):
        printIndented(0, "\n" + g_Devices[i])
        displayServices(g_Devices[i])

    print "\n"
    g_Connection.close()
    exit(0)

if __name__ == '__main__':
    main()
    
    
    
    
