#!/usr/bin/python3
'''
Created on Jun 14, 2014

@author: lwoydziak
'''
from jsonconfigfile import Env
from providers import digitalOceanHosting
from dynamic_machine.machine import Machine
from dynamic_machine.inventory import Inventory
from pertinosdk import PertinoSdk, where

class NullPertino():
    def listOrgs(self):
        return ["none"]

    def listDevicesIn(self, *args):
        return ""
    
    def deleteFrom(self, *args):
        pass

def destroyNodes(aFilter):
    onDigitalOcean = digitalOceanHosting()
    name = Env().get("BaseHostName")
    machines = []
    
    try:
        username = Env().get("Pertino","username")
        password = Env().get("Pertino","password")
        pertinoSdk = PertinoSdk(username, password)
    except:
        pertinoSdk = NullPertino()
        
    organization = pertinoSdk.listOrgs()[0]
    
    # split
    for item in Inventory(onDigitalOcean).list(filteredByHost=name):
        if aFilter and not aFilter in item.name:
            continue
        pertinoHost = aFilter if aFilter else name
        machine = pertinoSdk.listDevicesIn(organization, where("hostName").contains(pertinoHost))
        pertinoSdk.deleteFrom(organization, machine)
        machine = Machine(onDigitalOcean, existing=True).name(item.name)
        machine.destroy()
        machines.append(machine)
    
    #join
    for machine in machines:
        machine.waitUntilDestroyed()    
    
def DestroyMachines(filter):
    initialJson = '{ \
        "DigitalOcean" : { \
            "Client ID"     : "None", \
            "API Key"       : "None", \
            "location"      : "None", \
            "image"         : "None", \
            "size"          : "None" \
        },\
        "Pertino" : { \
            "username"      : "None", \
            "password"      : "None"  \
        },\
        "BaseHostName": "None"\
    }'
    Env(initialJson, ".dynamicMachine", "DYNAMIC_MACHINE_CONFIG")
    destroyNodes(filter)



if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(description='Delete Machines.')
    parser.add_argument('--filter', help='The filename of the JSON file containing the list of commands.',required=False)
    args = parser.parse_args()
    try:
        DestroyMachines(args.filter)
        exit(0)
    except Exception as e:
        print (str(e))
        exit(1)
