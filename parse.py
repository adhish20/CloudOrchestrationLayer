import json

def parseImages(imFile):
    images = {}
    ct = 1
    with open(imFile) as image_file:
        for line in image_file:
            images[ct] = {}
            images[ct]['username'] = line.split('@')[0]
            images[ct]['hostname'] = line.split('@')[1].split(':')[0]
            images[ct]['path'] = line.split('@')[1].split(':')[1].split('\n')[0]
            ct = ct + 1
    return images

def parseVMTypes(vmFile):
    with open(vmFile) as vm_file:
        vm_types = json.loads(vm_file.read())[u'types']
        VMTypes = {}
        for x in vm_types:
            VMTypes[x[u'tid']] = {}
            VMTypes[x[u'tid']]['cpu'] = x[u'cpu']
            VMTypes[x[u'tid']]['ram'] = x[u'ram']
            VMTypes[x[u'tid']]['disk'] = x[u'disk']

    return VMTypes

def parsePMs(pmFile):
    PMs = {}
    PMdetails = {}
    ct = 1
    with open(pmFile) as pm_file:
        for line in pm_file:
            PMs[ct] = {}
            PMs[ct]['username'] = line.split('@')[0]
            PMs[ct]['hostname'] = line.split('@')[1].split('\n')[0]
            PMs[ct]['pmid'] = ct
            PMdetails[ct] = {}
            PMdetails[ct]['pmid'] = ct
            PMdetails[ct]['capacity'] = {}
            PMdetails[ct]['capacity']['cpu'] = '4'
            PMdetails[ct]['capacity']['ram'] = '4096'
            PMdetails[ct]['capacity']['disk'] = '460'
            PMdetails[ct]['free'] = {}
            PMdetails[ct]['free']['cpu'] = '2'
            PMdetails[ct]['free']['ram'] = '2048'
            PMdetails[ct]['free']['disk'] = '157'
            PMdetails[ct]['vms'] = 0
            ct = ct + 1
    return (PMs, PMdetails)