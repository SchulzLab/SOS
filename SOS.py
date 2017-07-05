import os
import sys
import optparse
from optparse import OptionParser
from optparse import Option, OptionValueError
import commands
import os.path


class pipeline():
	def getoptions(self):
		parser = OptionParser()
		wd = os.getcwd()
		parser.add_option('-o', '--output',dest='foldername',help='Output directory', action="store", default=wd)
		parser.add_option('-i', '--input',dest='inputname',help='Single end reads (comma seperated)', action="store")
		parser.add_option('-l', '--left',dest='left_name',help='Left end reads (comma seperated)', action="store")		
		parser.add_option('-r', '--right',dest='right_name',help='Right end reads (comma seperated)', action="store")
		parser.add_option('-t', '--threshold',dest='threshold',help='Threshold value for KREATION (optional)', action="store")
		parser.add_option('-b', '--base',dest='base',help='Logarithm Base value for file reduction(optional)', action="store", default="NA")
		parser.add_option('-c', '--config',dest='config_file',help='Config file (required)', action="store")
		parser.add_option('-s', '--step',dest='step',help='The step you want start with (1-SEECER(default) 2-OASES 3-Salmon)', action="store", default=1)
		parser.add_option('-p', '--program', dest='prog', help='Assembly program to be used (Oases or TransABySS)', action="store", default="Oases")
				
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

		if("Salmon" in program):
			if(output1[1]==""):
				print "Salmon not found in the path variable. Please set the path variable to the Salmon bin folder"
				cnt = 0

		if "transabyss" in program:		
			output1=list(output1)
			if(output1[1]==""):
				print "Transabyss not found in the path variable. Please set the path variable to the oases folder"
				cnt = 0
		
		return cnt

	def obtainseecer(self, config_file):
		s_para = "bin/run_seecer.sh"	
		input_file = open(config_file)
		lines = input_file.readlines()
		i=0
		while i < len(lines):
			if(lines[i].rstrip() == "***SEECER***"):
				i = i+1
				while(lines[i][0] != "*"):
					if lines[i][0] == "t":
						temp = lines[i].rstrip().split()
						if(not(os.path.exists(temp[1]))):				
							os.system("mkdir %s" % temp[1])
					if (lines[i].rstrip() != ""):
						tmp1 = lines[i].rstrip().split("	")				
						s_para = s_para+" -"+tmp1[0]+" "+tmp1[1]+" "
					i=i+1
			i=i+1
		return s_para
	
	def obtainoases(self, config_file, arguments, output):
		input_file = open(config_file)
		lines = input_file.readlines()		
		f1 = os.popen('which oases')
		n1 = f1.read().rstrip()
		if "//" in n1:
			n1 = n1.replace("/oases//oases", "/oases/scripts/oases_pipeline.py")
		else:
			n1 = n1.replace("/oases/oases", "/oases/scripts/oases_pipeline.py")
		o_para = "python " +n1
		v_para = ""
		oa_para = ""
		velvet_para="-d \""	
		oases_para="-p \""
		pipeline_para = ""
		i=0
		while i < len(lines):
			if(lines[i].rstrip() == "***OASES PIPELINE***"):
				i = i+1
				while(lines[i][0] != "*"):
					if(lines[i][0] == "m"):
						tmp3 = lines[i].rstrip().split("	")
						mkmer = tmp3[-1]
					if(lines[i].rstrip() != ""):
						tmp2 = lines[i].rstrip().split("	")
						#para2 = para2 + tmp2[0] + " "
						o_para = o_para+" -"+tmp2[0]+" "+tmp2[1]+" "
						pipeline_para = tmp2[0]+" "+tmp2[1]+" "
					i=i+1


			if(lines[i].rstrip() == "***VELVET***"):
				i = i+1
				fl = 0
				file_name=""
				f_name=""
				o_para = o_para + " -d \""
				while(lines[i][0] != "*"):
					if(lines[i].rstrip() != ""):
						if(lines[i].rstrip().upper() == "SHORT" or lines[i].rstrip().upper() == "SHORT" or lines[i].rstrip().upper() == "SHORT2" or lines[i].rstrip().upper() == "LONG" or lines[i].rstrip().upper() == "SHORTPAIRED" or lines[i].rstrip().upper() == "INTERLEAVED"):
							v_para = v_para+" -"+lines[i].rstrip()
						else:
							tmp5 = lines[i].rstrip().split("	")
							v_para = v_para+" -"+tmp5[0]+" "+tmp5[1]+" "
						if (lines[i].rstrip().upper() == "SHORT" or lines[i].rstrip().upper() == "SHORT2" or lines[i].rstrip().upper() == "LONG"):
							fl = fl + 1
					i=i+1
				if (fl == 0):
					v_para = v_para + arguments
				if (fl == 1):
					for inpf in input_files:
						if inpf!=file_name:
							f_name = inpf
					v_para = v_para + f_name
				velvet_para = velvet_para + v_para+"\""
				o_para = o_para + v_para +" \" "
				i = i-1
			if(lines[i].rstrip() == "***OASES***"):
				i = i+1
				o_para = o_para + " -p \"" 
				while(lines[i][0] != "*"):
					if(lines[i].rstrip() != ""):
						tmp6 = lines[i].rstrip().split("	")
						oa_para = oa_para+" -"+tmp6[0]+" "+tmp6[1]+" "
					i=i+1
				oases_para = oases_para + oa_para + "\""
				o_para = o_para + oa_para +" \" "
				i = i-1
			i=i+1
		
		o_para = o_para + "-o /"+output+"/OasesPipeline"
		return o_para

	def obtainkreation(self, config_file, arguments, output):
		input_file = open(config_file)
		lines = input_file.readlines()		
		f1 = os.popen('which oases')
		n1 = f1.read().rstrip()
		if "//" in n1:
			n1 = n1.replace("/oases//oases", "/oases/scripts/oases_pipeline.py")
		else:
			n1 = n1.replace("/oases/oases", "/oases/scripts/oases_pipeline.py")
		o_para = "python " +n1
		v_para = ""
		oa_para = ""
		velvet_para="-d \\\""	
		oases_para="-p \\\""
		pipeline_para = ""
		kreation_para = ""
		i=0
		while i < len(lines):
			if(lines[i].rstrip() == "***VELVET***"):
				i = i+1
				fl = 0
				file_name=""
				f_name=""
				while(lines[i][0] != "*"):
					if(lines[i].rstrip() != ""):
						if(lines[i].rstrip().upper() == "SHORT" or lines[i].rstrip().upper() == "SHORT" or lines[i].rstrip().upper() == "SHORT2" or lines[i].rstrip().upper() == "LONG" or lines[i].rstrip().upper() == "SHORTPAIRED" or lines[i].rstrip().upper() == "INTERLEAVED"):
							v_para = v_para+" -"+lines[i].rstrip()+" "
						else:
							tmp5 = lines[i].rstrip().split("	")
							v_para = v_para+" -"+tmp5[0]+" "+tmp5[1]+" "
						if (lines[i].rstrip().upper() == "SHORT" or lines[i].rstrip().upper() == "SHORT2" or lines[i].rstrip().upper() == "LONG"):
							fl = fl + 1
					i=i+1
				if (fl == 0):
					v_para = v_para + arguments
				if (fl == 1):
					for inpf in input_files:
						if inpf!=file_name:
							f_name = inpf
					v_para = v_para + f_name
				velvet_para = velvet_para + v_para+"\\\""
				i = i-1
			if(lines[i].rstrip() == "***OASES***"):
				i = i+1
				while(lines[i][0] != "*"):
					if(lines[i].rstrip() != ""):
						tmp6 = lines[i].rstrip().split("	")
						oa_para = oa_para+" -"+tmp6[0]+" "+tmp6[1]+" "
					i=i+1
				oases_para = oases_para + oa_para + "\\\""
				i = i-1
			i=i+1
		
		kreation_para = pipeline_para + " "+velvet_para+" "+oases_para
		return kreation_para

	def obtaintransabyss(self, config_file, arguments, output, parameter):
		input_file = open(config_file)
		lines = input_file.readlines()		
		f1 = os.popen('which transabyss')
		n1 = f1.read().rstrip()
		t_para = n1+" "
		i=0
		while i < len(lines):
			if(lines[i].rstrip().upper() == "***TRANSABYSS***"):
				i = i+1
				while(lines[i][0] != "*"):
					if(lines[i][0] == "k"):
						tmp3 = lines[i].rstrip().split("	")
						mkmer = tmp3[-1]
					if(lines[i].rstrip() != ""):
						tmp2 = lines[i].rstrip().split("	")
						t_para = t_para+" -"+tmp2[0]+" "+tmp2[1]+" "
					i=i+1		
			i=i+1
		t_para = t_para + ""+parameter+ " "+arguments+" --name "+output+"/transcripts"
		return t_para			

	def obtainsalmon(self, config_file):
		input_file = open(config_file)
		lines = input_file.readlines()
		sa_index_para = "salmon index "
		sa_quant_para = "salmon quant "		
		i=0
		while i < len(lines):
			if(lines[i].rstrip() == "***SALMON INDEX***"):
				i = i+1
				while(lines[i][0] != "*"):
					if(lines[i].rstrip() != ""):
						tmp3 = lines[i].rstrip().split("	")
						#para3 = para3 + tmp3[0] + " "
					if(tmp3[0] == "i"):
						index_folder = tmp3[1]
						fold_count = 1
					sa_index_para = sa_index_para+" -"+tmp3[0]+" "+tmp3[1]+" "
					i=i+1
				i=i-1
	
			if(lines[i].rstrip() == "***SALMON QUANT***"):
				i = i+1
				while(lines[i][0] != "*"):
					if(lines[i].rstrip() != ""):
						tmp4 = lines[i].rstrip().split("	")
						if(tmp4[0] == "o"):
							quant_folder = tmp4[1]
							quant_count = 1
						sa_quant_para = sa_quant_para+" -"+tmp4[0]+" "+tmp4[1]+" "
					i=i+1
				i=i-1
			i=i+1
		input_file.close()
		return sa_index_para, sa_quant_para


	def getkmer(self, prog, config_file):
		input_file = open(config_file)
		lines = input_file.readlines()
		if(prog.upper()=="OASES"):
			i=0
			mkmer="19"	
			while i < len(lines):
				if(lines[i].rstrip() == "***OASES PIPELINE***"):
					i = i+1
					while(lines[i][0] != "*"):
						if(lines[i][0] == "m"):
							tmp3 = lines[i].rstrip().split()
							mkmer = tmp3[-1]
						i=i+1
				i=i+1
		elif(prog.upper()=="TRANSABYSS"):
			i=0
			mkmer="32"		
			while i < len(lines):
				if(lines[i].rstrip() == "***TRANSABYSS***"):
					i = i+1
					while(lines[i][0] != "*"):
						if(lines[i][0] == "k"):
							tmp3 = lines[i].rstrip().split()
							mkmer = tmp3[-1]
						i=i+1
				i=i+1
		else:
			print("Couldnt find the program "+prog+". Please the check the parameter")
			sys.exit()
		input_file.close()
		return mkmer

	def getReadLength(self, readfile):
		i=0;
		length=0
		with open(readfile, 'r') as f:
			for i, line in enumerate(f):
        			if i == 1:
					length = len(str(line))
					break
       		return length
		
		
############### Main Program ###################
output_fil=""
cl = pipeline()
cl1 = cl.getoptions()

if(cl1.prog.upper() == "OASES"):
	cnt = cl.checkprogram("oases")
	cnt = cl.checkprogram("velvetg")
	cnt = cl.checkprogram("velveth")
else:
	cnt = cl.checkprogram("transabyss")

cnt = cl.checkprogram("run_seecer.sh")
cnt = cl.checkprogram("salmon")

if cnt == 0:
	sys.exit()
if (cl1.foldername != None):
	if "/" not in cl1.foldername:
		a_pathn = os.getcwd() + "/" + cl1.foldername + "/"
	else:
		a_pathn = cl1.foldername + "/"
pathn = os.path.realpath(a_pathn)

if(not(os.path.exists(pathn))):
	os.system("mkdir "+pathn)
###Checking for the paired end files ####
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
			input_f = cl1.inputname
			i1=os.path.realpath(input_f)
			form = i1.split(".")
			forma = form[-1]
			input_files = cl1.inputname.split(",")

if input_files[-1]=="":
	input_files.pop()
n0 = commands.getstatusoutput("which run_seecer.sh")
n = n0[1]

if "//" in n:
	n = n.replace("bin//run_seecer.sh", "")
else:
	n = n.replace("bin/run_seecer.sh", "")

conf = cl1.config_file

input_file = open(conf)
lines = input_file.readlines()
pathname1 = os.path.abspath(sys.argv[0]).replace("SOS.py", "")

if (cl1.foldername != None):
	if "/" not in cl1.foldername:
		pathname = pathname1 + cl1.foldername + "/"
	else:
		pathname = cl1.foldername + "/"
else:
	pathname = os.path.abspath(sys.argv[0]).replace("SOS.py", "")

input_file.close()
step_number = 0
cond = "true"

######## Obtain the step number #########

step_number=int(cl1.step)

if step_number==0:
	sys.exit()

i=0
str_input = ""
arguments = ""
index_folder = "Salmon_output/pipeline_index"
fold_count = 0
quant_folder = "Salmon_output/pipeline_quant"
quant_count = 0
kreation_para=""

mkmer = cl.getkmer(cl1.prog.upper(), conf)
for i10 in range(0,len(input_files)):
	str_input = str_input + input_files[i10] + " "
	temf = commands.getstatusoutput("readlink -f "+input_files[i10])
	input_files[i10] = temf[1]
	if (step_number == 1):
		arguments = arguments + input_files[i10] + "_corrected.fa" + " "
	else:
		arguments = arguments + input_files[i10] + " "
	

#####Collecting Parameters for each program#########
s_para=cl.obtainseecer(cl1.config_file)    ##SEECER PARAMETERS
normalized_file = pathn+"/Normalization_Output/Combined_"+forma+"_corrected_cleared.fa"
		
if(cl1.prog.upper()=="OASES"):
	if(cl1.base == "NA"):                      ##OASES PARAMETERS
		o_para=cl.obtainoases(cl1.config_file, arguments, pathn)
		kreation_para=cl.obtainkreation(cl1.config_file, arguments, pathn)
	else:
		o_para=cl.obtainoases(cl1.config_file, normalized_file, pathn)
		kreation_para=cl.obtainkreation(cl1.config_file, normalized_file, pathn)
else:                                              ##TRANSABYSS PARAMETERS
	if(cl1.left_name != None and cl1.right_name != None):
		if(cl1.base != None):
			t_para=cl.obtaintransabyss(cl1.config_file, normalized_file, pathn, "--pe")
		else:	
			t_para=cl.obtaintransabyss(cl1.config_file, arguments, pathn, "--pe")
	else:
		if(cl1.base != None):
			t_para=cl.obtaintransabyss(cl1.config_file, normalized_file, pathn, "--se")
		else:	
			t_para=cl.obtaintransabyss(cl1.config_file, arguments, pathn, "--se")
  
sa_index_para, sa_quant_para=cl.obtainsalmon(cl1.config_file)   ##SALMON PARAMETERS

os.chdir(n)
if (not(os.path.exists(pathn+"/logfiles/"))):
	os.system("mkdir "+pathn+"/logfiles/")


### SEECER execution ###
if(step_number==1):
	for k in input_files:
		s_para = s_para+ " " +k
	with open(pathn + "/logfiles/commands.txt","a") as command_file:
		command_file.write(s_para)
		command_file.write("\n")
	#if(step_number==1):
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

### Clearing the file ####
if (cl1.base == "NA"):
	print("Skipping normalization step")
else:
	if(not(os.path.exists(pathn+"/Normalization_Output"))):
		os.system("mkdir "+pathn+"/Normalization_Output")
	if cl1.left_name != None and cl1.right_name != None:
		red_flag = 1
		os.system("ORNA -pair1 "+input_files[0]+"_corrected.fa -pair2 "+input_files[1]+"_corrected.fa -base "+str(cl1.base)+" -output "+pathn+"/Normalization_Output/Combined_"+forma+"_corrected_cleared.fa -kmer " +mkmer+" >"+pathn+ "/logfiles/Normalization_log.txt 2>&1")			
	else:	
		red_flag = 1
		os.system(">"+pathn+"/Combined."+forma)
		
		for clf in input_files:
			clf=clf+"_corrected.fa"
			os.system("cat "+clf+" >> "+pathn+"/Combined."+forma)	
		os.system("ORNA -input "+pathn+"/Combined."+forma+" -base "+str(cl1.base)+" -output "+pathn+"/Normalization_Output/Combined_"+forma+"_corrected_cleared.fa -kmer " +mkmer +" >"+pathn+ "/logfiles/Normalization_log.txt 2>&1")
	je_file = pathn+"/Normalization_Output/Combined_"+forma+"_corrected_cleared.fa"
	input_files = je_file.split(",")	

###Assembly execution ###
assembly_program = cl1.prog
if(cl1.threshold != None):
	if(cl1.prog.upper() == "OASES"):
		print("python "+pathname1+"/KREATION.py -p "+cl1.prog+" -s 2 -o "+pathn+" -r "+str(cl.getReadLength(input_files[0]))+" -t "+str(cl1.threshold)+" -k "+mkmer+ " -a m -c \""+kreation_para+"\"")
		os.system("python "+pathname1+"/KREATION.py -p oases -s 2 -o "+pathn+" -r "+str(cl.getReadLength(input_files[0]))+" -t "+str(cl1.threshold)+" -k "+mkmer+ " -a m -c \""+kreation_para+"\"")
	else:
		os.system("python "+pathname1+"/KREATION.py -p transabyss -s 2 -o "+pathn+" -r "+str(cl.getReadLength(input_files[0]))+" -t "+str(cl1.threshold)+" -k "+mkmer+ " -a k -c \""+kreation_para+"\"")       

####### KREATION EXECUTION 
else:
	if(cl1.prog.upper()=="OASES"):
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
		cceo = os.path.exists(pathn + "/OasesPipelineMerged/transcripts.fa")
		if cceo == False:
			ffco = 1
		if ffco == 1:
			print "OASES did not run properly. Please see the log files and try again"
			sys.exit()
		else:
			print "OASES executed successfully"
	else:
		with open(pathn + "/logfiles/commands.txt","a") as command_file:
			command_file.write(o_para)
			command_file.write("\n")
		os.chdir(pathn)
		if (step_number<=2):
			try:
				os.system(t_para+" >"+pathn+"/logfiles/transabyss_log.txt 2>&1")
			except:
				sys.exit()
	
		### Check transabyss ###
		ffco = 0
		cceo = os.path.exists(pathn + "/transcripts-final.fa")
		if cceo == False:
			ffco = 1
		if ffco == 1:
			print "OASES did not run properly. Please see the log files and try again"
			sys.exit()
		else:
			print "TRANSABYSS executed successfully"
			os.system("mv "+pathn+"/transcripts-final.fa "+pathn+"/transcripts.fa")
	
### Salmon execution ###
if(not(os.path.exists("Salmon_output"))):
	os.system("mkdir Salmon_output")

if(step_number<=3):
	if(fold_count == 0):
		index_output = pathn + "/Salmon_output/pipeline_index"
		sa_index_para = sa_index_para + " -i " + index_output
	
	if(cl1.threshold != None):
		index_transcripts = pathn + "/Cluster/Combined/transcripts.fa"
	else:
		if(cl1.prog.upper()=="OASES"):
			index_transcripts = pathn + "/OasesPipelineMerged/transcripts.fa"
		else:
			index_transcripts = pathn + "/transcripts.fa"
	
	sa_index_para = sa_index_para + " -t "+index_transcripts+ "" 

	with open(pathn + "/logfiles/commands.txt","a") as command_file:
		command_file.write(sa_index_para)
		command_file.write("\n")
		
	#os.system(sa_index_para+" >"+pathn+ "/logfiles/Salmon_index_log.txt 2>&1") 

	if(quant_count == 0):
		quant_output = pathn + "/Salmon_output/pipeline_quant"
		sa_quant_para = sa_quant_para + " -o " + quant_output
	if(cl1.left_name != None and cl1.right_name != None):
		sa_quant_para = sa_quant_para + " -i "+index_output+ " -1 "+arguments.split()[0]+" -2 "+arguments.split()[1]+" "
	else:		
		sa_quant_para = sa_quant_para + " -i "+index_output+ " -r " +arguments
	
	with open(pathn + "/logfiles/commands.txt","a") as command_file:
		command_file.write(sa_quant_para)
		command_file.write("\n")
	
	print sa_quant_para	
	os.system(sa_quant_para+" >"+pathn+"/logfiles/Salmon_quant_log.txt 2>stderr.txt")

### Check Salmon ###
ffcsa = 0
ccesa = os.path.exists(quant_output + "/quant.sf")
if ccesa == False:
	ffcsa = 1
if ffcsa == 1:
	print "Salmon did not run properly. Please see the log files and try again"
	sys.exit()
else:
	print "Salmon executed successfully"

######## Collecting Outputs ###########
os.chdir(pathn)
if(not(os.path.exists("Final_Output"))):
	os.system("mkdir Final_Output")

if(cl1.threshold != None):
	os.system("mv "+pathn + "/Cluster/Combined/transcripts.fa Final_Output/")
else:
	if(cl1.prog=="OASES"):
		os.system("mv "+pathn + "/OasesPipelineMerged/transcripts.fa Final_Output/")
	else:
		os.system("mv "+pathn + "/transcripts.fa Final_Output/")

os.system("mv " +quant_output+ "/quant.sf Final_Output/")
os.system("mv " +index_transcripts+ " Final_Output/")
if(cl1.base == None):
	for i in input_files:
		os.system("mv " +i+ "_corrected.fa Final_Output/")
else:
	input_files = arguments.split(" ")
	input_files.pop()
	for i in input_files:
		os.system("mv " +i+ " Final_Output/")

