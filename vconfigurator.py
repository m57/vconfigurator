#!/usr/bin/env python
#
# Wrote this in a DC when i had to test > 10 VLANS from a trunk port cos im lazy.
# Fairly simple to use and really helpful. All that is required is 8021q kernel 
# module to be installed.
#
# The CSV file should be in the order:
#
#	IP,Netmask,Gateway,VlanID,Comment
#
# ~ \x90
#

import os
import sys
import commands
import time

VERSION = "1.0"

def pc(c, str):
	if c == 1:
		print "\033[1;32m[+]\033[0m %s" % str
	elif c == 2:
		print "\033[1;31m[!]\033[0m %s" % str
	elif c == 3:
		print "\033[1;33m[?]\033[0m %s" % str
	else:
		print "wu w0t m8?!"

def init(iface, c):
	
	x = commands.getstatusoutput("ifconfig %s" % iface)[1]
	if "Device not found" in x:
		pc(2, x)
		exit(1)
	pc(3, "Interface: '%s'" % iface)

	pc(3,"Loading kernel module 8021q...")
	x = commands.getstatusoutput("modprobe 8021q")[1]
	if x:
		pc(2, "Failed to load kernel module 8021q. Install with local package manager.")
		exit(1)
	try:
		f = open(c, "r").close()
	except:
		pc(2, "Error opening file '%s'" % c)	
		exit(1)

def c_vlans(c,all):

	configs = []

	f = open(c, "r")

	for line in f.readlines():
		if len(line) > 1:
			configs.append(line.split(","))

	num_all_configs = len(configs)
	num_exit 	= len(configs)+1

	rng = range( 0, num_all_configs )
	rng.append(num_all_configs)
	rng.append(num_exit)

	ch = -1

	if all == 0:
	
		while (ch not in rng):
			pc(1, "-- Choose VLAN to apply --")
			for cnf in configs:
				print "\033[1;32m[%d]\033[0m\tVID: \033[1;32m'%s'\033[0m\tIP: '%s'\tNetmask: '%s'\tGateway: '%s'\tComment: '%s'" % (configs.index(cnf), cnf[3], cnf[0], cnf[1], cnf[2], cnf[4].strip())

			print "\033[1;32m[%d]\033[0m\tEnable all vlans" % num_all_configs
			print "\033[1;32m[%d]\033[0m\tExit" % num_exit

			try:
				ch = int(raw_input("\033[1;31m > \033[0m"))

			except:
				continue
		if ch == num_exit:
			exit(0)
		elif ch != num_all_configs:
			configs = [configs[ch]]
					

	for cnf in configs:
		
		e = commands.getstatusoutput("vconfig add %s %s" % (iface, cnf[3]))[1]
		
		if "exists" in e:
			pc(3, e)

		elif not "Added VLAN with VID ==" in e:
 			pc(2, e)
			continue
		time.sleep(0.5)

		e = commands.getstatusoutput("ifconfig %s.%s %s netmask %s" % (iface, cnf[3], cnf[0], cnf[1]) )[1]
		
		if e:
			pc(2, e)
			exit(1)
		
		time.sleep(0.5)

		commands.getstatusoutput("route add default gw %s %s.%s" % (cnf[2], iface, cnf[3]))[1]
		if "File exists" in e:
			pc(3, e)

		elif e:
			pc(2, e + " - Skipping but will still configure IP...")
			continue

		pc(1, "VID '%s' : '%s.%s ip:'%s' netmask:'%s' gateway:'%s' (Comment: '%s')" % (cnf[3], iface, cnf[3], cnf[0], cnf[1], cnf[2], cnf[4].strip()))

	if ch != num_all_configs and ch != -1:
		pc(3, "ifconfig %s.%s\n" % (iface, configs[0][3]) )
		os.system("ifconfig %s.%s" % (iface, configs[0][3]) )
	else:
		os.system("ifconfig")

	pc(3, "Routing table\n")
	os.system("route -n")
	

def rem_vlans(iface, all, id):
	
	if all:
		print commands.getstatusoutput("for i in $(ifconfig | grep \"eth0\.\" | awk '{print $1}'); do vconfig rem $i; done")[1]
	else:
		print commands.getstatusoutput("vconfig rem %s.%s" % (iface,id) )[1]
			
	pc(1, "Done")

def usage():
	
		pc(2, "Usage: %s -i [interface] -c [network_config_file.txt] [options]" % sys.argv[0])
		print "\nOptions:"
		print "\tBy default, this tool will offer an interactive menu, to enable all VLANS use -a"
		print ""
		print "\t-i [interface]\tInterface to configure VLAN ID."
		print "\t-c [csv_file]\tConfigurations file (CSV format). Example order (ip,netmask,gateway,vlan_id,vlan_name)"
		print "\t-a\t\tAdd and configure all VLANS in provided file."
		print "\t-d [vid]\tDelete specific VLAN ID."
		print "\t-r\t\tRemove all virtual interfaces. (vconfig rem)"
		print 
		print "An example configuration file (csv order: ip,netmask,gateway,vlanid,comment):\n"
		print "\t192.168.1.15,255.255.255.0,92.168.1.1,100,HOME_NETWORK"
		print "\t192.168.2.15,255.255.255.0,192.168.2.254,200,MGMT_NETWORK"
		print ""
		print "# vconfigurator.py -i eth0 -c networks.csv (interactive mode)"
		print "# vconfigurator.py -i eth0 -c networks.csv -a (auto-enable all vlans)"
		print ""

		exit(1)

if __name__ == "__main__":

	print ""
	print "                       ___ \033[1;32mVconfigurator v.%s\033[0m ___" % VERSION
	print ""
	print "   A simple utility to auto configure VLAN connectivity for pen testing. "
	print ""
	print "                \033[1;31m--\033[0m https://github.com/m57/vconfigurator \033[1;31m--\033[0m "
	print ""

	if "-i" not in sys.argv:
		usage()
	else:
		iface = sys.argv[sys.argv.index("-i")+1]

	if "-r" in sys.argv:
		rem_vlans(iface,1,id=-1)
		exit(1)

	if "-d" in sys.argv:
		rem_vlans(iface,0,sys.argv[sys.argv.index("-d")+1])
		exit(1)

	if "-c" not in sys.argv:
		usage()
	else:
		cfile = sys.argv[sys.argv.index("-c")+1]

	init(iface, cfile)

	if "-a" in sys.argv:
		c_vlans(cfile, 1)
	else:		
		c_vlans(cfile, 0)

