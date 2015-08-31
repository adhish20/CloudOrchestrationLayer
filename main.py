from flask import Flask, jsonify, request
import sys, parse, os, xml, libvirt
from pymongo import MongoClient
VMid = 32000
app = Flask(__name__)

@app.route('/')
def homepage():
    home = {}
    home["Cloud Orchestration Layer"] = [
        {
            "Author" : "Adhish Singla",
            "Project" : "Cloud Orchestration Layer",
            "URLs" : 
                {
                    "Create VM" : "http://server/vm/create?name=name&instance_type=type&image_id=id",
                    "Destroy VM" : "http://server/vm/destroy?vmid=vmid",
                    "VM Query" : "http://server/vm/query?vmid=vmid",
                    "List VM Types" : "http://server/vm/types",
                    "Images List" : "http://server/image/list",
                    "PMs List" : "http://server/pm/list",
                    "PM List VMs" : "http://server/pm/listvms?pmid=pmid",
                    "PM Query" : "http://server/pm/query?pmid=id"
                }
        }
    ]
    return jsonify(home)

@app.route("/vm/create", methods=['GET'])
def VMCreate():
    args = request.args
    VM = {}
    VM['name'] = args.get('name')
    VM['instance_type'] = args.get('instance_type')
    VM['image_id'] = args.get('image_id')

    if int(VM['image_id']) in images:
        if int(VM['instance_type']) in vm_types:
            PMNumber = Schedule(VM)
            if PMNumber > 0:
                os.system("sudo scp "+
                    images[int(VM['image_id'])]['path']+" "+
                    PMs[PMNumber]['username']+"@"+
                    PMs[PMNumber]['hostname']+":/home/"+PMs[PMNumber]['username'])

                path = '/usr/local/'+images[int(VM['image_id'])]['path'].split('/')[-1]
                global VMid
                VMid += 1
                XML = xml.createXML(VMid, VM['name'], vm_types[int(VM['instance_type'])], path)
                try:
                    connection = libvirt.open("qemu+ssh://"+PMs[PMNumber]['username']+"@"+PMs[PMNumber]['hostname']+"/system")
                    connection.defineXML(XML)
                    dom = connection.lookupByName(VM['name'])
                    dom.create()
                    VMs[VMid] = {}
                    VMs[VMid]['vmid'] = VMid
                    VMs[VMid]['name'] = VM['name']
                    VMs[VMid]['instance_type'] = VM['instance_type']
                    VMs[VMid]['pmid'] = PMNumber
                    PMdetails[PMNumber]['vms'] += 1
                    pmvms[PMNumber]['vmids'].append(VMid)
                    return jsonify({"vmid":VMid})
                except:
                    return jsonify({'status' : 0})
            else:
                return jsonify({'No such Physical Machine exists' : 0})
        else:
            return jsonify({'No such VM Type' : 0})
    else:
        return jsonify({'No such image' : 0})

@app.route("/vm/types", methods=['GET'])
def VMTypes():
    return jsonify(vm_types)

@app.route("/vm/query", methods=['GET'])
def VMQuery():
    args = request.args
    return jsonify(VMs[int(args.get('vmid'))])

@app.route("/vm/destroy", methods=['GET'])
def VMDestroy():
    args = request.args
    vmid = int(args.get('vmid'))
    try:
        connection = libvirt.open("qemu+ssh://"+PMs[VMs[vmid]['pmid']]['username']+"@"+PMs[VMs[vmid]['pmid']]['hostname']+"/system")
        dom = connection.lookupByName(VMs[vmid]['name'])
        dom.destroy()
        dom.undefine()
        return jsonify({'status' : 1})
    except:
        return jsonify({'status' : 0})

@app.route("/image/list", methods=['GET'])
def ImageList():
    image = {}
    image['images'] = []
    for x,y in imageNames.iteritems():
        image['images'].append(y)
    return jsonify(image)

@app.route("/pm/list", methods=['GET'])
def PMList():
    return jsonify(pmids)

@app.route("/pm/listvms", methods=['GET'])
def PMListVMs():
    args = request.args
    return jsonify(pmvms[int(args.get('pmid'))])

@app.route("/pm/query", methods=['GET'])
def PMQuery():
    args = request.args
    return jsonify(PMdetails[int(args.get('pmid'))])

@app.errorhandler(404)
def page_not_found(error):
    return 'This page does not exist', 404

def Schedule(VM):
    for x, y in PMs.iteritems():
        path = os.getcwd()
        path = path + "/data"
        os.system("ssh "+y['username']+"@"+y['hostname']+" free -m | grep 'Mem:' | awk '{print $4}' > data")
        with open(path) as f:
            ram = int(f.readline())
        os.system("ssh "+y['username']+"@"+y['hostname']+" nproc > data")
        with open(path) as f:
            cpu = int(f.readline())
        if vm_types[int(VM['instance_type'])]['cpu'] < cpu and vm_types[int(VM['instance_type'])]['ram'] < ram:
            return x
    return 0;

if __name__ == "__main__":
    if len(sys.argv) != 4:
        print "[ERROR] : Incorrect input parameters.\nUsage : $> python main.py pm_file image_file vm_types"
    else:
        client = MongoClient()
        PMs, PMdetails, pmids, pmvms = parse.parsePMs(sys.argv[1])
        images, imageNames = parse.parseImages(sys.argv[2])
        vm_types = parse.parseVMTypes(sys.argv[3])
        VMs = {}
        app.run(debug = True)