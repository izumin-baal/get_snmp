#!/usr/bin/env python
# -*- coding: utf-8 -*-

import subprocess
import os
from os import path
from time import sleep

if os.getenv('SNMP_COMMUNITY'):
    COMMUNITY = os.getenv('SNMP_COMMUNITY')
else:
    COMMUNITY = ""

def getTargets():
    try:
        with open(path.dirname(path.abspath(__file__)) + '/' + 'hosts.txt') as f:
            targets = f.read().split("\n")
            if len(targets) <= 1:
                print('対象のホストが存在しません')
                exit()
            targets = list(filter(None, targets))
            return targets
    except FileNotFoundError:
        print('hosts.txtがありません')
        exit()

def getItems():
    try:
        with open(path.dirname(path.abspath(__file__)) + '/' + 'items.txt') as f:
            targets = f.read().split("\n")
            if len(targets) <= 1:
                print('対象のアイテムが存在しません')
                exit()
            targets = list(filter(None, targets))
            itemName = []
            itemOID = []
            for i in targets:
                item = i.split(",")
                itemName.append(item[0])
                itemOID.append(item[1])
            return itemName, itemOID
    except FileNotFoundError:
        print('items.txtがありません')
        exit()

def snmpGet(target,oids):
    results = []
    for i,oid in enumerate(oids):
        result = subprocess.run(['snmpwalk', '-t0.2', '-v2c', '-c', COMMUNITY, '-Ovq', target, oid],stdout=subprocess.PIPE,stderr=subprocess.DEVNULL)
        if result.stderr != None or result.stdout.decode('utf-8').rstrip() == "":
            results.append("None")
        else:
            results.append(result.stdout.decode('utf-8').rstrip())
    return results

def main():
    print('=== SNMP Monitor ===')
    print('COMMUNITY: '+COMMUNITY+"\n")
    targets = getTargets()
    itemNames,itemOIDs = getItems()
    for target in targets:
        print("== " + target + " ==")
        results = snmpGet(target,itemOIDs)
        for i,item in enumerate(itemNames):
            print(" " + item + ": " + results[i])
    print('\n')

if __name__ == '__main__':
    main()
