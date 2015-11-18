#!/usr/bin/python3
'''
Created on Dec 15, 2014

@author: lwoydziak
'''
from jsonconfigfile import Env
from providers import digitalOceanHosting

'''usage: 
list_locations.py                                                                                                 # clean up
'''



def ListLocations():
    initialJson = '{ \
        "DigitalOcean" : { \
            "Client ID"     : "None", \
            "API Key"       : "None", \
            "location"      : "None", \
            "image"         : "None", \
            "size"          : "None" \
        },\
        "BaseHostName": "None"\
    }'
    Env(initialJson, ".dynamicMachine", "DYNAMIC_MACHINE_CONFIG")
    onDigitalOcean = digitalOceanHosting()
    print("Available Targets:")
    for target in onDigitalOcean.list_locations():
        print (str(target))



if __name__ == '__main__':
    try:
        ListLocations()
        exit(0)
    except Exception as e:
        print (str(e))
        exit(1)