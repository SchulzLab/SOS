import os
import sys
import optparse
from optparse import OptionParser
from optparse import Option, OptionValueError
import commands

class pipeline():
	def getoptions(self):
		parser = OptionParser()
		parser.add_option('-o', '--output',dest='foldername',help='Output director', action="store")
		parser.add_option('-i', '--input',dest='inputname',help='Input file', action="store")
		parser.add_option('-c', '--config',dest='config_file',help='Config file', action="store")
		(options, args) = parser.parse_args()
		return options
		
	def checkprogram(self, program):
		output1 = commands.getstatusoutput("which "+program)
		cnt = 1
		if "oases" in program:		
			output1=list(output1)
			if(output1[1]==""):
				print "oases not found in the path variable. Please set the path variable to the oases folder"
				cnt = 0
				
		if ("velvetg" in program) or ("velveth" in program):
			if(output1[1]==""):
				print "velvet not found in the path variable. Please set the path variable to the velvet folder"
				cnt = 0

		if("run_seecer.sh" in program):			
			if(output1[1]==""):
				print "SEECER not found in the path variable. Please set the path variable to the SEECER/bin folder"
				cnt = 0

		if("sailfish" in program):
			if(output1[1]==""):
				print "sailfish not found in the path variable. Please set the path variable to the sailfish bin folder"
				cnt = 0
		
		return cnt
		
	def sequence_count(self, input_file):
		y = input_file		
		x = y.split(".")
		file = open(y)
		l_c =0		
		for i in file.readlines():
			l_c = l_c + 1 
		if(x[-1].upper() == "FASTQ" or x[-1].upper() == "FQ"):
			l_c = l_c/4 
		if(x[-1].upper() == "FASTA" or x[-1].upper() == "FA"):
			l_c = l_c/2
		return l_c 


############### Main Program ###################
cl = pipeline()
cl1 = cl.getoptions()
cnt = 0
#output1 = commands.getstatusoutput("which oases_pipeline.py")

input_files = cl1.inputname.split(",")

cnt = cl.checkprogram("oases")
cnt = cl.checkprogram("velvetg")
cnt = cl.checkprogram("velveth")
cnt = cl.checkprogram("run_seecer.sh")
cnt = cl.checkprogram("sailfish")

if cnt == 0:
	sys.exit()


try:
	if cl1.foldername != None:
		try:
			os.system("mkdir "+cl1.foldername)
		except:
			print "The foldername exists"
except:
	sys.exit()

n0 = commands.getstatusoutput("which run_seecer.sh")
n = n0[1]
if "//" in n:
	n = n.replace("bin//run_seecer.sh", "")
else:
	n = n.replace("bin/run_seecer.sh", "")

f1 = os.popen('which oases')
n1 = f1.read().rstrip()
if "//" in n1:
	n1 = n1.replace("/oases//oases", "/oases/scripts/oases_pipeline.py")
else:
	n1 = n1.replace("/oases/oases", "/oases/scripts/oases_pipeline.py")

f2 = os.popen('which sailfish')
n2 = f2.read().rstrip()
if "//" in n2:
	n2 = n2.replace("/sailfish", "")
else:
	n2 = n2.replace("sailfish", "")
	
conf = cl1.config_file

input_file = open(conf)
lines = input_file.readlines()
pathname1 = os.path.abspath(sys.argv[0]).replace("pipeline.py", "")

if (cl1.foldername != None):
	if "/" not in cl1.foldername:
		pathname = pathname1 + cl1.foldername + "/"
	else:
		pathname = cl1.foldername + "/"
else:
	pathname = os.path.abspath(sys.argv[0]).replace("pipeline.py", "")

input_file.close()
step_number = 0
cond = "true"


######## Obtain the step number ##########


while (cond == "true"):
	print "Steps in the pipeline"
	print "1.	SEECER"
	print "2.	OASES"
	print "3.	SAILFISH"
	print "0.	EXIT"
	print "-------------------"
	step_number = input("Enter the step you want to start with: ")
	if(step_number<4 and step_number>=0):
		cond = "false"
	else:
		print "You have entered an invalid step number. Please enter again"

if step_number==0:
	sys.exit()

thi = raw_input("Do you want to clean your input files (y/n) : ")
if (thi.upper() == "YES" or thi.upper() == "Y"):
	thiv = raw_input("Enter the threshold value :")
	threshold = int(thiv)
	for clf in input_files:
		os.system("python sequence_cleaner.py -i "+clf+" -t "+str(threshold)+" ")

	for cl in range(0, len(input_files)):
		input_files[cl] = input_files[cl].replace(".","_")
		input_files[cl] = input_files[cl]+"_cleared.fa"

############## Initializations #####################

i=0
s_para = "bin/run_seecer.sh"
o_para = "python " +n1
v_para = ""
oa_para = ""
sa_index_para = "sailfish index "
sa_quant_para = "sailfish quant "
para1 = ""
para2 = ""
para3 = ""
para4 = ""
para5 = ""
para6 = ""
argu1 = ""
arguments = ""
index_folder = "sailfish_output/pipeline_index"
fold_count = 0
quant_folder = "sailfish_output/pipeline_quant"
quant_count = 0

for i10 in range(0,len(input_files)):
	temf = commands.getstatusoutput("readlink -f "+input_files[i10])
	input_files[i10] = temf[1]
	if (step_number == 1):
		arguments = arguments + input_files[i10] + "_corrected.fa" + " "
		argu1 = argu1 + input_files[i10] + " "
	else:
		arguments = arguments + input_files[i10] + " "
		argu1 = argu1 + input_files[i10] + " "
			
############## collecting parameters #####################

while i < len(lines):
	if(lines[i].rstrip() == "***SEECER***"):
		i = i+1
		while(lines[i][0] != "*"):
			if lines[i][0] == "t":
				temp = lines[i].rstrip().split()				
				os.system("mkdir %s" % temp[1])
			if (lines[i].rstrip() != ""):
				tmp1 = lines[i].rstrip().split()				
				para1 = para1 + tmp1[0] + " "			
				s_para = s_para+" -"+lines[i].rstrip()+" "
			i=i+1
	
	if(lines[i].rstrip() == "***OASES PIPELINE***"):
		i = i+1
		while(lines[i][0] != "*"):
			if(lines[i].rstrip() != ""):
				tmp2 = lines[i].rstrip().split()
				para2 = para2 + tmp2[0] + " "
				o_para = o_para+" -"+lines[i].rstrip()+" "
			i=i+1

	if(lines[i].rstrip() == "***VELVET***"):
		i = i+1
		o_para = o_para + " -d \"" + arguments
		while(lines[i][0] != "*"):
			if(lines[i].rstrip() != ""):
				tmp5 = lines[i].rstrip().split()
				para5 = para5 + tmp5[0] + " "
				v_para = v_para+" -"+lines[i].rstrip()+" "
			i=i+1
		o_para = o_para + v_para +" \" "
		i = i-1

	if(lines[i].rstrip() == "***OASES***"):
		i = i+1
		o_para = o_para + " -p \"" 
		while(lines[i][0] != "*"):
			if(lines[i].rstrip() != ""):
				tmp6 = lines[i].rstrip().split()
				para6 = para5 + tmp5[0] + " "
				oa_para = oa_para+" -"+lines[i].rstrip()+" "
			i=i+1
		o_para = o_para + oa_para +" \" "
		i = i-1
	
	if(lines[i].rstrip() == "***SAILFISH INDEX***"):
		i = i+1
		while(lines[i][0] != "*"):
			if(lines[i].rstrip() != ""):
				tmp3 = lines[i].rstrip().split()
				para3 = para3 + tmp3[0] + " "
				if(tmp3[0] == "o"):
					index_folder = tmp3[1]
					fold_count = 1
				sa_index_para = sa_index_para+" -"+lines[i].rstrip()+" "
			i=i+1
	
	if(lines[i].rstrip() == "***SAILFISH QUANT***"):
		i = i+1
		while(lines[i][0] != "*"):
			if(lines[i].rstrip() != ""):
				tmp4 = lines[i].rstrip().split()
				para4 = para4 + tmp4[0] + " "
				if(tmp4[0] == "o"):
					quant_folder = tmp3[1]
					quant_count = 1
				sa_quant_para = sa_quant_para+" -"+lines[i].rstrip()+" "
			i=i+1
	i=i+1

os.chdir(n)

### SEECER execution ###
for k in input_files:
	s_para = s_para+ " " +k

print s_para 
if(step_number==1):
	os.system(s_para)


### OASES PIPELINE execution ###
print o_para
os.chdir(pathname)
if (step_number<=2):
	try:
		print "Hello"
		os.system(o_para)
	except:
		sys.exit()


### Sailfish execution ###
os.system("mkdir sailfish_output")
#os.chdir(n2)

if(step_number<=3):
	if (fold_count == 0):
		index_output = pathname + "sailfish_output/pipeline_index"
		sa_index_para = sa_index_para + " -o " + index_output

	index_transcripts = pathname + "oasesPipelineMerged/transcripts.fa"
	sa_index_para = sa_index_para + " -t "+index_transcripts+ " --force" 

	print ""
	print sa_index_para
	os.system(sa_index_para) 

	if(quant_count == 0):
		quant_output = pathname + "sailfish_output/pipeline_quant"
		sa_quant_para = sa_quant_para + " -o " + quant_output
	sa_quant_para = sa_quant_para + " -i "+index_output+ " -r " +arguments
	print ""
	print sa_quant_para
	os.system(sa_quant_para)



######## Collecting Outputs ###########
os.chdir(pathname)
os.system("mkdir Final_Output")
os.system("mv " +quant_output+ "/quant.sf Final_Output/")
os.system("mv " +index_transcripts+ " Final_Output/")
for i in input_files:
	os.system("mv " +i+ "_corrected.fa Final_Output/")

