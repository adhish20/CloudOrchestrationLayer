def createXML(VMid, VMname, VM, path):
    xml = """
    <domain type='kvm' id='%s'>
      <name>%s</name>
      <memory unit='KiB'>%s</memory>
      <currentMemory unit='KiB'>1024</currentMemory>
      <vcpu placement='static'>%s</vcpu>
      <os>
        <type arch='x86_64' machine='pc-i440fx-utopic'>hvm</type>
        <boot dev='cdrom'/>
      </os>
      <features>
        <acpi/>
        <apic/>
        <pae/>
      </features>
      <clock offset='utc' />
      <on_poweroff>destroy</on_poweroff>
      <on_reboot>restart</on_reboot>
      <on_crash>restart</on_crash>
      <devices>
        <disk type='file' device='cdrom'>
          <driver name='qemu' type='raw'/>
          <source file='%s' />
          <backingStore/>
          <target dev='hda' bus='ide'/>
          <readonly/>
          <alias name='ide0-0-0'/>
          <address type='drive' controller='0' bus='0' target='0' unit='0'/>
        </disk>
      </devices>
    </domain>

    """% (VMid, VMname, VM['ram'], VM['cpu'], path)

    return xml