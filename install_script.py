#!/usr/bin/env python
import os
from optparse import OptionParser
import subprocess
import sys
import commands

class install_script():
	def __init__(self):
		self.prog_installed = []

	def obtaining_tar(self, prog, path):
		if (prog == 6):
			output1 = commands.getstatusoutput("uname")		
			if(output1[1].upper() == "LINUX"):			
				chk2 = self.checkfolder("salmon-1.1.0_linux_x86_64.tar.gz")
			else:
				chk2 = self.checkfolder("salmon-1.1.0_linux_x86_64.tar.gz")

			chk = self.checkfolder("oases")
			
			if(chk == False):
				os.system("git clone --recursive http://github.com/dzerbino/oases.git")
			else:
				print ("The path already contains a folder named oases. Please rename the folder or remove it from the path")
				sys.exit()
							
			chk1 = self.checkfolder("SEECER-0.1.3.tar.gz")
			if(chk1 == False):
				os.system("wget http://sb.cs.cmu.edu/seecer/downloads/SEECER-0.1.3.tar.gz")
				os.system("tar -zxvf SEECER-0.1.3.tar.gz")
			else:
				print ("The path already contains a folder named SEECER-0.1.3.tar.gz. Please rename it or remove it from the path")
			
			if(chk2 == False):
				if (output1[1].upper() == "LINUX"):
					os.system("wget https://github.com/COMBINE-lab/salmon/releases/download/v1.1.0/salmon-1.1.0_linux_x86_64.tar.gz")
					os.system("tar -zxvf salmon-1.1.0_linux_x86_64.tar.gz")
					self.prog_installed.append(path+"/salmon-1.1.0_linux_x86_64.tar.gz")
				#elif(output1[1].upper() == "DARWIN"):
				#	os.system("wget https://github.com/kingsfordgroup/sailfish/releases/download/v0.6.2/Sailfish-0.6.2-Mac_x86-64.tar.gz --no-check-certificate")
				#	os.system("tar -zxvf Sailfish-0.6.2-Mac_x86-64.tar.gz")
				#	self.prog_installed.append(path+"/Sailfish-0.6.2-Mac_x86-64")
				else:
					print "Unknown operating system"
					sys.exit()
								
			else:
				print ("The path already contains a folder named salmon-1.1.0_linux_x86_64.tar.gz. Please rename it or remove it from the path") 

			if(output1[1].upper() == "LINUX"):			
				chk2 = self.checkfolder("ORNA")
				if(chk2 == False):
					os.system("git clone https://github.com/SchulzLab/ORNA")
					self.prog_installed.append(path+"/ORNA")
				else:
					print ("The path already contains a folder named ORNA. Please rename it or remove it from the path")

			if(output1[1].upper() == "LINUX"):			
				chk2 = self.checkfolder("KREATION")
				if(chk2 == False):
					os.system("git clone https://github.com/SchulzLab/KREATION")
					self.prog_installed.append(path+"/KREATION")
				else:
					print ("The path already contains a folder named KREATION. Please rename it or remove it from the path")
		
		if(prog==3):
			output = commands.getstatusoutput("uname")		
			if(output[1].upper() == "LINUX"):			
				chk2 = self.checkfolder("salmon-1.1.0_linux_x86_64")
			else:
				chk2 = self.checkfolder("salmon-1.1.0_linux_x86_64")
							
			if(chk2 == False):
				if (output[1].upper() == "LINUX"):
					os.system("wget https://github.com/COMBINE-lab/salmon/releases/download/v1.1.0/salmon-1.1.0_linux_x86_64.tar.gz")
					os.system("tar -zxvf salmon-1.1.0_linux_x86_64.tar.gz")
					self.prog_installed.append(path+"/salmon-1.1.0_linux_x86_64")
				#elif(output[1].upper() == "DARWIN"):
				#	os.system("wget https://github.com/kingsfordgroup/sailfish/releases/download/v0.6.2/Sailfish-0.6.2-Mac_x86-64.tar.gz --no-check-certificate")
				#	os.system("tar -zxvf Sailfish-0.6.2-Mac_x86-64.tar.gz")
				#	self.prog_installed.append(path+"/Sailfish-0.6.2-Mac_x86-64")
				else:
					print "Unknown operating system"
					sys.exit()
			else:
				print ("The path already contains a folder named salmon-1.1.0_linux_x86_64.tar.gz. please rename it or remove it from the path") 
				
		
		if(prog==2):
			chk6 = self.checkfolder("oases")
			if(chk6 == False):
				os.system("git clone http://github.com/dzerbino/oases.git")
			else:
				print ("The path already contains a folder named oases. please rename the folder or remove it from the path")
				sys.exit()
			
		if(prog==1):
			chk4 = self.checkfolder("SEECER-0.1.3.tar.gz")
			if(chk4 == False):
				os.system("wget http://sb.cs.cmu.edu/seecer/downloads/SEECER-0.1.3.tar.gz")
				os.system("tar -zxvf SEECER-0.1.3.tar.gz")
				self.install_seecer(path)
			else:
				print ("The path already contains a folder named SEECER-0.1.3.tar.gz. please rename it or remove it from the path")
				sys.exit()
		
		if(prog==6):
			chk5 = self.checkfolder("velvet")
			if(chk5 == False):
				os.system("git clone http://github.com/dzerbino/velvet.git")
			else:
				print ("The path already contains a folder named velvet. please rename the folder or remove it from the path")
				sys.exit()
		if (prog == 4):
			output1 = commands.getstatusoutput("uname")		
			if(output1[1].upper() == "LINUX"):			
				chk2 = self.checkfolder("ORNA")
				if(chk2 == False):
					os.system("git clone https://github.com/SchulzLab/ORNA")
					self.prog_installed.append(path+"/ORNA")
				else:
					print ("The path already contains a folder named ORNA. Please rename it or remove it from the path")
			else:
				print("Unknown operating system")

		if (prog == 5):
			output1 = commands.getstatusoutput("uname")		
			if(output1[1].upper() == "LINUX"):			
				chk2 = self.checkfolder("KREATION")
				if(chk2 == False):
					os.system("git clone https://github.com/SchulzLab/KREATION")
					self.prog_installed.append(path+"/KREATION")
				else:
					print ("The path already contains a folder named KREATION. Please rename it or remove it from the path")
			else:
				print("Unknown operating system")

	
	def install_oases(self, path, cs):
		path2 = path + "/oases"
		os.chdir(path2)
		os.system("make "+cs)
		self.prog_installed.append(path2)
#		os.system("")

	def install_orna(self, path):
		path2 = path + "/ORNA"
		os.chdir(path2)
		os.system("bash install.sh")
		self.prog_installed.append(path2)
	
	def install_velvet(self,path, cs):
		path1 = path + "/velvet"
		os.chdir(path1) 
		print "------Velvet installation------"
		os.system("make "+cs)
		self.prog_installed.append(path1)
		
	def install_seecer(self, path):
		path3 = path + "/SEECER-0.1.3"
		temp_pa = path3 + "/jellyfish-1.1.11/"
		os.chdir(temp_pa)
		os.system("./configure")
		os.system("make")
		temp_pa1 = path3 + "/SEECER/"
		os.chdir(temp_pa1)
		os.system("./configure")
		os.system("make")
		self.prog_installed.append(temp_pa1)

	def getoptions(self):
		parser = OptionParser()
		parser.add_option("-f", "--folder", dest="foldername", help="destination folder")
		(options, args) = parser.parse_args()
		return options
	
	def checkfolder(self, program):
		var = os.path.exists(program)
		return var
	
	def checkinstall(self):
		for i in self.prog_installed:
			if "SEECER" in i:
				x1 = os.listdir(i+"/bin/")
				if(("seecer" in x1) and ("random_sub_N" in x1) and ("run_seecer.sh" in x1) and ("run_jellyfish.sh" in x1) and ("replace_ids" in x1)):
					print "SEECER installed successfully"
					s#elf.export_prog(i)
				else:
					print "SEECER was not installed properly. Please try again"				
			if "oases" in i:
				x2 = os.listdir(i)
				if ("oases" in x2):
					print "oases installed successfully"
					#self.export_prog(i)
				else:
					print "oases was not installed properly. please try again"
			
			if "velvet" in i:
				x3 = os.listdir(i)
				if(("velvetg" in x3) and ("velveth" in x3)):
					print "velvet installed successfully"
					#self.export_prog(i)
				else:
					print "velvet was not installed properly. Please try again"
					
			if ("salmon-1.1.0_linux_x86_64.tar.gz" in i):
				x4 = os.listdir(i+"/bin/")
				if("salmon" in x4):
					print "Sailfish installed successfully"
					#self.export_prog(i)
				else:
					print "Sailfish was not installed properly. Please try again"

########### MAIN PROGRAM ###########3

x = install_script()
y1 = x.getoptions()
print(y1)
if(y1.foldername != None):
	try:
		os.chdir(y1.foldername)
	except:
		uc = raw_input("folder "+ y1.foldername + " does not exists. Do you want to create one (y/n) : ")
		if(uc == "y"):
			os.system("mkdir " +y1.foldername)
			os.chdir(y1.foldername)
		else:
			sys.exit()

pwd = os.getcwd()

print ("Programs to install :")
print ("1.	SEECER")
print ("2.	OASES")
print ("3.	SALMON")
print ("4.	ORNA")
print ("5.	KREATION")
print ("6.	ALL")
print ("7.	QUIT")

x1 = raw_input("Enter the option number (if multiple options then separate it by comma): ")
y = x1.split(",")
acs = ""
vd = ""
flg = 0
cs = ""
a13 = ""
if("7" in y):
	print "Thank you. It was nice working for you"
	sys.exit()

if "6" in y:
	vc = raw_input("Execution of Oases requires velvet. Do you want to install velvet (y/n) : ")
	if(vc == "y"):
		ch = raw_input("Do you want to include additional compilation settings for velvet (refer to velvet manual for details) y/n : ")
		if(ch == "y"):
			print "Enter the additional compilation settings of velvet seperated by space :"
			a1 = raw_input()
			a11 = a1.split()
			for a2 in a11:
				a2 = a2.replace("'","")
				a2 = "\'" + a2 + "\'"
				a13 = a13 + " " + a2 
			cs = cs + a13
		flg = 1
	if(vc == "n"):
		vd = raw_input("Enter the location of velvet : ")
		cs = cs + " \'VELVET_DIR=" + vd +"\'"
	x.obtaining_tar(4, pwd)
	if (flg == 1):
		x.obtaining_tar(5, pwd)
		x.install_velvet(pwd, cs)	
	x.install_oases(pwd, cs)
	x.install_seecer(pwd)	

else:
	for i in y:
		if(int(i) == 2):
			vc = raw_input("Execution of Oases requires velvet. Do you want to install velvet (y/n) : ")
			if(vc == "y"):
				ch = raw_input("Do you want to include additional compilation settings for velvet (refer to velvet manual for details) y/n : ")
				if(ch == "y"):
					print "Enter the additional compilation settings of velvet seperated by space :"
					a1 = raw_input()
					a11 = a1.split()
					for a2 in a11:
						a2 = a2.replace("'","")
						a2 = "\'" + a2 + "\'"
						a13 = a13 + " " + a2 
					cs = cs + a13
				flg = 1
				cs = cs + "\'VELVET_DIR="+pwd+"/velvet\'"
			if(vc == "n"):
				vd = raw_input("Enter the location of velvet : ")
				if("\\" not in vd):
					cs = cs + " \'VELVET_DIR=" +pwd+"\\"+ vd +"\'"
				else:
					cs = cs + " \'VELVET_DIR=" + vd +"\'"
			x.obtaining_tar(2,pwd)
			if(flg == 1):			
				x.obtaining_tar(6,pwd)
				x.install_velvet(pwd, cs)
			x.install_oases(pwd, cs)
		if(int(i)==4):
			x.obtaining_tar(4,pwd)
			x.install_orna(pwd)
		else:
			x.obtaining_tar(int(i), pwd)

x.checkinstall()
