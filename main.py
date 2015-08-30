from flask import Flask, jsonify, request
import sys, parse, os, xml, libvirt
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
                    "List VM Types" : "http://server/vm/types",
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
                    images[int(VM['image_id'])]['username']+"@"+
                    images[int(VM['image_id'])]['hostname']+":"+
                    images[int(VM['image_id'])]['path']+" "+
                    PMs[PMNumber]['username']+"@"+
                    PMs[PMNumber]['hostname']+":/")

                path = '/home/phantom/Desktop/'+images[int(VM['image_id'])]['path'].split('/')[-1]
                XML = xml.createXML(VMid, VM['name'], vm_types[int(VM['instance_type'])], path)
                connection = libvirt.open("qemu:///system")
                connection.defineXML(XML)
                dom = connection.lookupByName(VM['name'])
                dom.create()
                VMid += 1
                return jsonify(PMdetails[PMNumber])
            else:
                return "No such Physical Machine exists"
        else:
            return "No such VM Type"
    else:
        return "No such image"

@app.route("/vm/types", methods=['GET'])
def VMTypes():
    return jsonify(vm_types)

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
        PMs, PMdetails = parse.parsePMs(sys.argv[1])
        images = parse.parseImages(sys.argv[2])
        vm_types = parse.parseVMTypes(sys.argv[3])
        app.run(debug = True)