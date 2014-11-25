import os
import sys
import optparse
from optparse import OptionParser
from optparse import Option, OptionValueError
import commands

class pipeline():
	def getoptions(self):
		parser = OptionParser()
		wd = os.getcwd()
		parser.add_option('-o', '--output',dest='foldername',help='Output director', action="store", default=wd)

		parser.add_option('-i', '--input',dest='inputname',help='Single end read', action="store")
		parser.add_option('-l', '--left',dest='left_name',help='Left end read', action="store")		
		parser.add_option('-r', '--right',dest='right_name',help='Right end read', action="store")
		
		parser.add_option('-t', '--threshold',dest='threshold',help='Threshold value for file reduction', action="store")
		parser.add_option('-p', '--per',dest='perc',help='Percentage', action="store")
		
		parser.add_option('-c', '--config',dest='config_file',help='Config file', action="store")
		parser.add_option('-s', '--step',dest='step',help='The step you want start with (1-SEECER(default) 2-OASES 3-SAILFISH)', action="store", default=1)
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
		
############### Main Program ###################
output_fil=""
cl = pipeline()
cnt = cl.checkprogram("oases")
cnt = cl.checkprogram("velvetg")
cnt = cl.checkprogram("velveth")
cnt = cl.checkprogram("run_seecer.sh")
cnt = cl.checkprogram("sailfish")

if cnt == 0:
	sys.exit()

cl1 = cl.getoptions()
if (cl1.foldername != None):
	if "/" not in cl1.foldername:
		a_pathn = os.getcwd() + "/" + cl1.foldername + "/"
	else:
		a_pathn = cl1.foldername + "/"
pathn = os.path.realpath(a_pathn)
os.system("mkdir "+pathn)

if cl1.left_name == None and cl1.right_name !=None:
	print "Missing one end"
	sys.exit()
elif cl1.left_name != None and cl1.right_name == None:
	print "Missing one end"
	sys.exit()
elif (cl1.inputname != None and cl1.left_name != None) or (cl1.inputname != None and cl1.right_name != None):
	print "Cannot give single end and paired end at the same time"
	sys.exit()  
else:
	if cl1.left_name != None and cl1.right_name != None:  	 		
		if "," in cl1.left_name:		
			input_left = cl1.left_name.split(",")
			output_left=""
		
			for i in input_left:
				i1=os.path.realpath(i)
				form = i1.split(".")
				forma = form[-1]
				output_left = output_left + " " + i1
			output_left_f = pathn+"/combined_input_left."+forma 
			os.system("cat "+output_left+" > "+pathn+"/combined_input_left."+forma)
			output_fil = output_fil + pathn+"/combined_input_left."+forma + ","
		else:
			form = os.path.realpath(cl1.left_name).split(".")
			forma = form[-1]
			output_fil = output_fil + os.path.realpath(cl1.left_name) + ","
		
		if "," in cl1.right_name:		
			input_right = cl1.right_name.split(",")
			output_right=""

			for i in input_right:
				i1=os.path.realpath(i)
				form = i1.split(".")
				forma = form[-1]
				output_right = output_right + " " + i1
			output_right_f = pathn+"/combined_input_right."+forma 
			os.system("cat "+output_right+" > "+pathn+"/combined_input_right."+forma)
			output_fil = output_fil + pathn+"/combined_input_right."+forma + ","
		else:
			form = os.path.realpath(cl1.right_name).split(".")
			forma = form[-1]
			output_fil = output_fil + os.path.realpath(cl1.right_name) + ","
		print output_fil		
		input_files = output_fil.split(",") 
	
	else:
		if "," in cl1.inputname:
			input_f = cl1.inputname.split(",")
			output_f=""
			for i in input_f:
				i1=os.path.realpath(i)
				form = i1.split(".")
				forma = form[-1]
				output_f = output_f + " " + i1
			output_fil = pathn+"/combined_input."+forma 
			print output_f
			os.system("cat "+output_f+" >> "+pathn+"/combined_input."+forma)
			input_files = output_fil.split(",") 
		else:
			print "There is a single file"
			input_files = cl1.inputname.split(",")
if input_files[-1]=="":
	input_files.pop()

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

conf = cl1.config_file

input_file = open(conf)
lines = input_file.readlines()
pathname1 = os.path.abspath(sys.argv[0]).replace("pipeline_1.py", "")

if (cl1.foldername != None):
	if "/" not in cl1.foldername:
		pathname = pathname1 + cl1.foldername + "/"
	else:
		pathname = cl1.foldername + "/"
else:
	pathname = os.path.abspath(sys.argv[0]).replace("pipeline_1.py", "")

input_file.close()
step_number = 0
cond = "true"


######## Obtain the step number ##########

step_number=int(cl1.step)

if step_number==0:
	sys.exit()

####### Clearing the file ########	
thi = str(cl1.threshold)
per1 = (cl1.perc)
red_flag = 0
if (thi != "None"):
	red_flag = 1
	for clf in input_files:
		os.system("cat "+clf+" >> "+pathn+"/Combined."+forma)	
	threshold = int(cl1.threshold)
	os.system("mkdir "+pathn+"/Jellyfish_Output")
	os.system("python sequence_cleaner.py -i "+pathn+"/Combined."+forma+" -t "+str(threshold)+" -o "+pathn+"/Jellyfish_Output -p " +per1)
	je_file = pathn+"/Jellyfish_Output/Combined_"+forma+"_cleared.fa"
	input_files = je_file.split(",")	
	
############## Initializations #####################

i=0
s_para = "bin/run_seecer.sh"
o_para = "python " +n1
v_para = ""
oa_para = ""
str_input = ""
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
	str_input = str_input + input_files[i10] + " "
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
		fl = 0
		file_name=""
		f_name=""
		o_para = o_para + " -d \""
		while(lines[i][0] != "*"):
			if(lines[i].rstrip() != ""):
				tmp5 = lines[i].rstrip().split()
				if((tmp5[0] == "interleaved") and (red_flag==1)):
					print "Ignoring interleaved option because of read reduction"
				elif((tmp5[0] == "shortPaired") and (red_flag==1)):
					print "Ignoring shortPaired option because of read reduction"
				else:				
					para5 = para5 + tmp5[0] + " "
					v_para = v_para+" -"+lines[i].rstrip()+" "
					if (lines[i].rstrip().upper() == "SHORT" or lines[i].rstrip().upper() == "SHORT2" or lines[i].rstrip().upper() == "LONG"):
						fl = fl + 1
						#file_name = tmp5[1]
			i=i+1
		if (fl == 0):
			v_para = v_para + arguments
		if (fl == 1):
			for inpf in input_files:
				if inpf!=file_name:
					f_name = inpf
			v_para = v_para + f_name
		o_para = o_para + v_para +" \" "
		i = i-1

	if(lines[i].rstrip() == "***OASES***"):
		i = i+1
		o_para = o_para + " -p \"" 
		while(lines[i][0] != "*"):
			if(lines[i].rstrip() != ""):
				tmp6 = lines[i].rstrip().split()
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
		i=i-1
	
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
		i=i-1
	i=i+1

os.chdir(n)
os.system("mkdir "+pathn+"/logfiles/")
### SEECER execution ###
if(step_number==1):
	for k in input_files:
		s_para = s_para+ " " +k
	with open(pathn + "/logfiles/commands.txt","a") as command_file:
		command_file.write(s_para)
		command_file.write("\n")
	if(step_number==1):
		os.system("bash "+s_para+" >>"+pathn+"/logfiles/seecer_log.txt 2>&1")
	
### Check SEECER ###
if(step_number==1):
	ffcs = 0
	for k1 in input_files:
		cce = os.path.exists(k1 + "_corrected.fa")
		if cce == False:
			ffcs = 1
	if ffcs == 1:
		print "SEECER did not run properly. Please see the log files and try again"
		sys.exit()
	else:
		print "SEECER executed successfully"
		
### OASES PIPELINE execution ###

with open(pathn + "/logfiles/commands.txt","a") as command_file:
	command_file.write(o_para)
	command_file.write("\n")
	
os.chdir(pathn)
if (step_number<=2):
	try:
		os.system(o_para+" >"+pathn+"/logfiles/oases_log.txt 2>&1")
	except:
		sys.exit()

### Check oases ###
ffco = 0
cceo = os.path.exists(pathn + "/oasesPipelineMerged/transcripts.fa")
if cceo == False:
	ffco = 1
if ffco == 1:
	print "OASES did not run properly. Please see the log files and try again"
	sys.exit()
else:
	print "OASES executed successfully"



### Sailfish execution ###
os.system("mkdir sailfish_output")

if(step_number<=3):
	if (fold_count == 0):
		index_output = pathn + "/sailfish_output/pipeline_index"
		sa_index_para = sa_index_para + " -o " + index_output

	index_transcripts = pathn + "/oasesPipelineMerged/transcripts.fa"
	sa_index_para = sa_index_para + " -t "+index_transcripts+ " --force" 

	with open(pathn + "/logfiles/commands.txt","a") as command_file:
		command_file.write(sa_index_para)
		command_file.write("\n")
		
	os.system(sa_index_para+" >"+pathn+ "/logfiles/sailfish_index_log.txt 2>&1") 

	if(quant_count == 0):
		quant_output = pathn + "/sailfish_output/pipeline_quant"
		sa_quant_para = sa_quant_para + " -o " + quant_output
	sa_quant_para = sa_quant_para + " -i "+index_output+ " -r " +str_input
	
	with open(pathn + "/logfiles/commands.txt","a") as command_file:
		command_file.write(sa_quant_para)
		command_file.write("\n")
		
	os.system(sa_quant_para+" >"+pathn+"/logfiles/sailfish_quant_log.txt 2>stderr.txt")
	
### Check Sailfish ###
ffcsa = 0
ccesa = os.path.exists(quant_output + "/quant.sf")
if ccesa == False:
	ffcsa = 1
if ffcsa == 1:
	print "Sailfish did not run properly. Please see the log files and try again"
	sys.exit()
else:
	print "Sailfish executed successfully"


######## Collecting Outputs ###########
os.chdir(pathn)
os.system("mkdir Final_Output")
os.system("mv " +quant_output+ "/quant.sf Final_Output/")
os.system("mv " +index_transcripts+ " Final_Output/")
for i in input_files:
	os.system("mv " +i+ "_corrected.fa Final_Output/")


	
