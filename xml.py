def createXML(VMid, VMname, VM, path):
    xml = """
    <domain type='qemu' id='%s'>
        <name>%s</name>
        <memory unit='KiB'>%s</memory>
        <currentMemory unit='KiB'>524</currentMemory>
        <vcpu>%s</vcpu>
        <os>
            <type arch='x86_64' machine='pc-1.1'>hvm</type>
            <boot dev='cdrom'/>
            <boot dev='hd'/>
        </os>
        <features>
            <acpi/>
            <apic/>
            <pae/>
        </features>
        <clock offset='utc'/>
        <on_poweroff>destroy</on_poweroff>
        <on_reboot>restart</on_reboot>
        <on_crash>restart</on_crash>
        <devices>
            <emulator>/usr/bin/kvm-spice</emulator>
            <disk type='file' device='cdrom'>
                <driver name='qemu' type='raw'/>
                <target dev='hda' bus='ide'/>
            </disk>
            <disk type='file' device='cdrom'>
                <driver name='qemu' type='raw'/>
                <source file='%s'/>
                <target dev='hdc' bus='ide'/>
                <readonly/>
            </disk>
            <graphics type='spice' port='5900' autoport='yes' listen='127.0.0.1'>
                <listen type='address' address='127.0.0.1'/>
            </graphics>
        </devices>
    </domain>
    """% (VMid, VMname, str(int(VM['ram'])*1024), VM['cpu'], path)

    return xml