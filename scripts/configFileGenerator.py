import sys
import os
cfile=sys.argv[1]
ofile=sys.argv[2]
typ = sys.argv[3]
ins=200

dirname=os.path.dirname(ofile)
print(dirname)
krt=dict()
fl=open(cfile,"r")

flg=0
for line in fl:
	para=(line.rstrip()).split(":")
	if(len(para)!=0):
		if(para[0]=="input"):
			infile=(para[1].strip()).rstrip()
		if(para[0]=="kmer"):
			kmer=(para[1].strip()).rstrip()
		if(para[0]=="readlength"):
			rl=(para[1].strip()).rstrip()
		if(para[0]=="configuration"):
			if(len(para)>1):
				krt[para[0]] = (para[1].strip())
			else:
				krt[para[0]] = "fr"
		if(para[0]=="inslength"):
			ins=int((para[1].strip()).rstrip())
		if(para[0]=="#KREATION Parameters"):
			flg=1
		if(para[0]=="#Salmon Parameters"):
			flg=0
		if(flg==1 and para[0]!="#KREATION Parameters"):
			if(len(para)>1):
				krt[para[0]] = (para[1].strip())
			else:
				krt[para[0]] = ""


files=infile.split(",")
frmt = files[0].split(".")[-1]
if(frmt.upper()=="FASTA" or frmt.upper()=="FA"):
	frmt="fa"
else:
	frmt="fq"


f=open(ofile, "a")
f.write("#Program Name"+"\n")
f.write(krt["kpname"]+"\n")
f.write("#Output file name"+"\n")
if(krt["kpname"]=="oases_pipeline_2.py"):
	f.write("transcripts.fa"+"\n")
	f.write("#minimum K"+"\n")
	f.write("-m "+str(kmer)+"\n")
	f.write("#Rest of the command"+"\n")
	if(typ.upper()=="PAIRED"):
		f.write("-d \"-shortPaired "+files[0]+" "+files[1]+"\" -p \"-ins_length "+str(ins)+" "+krt["kpadditional"]+"\"\n")
	else:
		f.write("-d \""+infile+"\" "+krt["kpadditional"]+"\n")
elif(krt["kpname"]=="transabyss"):
	f.write("transabyss-final.fa"+"\n")
	f.write("#minimum K"+"\n")
	f.write("-k "+str(kmer)+"\n")
	f.write("#Rest of the command"+"\n")
	if(typ.upper()=="PAIRED"):
		f.write("--pe "+files[0]+" "+files[1]+" --length 100 "+krt["kpadditional"]+"\n")
	else:
		f.write("--se "+infile+" --length 100 "+krt["kpadditional"]+"\n")
elif(krt["kpname"]=="TransLiG"):
	f.write("TransLiG.fa"+"\n")
	f.write("#minimum K"+"\n")
	f.write("-k "+str(kmer)+"\n")
	f.write("#Rest of the command"+"\n")
	if(typ.upper()=="PAIRED"):
		f.write("-p pair -l "+files[0]+" -r "+files[1]+" -t 100 -s "+frmt+" "+krt["kpadditional"]+"\n")
	else:
		f.write("-p single -u "+infile+" -t 100 -s "+frmt+" "+krt["kpadditional"]+"\n")
elif(krt["kpname"]=="rnaspades.py"):
	f.write("hard_filtered_transcripts.fasta"+"\n")
	f.write("#minimum K"+"\n")
	f.write("-k "+str(kmer)+"\n")
	f.write("#Rest of the command"+"\n")
	if(typ.upper()=="PAIRED"):
		if(krt["configuration"]=="rf"):
			f.write("-1 "+files[0]+" -2 "+files[1]+" -ss-rf "+krt["kpadditional"]+"\n")
		else:
			f.write("-1 "+files[0]+" -2 "+files[1]+" -ss-fr "+krt["kpadditional"]+"\n")
	else:
		f.write("-s "+infile+" "+krt["kpadditional"]+"\n")		
elif(krt["kpname"]=="SOAPdenovo-Trans-127mer all" or krt["kpname"]=="SOAPdenovo-Trans-31mer all"):
	f1=open(dirname+"/configSOAP.txt","a")	
	f1.write("max_rd_len="+str(rl)+"\n")
	f1.write("[LIB]"+"\n")
	f1.write("asm_flags=3"+"\n")
	if(typ.upper()=="PAIRED"):
		if(krt["configuration"]=="rf"):
			f1.write("reverse_seq=1"+"\n")
		else:
			f1.write("reverse_seq=0"+"\n")
		f1.write("avg_ins="+str(ins)+"\n")
		if(len(files)==1):
			f1.write("p="+infile+"\n")
		else:
			if(frmt=="fq"):
				f1.write("q1="+files[0]+"\n")
				f1.write("q2="+files[1]+"\n")
			else:
				f1.write("f1="+files[0]+"\n")
				f1.write("f2="+files[1]+"\n")
	else:
		f1.write("#fasta file for single reads")
		f1.write("f="+infile)	
	f.write("transcripts.contig"+"\n")
	f.write("#minimum K"+"\n")
	f.write("-K "+str(kmer)+"\n")
	f.write("#Rest of the command"+"\n")
	f.write("-s "+dirname+"/configSOAP.txt"+" -o transcripts"+"\n")
else:
	print("Hello")
