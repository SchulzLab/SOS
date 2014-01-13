import os
from optparse import OptionParser
import subprocess
import sys

class install_script():
	def obtaining_tar(self, prog):
		if (prog == 4):
			chk = self.checkfolder("oases")
			
			if(chk == False):
				os.system("git clone git://github.com/dzerbino/oases.git")
			else:
				print ("The path already contains a folder named oases. please rename the folder or remove it from the path")
				sys.exit()
							
			chk1 = self.checkfolder("SEECER-0.1.3.tar.gz")
			if(chk1 == False):
				os.system("wget http://sb.cs.cmu.edu/seecer/downloads/SEECER-0.1.3.tar.gz")
				os.system("tar -zxvf SEECER-0.1.3.tar.gz")
			else:
				print ("The path already contains a folder named SEECER-0.1.3.tar.gz. please rename it or remove it from the path")
			
			chk2 = self.checkfolder("Sailfish-0.6.2-Linux_x86-64.tar.gz")			
			if(chk2 == False):
				os.system("wget https://github.com/kingsfordgroup/sailfish/releases/download/v0.6.2/Sailfish-0.6.2-Linux_x86-64.tar.gz")
				os.system("tar -zxvf Sailfish-0.6.2-Linux_x86-64.tar.gz")
			
			else:
				print ("The path already contains a folder named Sailfish-0.6.2-Linux_x86-64.tar.gz. please rename it or remove it from the path") 
		
		if(prog==3):
			chk2 = self.checkfolder("Sailfish-0.6.2-Linux_x86-64.tar.gz")			
			if(chk2 == False):
				os.system("wget https://github.com/kingsfordgroup/sailfish/releases/download/v0.6.2/Sailfish-0.6.2-Linux_x86-64.tar.gz")
				os.system("tar -zxvf Sailfish-0.6.2-Linux_x86-64.tar.gz")

		if(prog==2):
			chk6 = self.checkfolder("oases")
			if(chk6 == False):
				os.system("git clone git://github.com/dzerbino/oases.git")

		if(prog==1):
			chk4 = self.checkfolder("SEECER-0.1.3.tar.gz")
			if(chk4 == False):
				os.system("wget http://sb.cs.cmu.edu/seecer/downloads/SEECER-0.1.3.tar.gz")
				os.system("tar -zxvf SEECER-0.1.3.tar.gz")
			else:
				print ("The path already contains a folder named SEECER-0.1.3.tar.gz. please rename it or remove it from the path")

		if(prog==5):
			chk5 = self.checkfolder("velvet")
			if(chk5 == False):
				os.system("git clone git://github.com/dzerbino/velvet.git")
			else:
				print ("The path already contains a folder named velvet. please rename the folder or remove it from the path")
				sys.exit()
				
	def install_oases(self, path, cs):
		path2 = path + "/oases"
		os.chdir(path2)
		os.system("make "+cs)
#		os.system("")
	
	def install_velvet(self,path, cs):
		path1 = path + "/velvet"
		os.chdir(path1) 
		print "------Velvet installation------"
		os.system("make "+cs)
		
	def getoptions(self):
		parser = OptionParser()
		parser.add_option("-f", "--folder", dest="foldername", help="destination folder")
		(options, args) = parser.parse_args()
		return options
	
	def checkfolder(self, program):
		var = os.path.exists(program)
		return var
	

########### MAIN PROGRAM ###########3

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

print ("Programs to install :")
print ("1.	SEECER")
print ("2.	OASES")
print ("3.	SAILFISH")
print ("4.	ALL")
print ("5.	QUIT")

x1 = raw_input("Enter the option number (if multiple options then separate it by comma): ")
y = x1.split(",")
acs = ""
vd = ""
flg = 0
cs = ""
a13 = ""
if("5" in y):
	print "Thank you. It was nice working for you"
	sys.exit()

if "4" in y:
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
	x.obtaining_tar(4)
	if (flg == 1):
		x.obtaining_tar(5)
		x.install_velvet(pwd, cs)	
	x.install_oases(pwd, cs)	

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
			if(vc == "n"):
				vd = raw_input("Enter the location of velvet : ")
				if("\\" not in vd):
					cs = cs + " \'VELVET_DIR=" +pwd+"\\"+ vd +"\'"
				else:
					cs = cs + " \'VELVET_DIR=" + vd +"\'"
			x.obtaining_tar(2)
			if(flg == 1):			
				x.obtaining_tar(5)
				x.install_velvet(pwd, cs)
			x.install_oases(pwd, cs)
		else:
			x.obtaining_tar(int(i))