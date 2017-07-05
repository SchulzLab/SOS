import os
import sys
import optparse
from optparse import OptionParser
from optparse import Option, OptionValueError
import commands
import math

class pipeline():
	def getoptions(self):
		stat1, cr=commands.getstatusoutput("which KREATION.py")
		cuwodi = os.path.dirname(cr)
		parser = OptionParser()
		#parser.add_option('-c', '--config',dest='config_file',help='path to the config file (only text file)', action="store")
		parser.add_option('-c', '--command',dest='rest',help='rest of the command', action="store")
		parser.add_option('-p', '--program',dest='prog',help='Program to be used', action="store", default="oases_pipeline_2.py")
		parser.add_option('-s', '--step',dest='ss',help='kmer step size for the assembly process (default=2)', action="store",default=2)
		parser.add_option('-o', '--output',dest='out',help='path to the output directory, directory will be created if non-existent', action="store",default=cuwodi)
		parser.add_option('-r', '--read',dest='read_length',help='read length (required)', action="store")
		parser.add_option('-t', '--threshold',dest='cut_off',help='cut_off for d_score', action="store",default=0.01)		
		parser.add_option('-k', '--kmer',dest='kmer',help='Minimum Kmer to be used', action="store", default="21")	
		parser.add_option('-a', '--parameter',dest='kparam',help='Minimum Kmer Parameter to be used', action="store", default="m")	
		(options, args) = parser.parse_args()
		return options

stat, kr=commands.getstatusoutput("which KREATION.py")
cwd = os.path.dirname(kr)
cl = pipeline()
cl1 = cl.getoptions()
threshold=float(cl1.cut_off)
#conf = os.path.abspath(cl1.config_file)par
output = cl1.out
output = os.path.abspath(output) 
rl=int(cl1.read_length)
extended=""
kmer=""
os.system("mkdir "+output)
os.system("mkdir "+output+"/Assembly/")
os.system("mkdir "+output+"/Cluster/")
output1=output+"/Assembly/"
#os.chdir(output1)
cnt=0
pval=0

#input_file = open(conf)
#lines = input_file.readlines()
#count=0
#for i in lines:
#if(not(i.startswith('#'))):
#	if(count==0):
program_name = cl1.prog
program_name = program_name.replace("\n","")
if(program_name.upper() == "OASES"):
	program_name = "oases_pipeline_2.py"
pn = program_name.split(".")
pnn = pn[0]
filename="transcripts.fa"
min_k=int(cl1.kmer)
rest_command=cl1.rest
para_min_k = "-"+cl1.kparam
i = min_k
os.system("mkdir "+output+"/KREATION/")	
f=open(""+output+"/KREATION/p_value.txt","a")

while i <= rl:
	output2=output1+"/"+str(i)+"/"
	if(not(os.path.exists(output2))):	
		os.system("mkdir "+output2)	
	os.chdir(output2)
	if(not(os.path.exists(output+"/Cluster/"+str(i)))):	
		os.system("mkdir "+output+"/Cluster/"+str(i)+"/")
	if(not(os.path.exists(output+"/Cluster/Combined"))):
		os.system("mkdir "+output+"/Cluster/Combined/")
	command = program_name + " " + para_min_k + " " +str(i)+ " " +rest_command	
	os.system(command)
	status, ts=commands.getstatusoutput("find "+output2.strip()+" -name "+filename.strip())
	dirname = os.path.dirname(ts)
	ts1=ts.replace(str(filename.strip()),str(i)+"_transcripts_org.fa")
	os.system("mv "+ts+" "+ts1)
	cmd_rn = "perl "+cwd+"/Utils/rename_sequence.pl "+ts1+" "+str(i)+""	
	os.system(cmd_rn)
	os.system("cd-hit-est -i "+dirname+"/"+str(i)+"_transcripts_org_clu.fa -o "+output+"/Cluster/"+str(i)+"/transcripts_clust.fa -c 0.99 -M 2000M -T 10 >> "+output+"/Cluster/"+str(i)+"/transcripts_clust.log")
	os.system("perl "+cwd+"/Utils/Combine_files.pl "+output+" "+str(min_k)+" "+str(i)+" "+str(cl1.ss))
	os.system("cd-hit-est -i "+output+"/Cluster/Combined/combine.fa -o "+output+"/Cluster/Combined/combined_clust.fa -c 0.99 -M 2000M -T 10 >> "+output+"/Cluster/Combined/combined_clust_"+str(i)+".log")
	s,t = commands.getstatusoutput("perl "+cwd+"/Utils/calculate_extended.pl "+output+"/Cluster/Combined/combined_clust.fa "+str(min_k)+" "+str(i)+" "+str(cl1.ss))
	ex=t.split("\t")
		
	if int(ex[-1]) != 0 or ex[-1]=="NaN":
		cnt=cnt+1
		if extended!="":
			#ex[-1]=float(math.log(ex[-1]))
			extended=extended+","+str((ex[-1]))
		else:
			#ex[-1]=float(math.'''log(ex[-1]))
			extended=ex[-1]
				
		if kmer !="":
			kmer=kmer+","+str(i)
		else:
			kmer=str(i)	
	if cnt > 3:	
		s1,t1 = commands.getstatusoutput("Rscript "+cwd+"/Utils/RegressionKMerSelection.R "+kmer+" "+extended)
		temp=((t1.split("\n"))[-1]).split(" ");
		f.write(str(i)+"	"+str(temp[-1])+"	"+str(ex[-1])+"\n");
		if temp[-1].strip() != "NaN":		
			if float(temp[-1].strip()) > threshold:
				print "Threshold reached"
				print "Stopped at k-mer = "+str(int(i))
				os.system("mv "+output+"/Cluster/Combined/combine_p.fa "+output+"/transcripts.fa")
				break
			#else:
			#	pval=float(temp[-1].strip())
	else:
		f.write(str(i)+"	0"+"	"+str(ex[-1])+"\n")
	i=i+int(cl1.ss)

os.system("mv "+output+"/Cluster/Combined/combine_clust.fa "+output+"/transcripts.fa")
	
