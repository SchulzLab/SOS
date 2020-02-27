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
			#Before obtaining tha tar file of the corresponding tool, we always check whether the folder exists in the path. If it exists then we throw an exception otherwise we download the tool
			#Checking and downloading oases			
			chk = self.checkfolder("oases")
			if(chk == False):
				os.system("git clone --recursive http://github.com/dzerbino/oases.git")
			else:
				print ("The path already contains a folder named oases. Please rename the folder or remove it from the path")
				sys.exit()
							
			#Checking and downloading SEECER. This is not the version mentioned in the manuscript of SEECER. This is the modified version which was used for the SOS manuscript. 
			chk1 = self.checkfolder("SEECER.tar.gz")
			if(chk1 == False):
				os.system("wget https://zenodo.org/record/3686150/files/SEECER.tar.gz?download=1")
				os.system("tar -zxvf SEECER.tar.gz")
			else:
				print ("The path already contains a folder named SEECER.tar.gz. Please rename it or remove it from the path")
			
			#Checking and downloading salmon
			chk2 = self.checkfolder("salmon-1.1.0_linux_x86_64.tar.gz")
			if(chk2 == False):
				#To get the latest version of salmon, please change the link in the next three lines
				os.system("wget https://github.com/COMBINE-lab/salmon/releases/download/v1.1.0/salmon-1.1.0_linux_x86_64.tar.gz") 
				os.system("tar -zxvf salmon-1.1.0_linux_x86_64.tar.gz")
				self.prog_installed.append(path+"/salmon-1.1.0_linux_x86_64.tar.gz")
			else:
				print ("The path already contains a folder named salmon-1.1.0_linux_x86_64.tar.gz. Please rename it or remove it from the path") 

			chk3 = self.checkfolder("ORNA")
			if(chk3 == False):
				os.system("git clone https://github.com/SchulzLab/ORNA")
				self.prog_installed.append(path+"/ORNA")
			else:
				print ("The path already contains a folder named ORNA. Please rename it or remove it from the path")

			chk4 = self.checkfolder("KREATION")
			if(chk4 == False):
				os.system("git clone https://github.com/SchulzLab/KREATION")
				self.prog_installed.append(path+"/KREATION")
			else:
				print ("The path already contains a folder named KREATION. Please rename it or remove it from the path")
		

		if(prog==1):
			chk6 = self.checkfolder("oases")
			if(chk6 == False):
				os.system("git clone http://github.com/dzerbino/oases.git")
			else:
				print ("The path already contains a folder named oases. please rename the folder or remove it from the path")
				sys.exit()
		
		if(prog==2):
			output = commands.getstatusoutput("uname")		
			chk2 = self.checkfolder("salmon-1.1.0_linux_x86_64")
			if(chk2 == False):
				#To get the latest version of salmon, please change the link in the next three lines
				os.system("wget https://github.com/COMBINE-lab/salmon/releases/download/v1.1.0/salmon-1.1.0_linux_x86_64.tar.gz")
				os.system("tar -zxvf salmon-1.1.0_linux_x86_64.tar.gz")
				self.prog_installed.append(path+"/salmon-1.1.0_linux_x86_64")
			else:
				print ("The path already contains a folder named salmon-1.1.0_linux_x86_64.tar.gz. please rename it or remove it from the path") 
				sys.exit()

		if (prog == 3):
			chk2 = self.checkfolder("ORNA")
			if(chk2 == False):
				os.system("git clone https://github.com/SchulzLab/ORNA")
				self.prog_installed.append(path+"/ORNA")
			else:
				print ("The path already contains a folder named ORNA. Please rename it or remove it from the path")
			
		if (prog == 4):
			s,t = commands.getstatusoutput("which cd-hit-est")
			if(s == 256):
				uc = raw_input("cd-hit is not found in the environment variables. Do you want to install (y/n) : ")
				if(uc == "y"):
					os.system("git clone https://github.com/weizhongli/cdhit")
					self.install_cdhit(path)
					os.chdir(path)
				else:
					print ("Please remember that cd-hit-est is required for the running of KREATION and must be in the environment variable $PATH")
			chk2 = self.checkfolder("KREATION")
			if(chk2 == False):
				os.system("git clone https://github.com/SchulzLab/KREATION")
				self.prog_installed.append(path+"/KREATION")
			else:
				print ("The path already contains a folder named KREATION. Please rename it or remove it from the path")
			
		if (prog == 5):
			chk1 = self.checkfolder("SEECER.tar.gz")
			if(chk1 == False):
				os.system("wget https://zenodo.org/record/3686150/files/SEECER.tar.gz?download=1")
				os.system("tar -zxvf SEECER.tar.gz")
				self.prog_installed.append(path+"/SEECER/bin/")
			else:
				print ("The path already contains a folder named SEECER.tar.gz. Please rename it or remove it from the path")

	
		if(prog==8):
			chk5 = self.checkfolder("velvet")
			if(chk5 == False):
				os.system("git clone http://github.com/dzerbino/velvet.git")
			else:
				print ("The path already contains a folder named velvet. please rename the folder or remove it from the path")
				sys.exit()


	def install_oases(self, path, cs):
		path2 = path + "/oases"
		os.chdir(path2)
		os.system("make "+cs)
		self.prog_installed.append(path2)

	def install_orna(self, path):
		path2 = path + "/ORNA"
		os.chdir(path2)
		os.system("bash install.sh")
		self.prog_installed.append(path2)
	
	def install_velvet(self,path, cs):
		path1 = path + "/velvet"
		os.chdir(path1) 
		print("------Velvet installation------")
		os.system("make "+cs)
		self.prog_installed.append(path1)

	def install_cdhit(self, path):
		path1 = path + "/cdhit"
		os.chdir(path1)
		print("------cd-hit-est installation------")
		os.system("make")

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
			if "oases" in i:
				x2 = os.listdir(i)
				if ("oases" in x2):
					print("oases installed successfully")
				else:
					print("oases was not installed properly. please try again")
			
			if "velvet" in i:
				x3 = os.listdir(i)
				if(("velvetg" in x3) and ("velveth" in x3)):
					print("velvet installed successfully")
				else:
					print("velvet was not installed properly. Please try again")
					
			if ("salmon-1.1.0_linux_x86_64.tar.gz" in i):
				x4 = os.listdir(i+"/bin/")
				if("salmon" in x4):
					print("Salmon installed successfully")
				else:
					print("Salmon was not installed properly. Please try again")

########### MAIN PROGRAM ###########

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
print ("1.	OASES")
print ("2.	SALMON")
print ("3.	ORNA")
print ("4.	KREATION")
print ("5.	SEECER")
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
	print("Thank you. It was nice working for you")
	sys.exit()

if "6" in y:
	#Obtaining and installing oases and velvet
	vc = raw_input("Execution of Oases requires velvet. Do you want to install velvet (y/n) : ")
	if(vc == "y"):
		ch = raw_input("Do you want to include additional compilation settings for velvet (refer to velvet manual for details) y/n : ")
		if(ch == "y"):
			print("Enter the additional compilation settings of velvet seperated by space (for instance - ’MAXKMERLENGTH=57’):")
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
	if (flg == 1):
		x.obtaining_tar(8, pwd)
		x.install_velvet(pwd, cs)	
	x.obtaining_tar(1, pwd)	
	x.install_oases(pwd, cs)
	#Obtaining salmon
	x.obtaining_tar(2, pwd)
	#Obtaining ORNA
	x.obtaining_tar(3, pwd)
	x.install_orna(pwd)
	#Obtaining KREATION
	x.obtaining_tar(4, pwd)
	#Obtaining SEECER
	x.obtaining_tar(5, pwd)
else:
	for i in y:
		if(int(i) == 1):
			vc = raw_input("Execution of Oases requires velvet. Do you want to install velvet (y/n) : ")
			if(vc == "y"):
				ch = raw_input("Do you want to include additional compilation settings for velvet (refer to velvet manual for details) y/n : ")
				if(ch == "y"):
					print("Enter the additional compilation settings of velvet seperated by space (for instance - ’MAXKMERLENGTH=57’):")
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
			x.obtaining_tar(1,pwd)
			if(flg == 1):			
				x.obtaining_tar(8,pwd)
				x.install_velvet(pwd, cs)
			x.install_oases(pwd, cs)
		elif(int(i)==3):
			x.obtaining_tar(3,pwd)
			x.install_orna(pwd)
		else:
			x.obtaining_tar(int(i), pwd)

x.checkinstall()
