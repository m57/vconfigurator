# vConfigurator v 1.1

vConfigurator is a simple utility to auto configure vlans for when your in a trunking port.
I wrote this whilst on a pentest, in a DC, in about an hour, so you get what you pay for ;) 
Its not meant to be anything special, personally helped me a lot, you don't have to configure
all the vlans separatly and then change IP etc etc.

See below for basic usage...

### VLAN config file

Basically the VLAN configuration file is a csv file, an example has been provided. You can also comment out VLANS using "#". Essentially it is formatted like so:

`ip,netmask,gateway,vlan_id,vlan_name`

## Enable all configurations and automatically ARP scan and create VLAN folders with results inside.
```bash
# ./vconfigurator.py -i eth0 -c networks.csv -a --arp
```

## Enable all configurations
```bash
# ./vconfigurator.py -i eth0 -c -a
```

## Interactive mode (select all or one)
```bash
# ./vconfigurator.py -i eth0 -c 
```

> \x90
