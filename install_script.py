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
			os.chdir(path)
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
				print("-----salmon installation-------")
				os.system("wget https://github.com/COMBINE-lab/salmon/releases/download/v1.1.0/salmon-1.1.0_linux_x86_64.tar.gz >"+path+"/LogFiles/salmon.txt 2> "+path+"/LogFiles/salmonError.txt") 
				os.system("tar -zxvf salmon-1.1.0_linux_x86_64.tar.gz >"+path+"/LogFiles/salmon.txt 2> "+path+"/LogFiles/salmonError.txt")
				self.prog_installed.append(path+"/salmon-1.1.0_linux_x86_64.tar.gz")
			else:
				print ("The path already contains a folder named salmon-1.1.0_linux_x86_64.tar.gz. Please rename it or remove it from the path")
				sys.exit() 

			chk3 = self.checkfolder("ORNA")
			if(chk3 == False):
				os.system("git clone https://github.com/SchulzLab/ORNA")
				self.prog_installed.append(path+"/ORNA")
			else:
				print ("The path already contains a folder named ORNA. Please rename it or remove it from the path")

			chk4 = self.checkfolder("KREATION")
			if(chk4 == False):
				print("-----KREATION installation-------")
				os.system("git clone https://github.com/SchulzLab/KREATION >"+path+"/LogFiles/KREATION.txt 2> "+path+"/LogFiles/KreationError.txt")
				self.prog_installed.append(path+"/KREATION")
			else:
				print ("The path already contains a folder named KREATION. Please rename it or remove it from the path")
		

		if(prog==1):
			os.chdir(path)
			chk6 = self.checkfolder("oases")
			if(chk6 == False):
				os.system("git clone http://github.com/dzerbino/oases.git >"+path+"/LogFiles/Oases.txt 2> "+path+"/LogFiles/OasesError.txt")
			else:
				print ("The path already contains a folder named oases. please rename the folder or remove it from the path")
				sys.exit()
		
		if(prog==2):
			os.chdir(path)
			output = commands.getstatusoutput("uname")		
			chk2 = self.checkfolder("salmon-1.1.0_linux_x86_64")
			if(chk2 == False):
				print("-----salmon installation-------")
				os.system("wget https://github.com/COMBINE-lab/salmon/releases/download/v1.1.0/salmon-1.1.0_linux_x86_64.tar.gz >"+path+"/LogFiles/salmon.txt 2> "+path+"/LogFiles/salmonError.txt") 
				os.system("tar -zxvf salmon-1.1.0_linux_x86_64.tar.gz >"+path+"/LogFiles/salmon.txt 2> "+path+"/LogFiles/salmonError.txt")
				self.prog_installed.append(path+"/salmon-1.1.0_linux_x86_64.tar.gz")
				chksalmon=self.checkfolder(path+"/salmon-latest_linux_x86_64/bin/salmon")
				if(chksalmon==False):
					print("Salmon did not install correctly. Please try again")
					sys.exit()
				else:
					print("Salmon installed successfully")
			
			else:
				print ("The path already contains a folder named salmon-1.1.0_linux_x86_64.tar.gz. please rename it or remove it from the path") 
				sys.exit()

		if (prog == 3):
			os.chdir(path)
			chk2 = self.checkfolder("ORNA")
			if(chk2 == False):
				os.system("git clone https://github.com/SchulzLab/ORNA >"+path+"/LogFiles/ORNA.txt 2> "+path+"/LogFiles/ORNAError.txt")
				self.prog_installed.append(path+"/ORNA")
			else:
				print ("The path already contains a folder named ORNA. Please rename it or remove it from the path")
			
		if (prog == 4):
			os.chdir(path)
			s,t = commands.getstatusoutput("which cd-hit-est")
			if(s == 256):
				uc = raw_input("cd-hit is not found in the environment variables. Do you want to install (y/n) : ")
				if(uc == "y"):
					os.system("git clone https://github.com/weizhongli/cdhit >"+path+"/LogFiles/cdhit.txt 2> "+path+"/LogFiles/cdhitError.txt")
					self.install_cdhit(path)
					os.chdir(path)
				else:
					print ("Please remember that cd-hit-est is required for the running of KREATION and must be in the environment variable $PATH")
			chk2 = self.checkfolder("KREATION")
			if(chk2 == False):
				print("-----KREATION installation-------")
				os.system("git clone https://github.com/SchulzLab/KREATION >"+path+"/LogFiles/KREATION.txt 2> "+path+"/LogFiles/KreationError.txt")
				self.prog_installed.append(path+"/KREATION")
				chkkreation=self.checkfolder(path+"/KREATION/KREATION.py")
				if(chkkreation==False):
					print("KREATION did not install correctly. Please try again")
					sys.exit()
				else:
					print("KREATION installed successfully")
			else:
				print ("The path already contains a folder named KREATION. Please rename it or remove it from the path")
			
		if (prog == 5):
			os.chdir(path)
			chk1 = self.checkfolder("SEECER.tar.gz")
			if(chk1 == False):
				print("-----SEECER installation-----")
				os.system("wget https://zenodo.org/record/3686150/files/SEECER.tar.gz > "+path+"/LogFiles/Seecer.txt 2> "+path+"/LogFiles/SeecerError.txt")
				os.system("tar -zxvf SEECER.tar.gz > "+path+"/LogFiles/Seecer.txt 2> "+path+"/LogFiles/SeecerError.txt")
				chkkreation=self.checkfolder(path+"/SEECER-0.1.3/SEECER/bin/run_seecer.sh")
				if(chkkreation==False):
					print("SEECER did not install correctly. Please try again")
					sys.exit()
				else:
					print("SEECER installed successfully")
			else:
				print ("The path already contains a folder named SEECER.tar.gz. Please rename it or remove it from the path")

	
		if(prog==8):
			os.chdir(path)
			chk5 = self.checkfolder("velvet")
			if(chk5 == False):
				os.system("git clone http://github.com/dzerbino/velvet.git >"+path+"/LogFiles/Velvet.txt 2> "+path+"/LogFiles/VelvetError.txt")
			else:
				print ("The path already contains a folder named velvet. please rename the folder or remove it from the path")
				sys.exit()


	def install_oases(self, path, cs):
		path2 = path + "/oases"
		os.chdir(path2)
		os.system("make "+cs+" > "+path+"/LogFiles/Oases.txt 2> "+path+"/LogFiles/OasesError.txt")
		self.prog_installed.append(path2)
		chk=self.checkfolder(path+"/oases/oases")
		if(chk==False):
			print("Oases did not install correctly. Please try again")
			sys.exit()
		else:
			print("Oases installed successfully")

	def install_orna(self, path):
		path2 = path + "/ORNA"
		os.chdir(path2)
		os.system("bash install.sh > "+path+"/LogFiles/ORNA.txt 2> "+path+"/LogFiles/ORNAError.txt")
		self.prog_installed.append(path2)
		chk=self.checkfolder(path+"/ORNA/build/bin/ORNA")
		if(chk==False):
			print("ORNA did not install correctly. Please try again")
			sys.exit()
		else:
			print("ORNA installed successfully")
	
	def install_velvet(self,path, cs):
		path1 = path + "/velvet"
		os.chdir(path1) 
		print("------Velvet installation------")
		os.system("make "+cs+" > "+path+"/LogFiles/velvet.txt 2> "+path+"/LogFiles/VelvetError.txt")
		self.prog_installed.append(path1)
		chk=self.checkfolder(path+"/velvet/velvetg") and self.checkfolder(path+"/velvet/velveth") 
		if(chk==False):
			print("velvet did not install correctly. Please try again")
			sys.exit()
		else:
			print("velvet installed successfully")

	def install_cdhit(self, path):
		path1 = path + "/cdhit"
		os.chdir(path1)
		print("------cd-hit-est installation------")
		os.system("make > "+path+"/LogFiles/cdhit.txt 2> "+path+"/LogFiles/cdHitError.txt")

	def getoptions(self):
		parser = OptionParser()
		parser.add_option("-f", "--folder", dest="foldername", help="destination folder")
		(options, args) = parser.parse_args()
		return options
	
	def checkfolder(self, program):
		var = os.path.exists(program)
		return var
	
########### MAIN PROGRAM ###########

x = install_script()
y1 = x.getoptions()
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
os.system("mkdir LogFiles")
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
			print("Enter the additional compilation settings of velvet seperated by space (for instance - \'MAXKMERLENGTH=57\'):")
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
		cs = cs + " \'VELVET_DIR=" + vd +"\'"
	x.obtaining_tar(1, pwd)		
	if (flg == 1):
		x.obtaining_tar(8, pwd)
		x.install_velvet(pwd, cs)	
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
					print("Enter the additional compilation settings of velvet seperated by space (for instance - \'MAXKMERLENGTH=57\'):")
					a1 = raw_input()
					a11 = a1.split()
					for a2 in a11:
						a2 = a2.replace("'","")
						a2 = "\'" + a2 + "\'"
						a13 = a13 + " " + a2 
					cs = cs + a13
				flg = 1
				cs = cs + " \'VELVET_DIR="+pwd+"/velvet\'"
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
