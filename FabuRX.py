#!/usr/bin/python3
from rflib import *
from time import sleep
from sys import exit
import os
from datetime import datetime

def write(d, freq, mod, baud, capture, dev=0):
	home = os.path.expanduser('/home/fabularaza/Programme/DaikonTools-for-Yardstick-One/Records')
	yn = input("Write to file? Y/n\n")
	if yn.lower() == "n":
		print("Resuming...Press Enter to Stop")
	else:
		#path = input("Enter the name of the save file\n")
		f = open(home + datetime.now().strftime("%Y_%m_%d-%I_%M_%S_%p") + ".ys1", "w")
		freq = (freq/1000000)
		f.write('Freq: %s\n' % freq)
		f.write('Mod: %s\n' % mod)
		f.write('Baud: %s\n' % baud)
		if dev != 0:
			f.write('Deviation: %s\n' % dev)
		f.write('Repeat: \n')
		f.write('Preamble: \n')
		f.write('Data: %s\n' % capture)
		f.close()
	print("Resuming...Press Enter to Stop")

def main():
	
	freq = input("Enter freq to two decimals: (eg. 433.92) \n")
	freq = str(freq).replace('.', '')
	freq = int(freq)*10000
	
	mod = input("Number of modulation: 1. ASK/OOK / 2. FSK \n")
	mod = int(mod)
	
	baud = input("Enter baud rate: (default 10000)")
	if baud == '':
		baud = 10000
	else:
		baud = int(baud)
	
	os.system('clear')

#setup rfcat
	d = RfCat()
	#Helps if using RX after DaikonTX
	#d.strobeModeReturn(MARC_STATE_RX)
	d.setModeIDLE()
	d.setModeRX()
	d.setFreq(freq)
	d.setAmpMode(0)
	print('Set Freq: %s' % freq)
	if mod == 1:
		d.setMdmModulation(MOD_ASK_OOK)
		print("Set Mod: ASK")
		mod = "ASK"
	elif mod == 2:
		dev = input("Enter deviation: \n")
		dev = int(dev)
		d.setMdmModulation(MOD_2FSK)
		print("Set Mod: FSK")
		mod = "FSK"
		d.setMdmDeviatn(dev)
		print('Set Deviation: %s' % dev)
	else:
		Print("Unsupported modulation")
		d.setModeIDLE()
		sys.exit(1)
	d.setMdmDRate(baud)
	print('Set Baud: %s' % baud)
	d.setMdmChanSpc(24000)
	d.calculatePktChanBW()
	d.setMdmSyncMode(0)
	d.setChannel(0)
	d.setMaxPower()
	d.lowball(1)
	
	print("Press ENTER to stop")
	while not keystop():
		try:
			pkt, y = d.RFrecv()
			capture = pkt.hex()
			rssi = d.getRSSI()
			rssi = rssi.hex()
			rssi = int(rssi, 16)
			if rssi < 90:
				print('RSSI: %s\n' % rssi)
				print('Received: %s\n' % capture)
				if mod == "ASK":
					write(d, freq, mod, baud, capture)
				elif mod == "FSK":
					write(d, freq, mod, baud, capture, dev)
		except ChipconUsbTimeoutException:
			pass 	
	d.setModeIDLE()
	time.sleep(1)
	d = None

if __name__ == '__main__':
    main()
