import sys
import os
import optparse
from optparse import OptionParser
from optparse import Option, OptionValueError
from Bio import SeqIO
import random

class sequence_cleaner():
	def __init__(self, input_file, t,output,per):
		x = input_file.split(".")
		if (x[-1].upper() == "FASTA" or x[-1].upper() == "FA"):
			self.file_clean(input_file, t,output,"FA",per)
		elif (x[-1].upper() == "FASTQ" or x[-1].upper() == "FQ"):
			self.file_clean(input_file, t,output,"FQ",per)
		else:
			print "The file is in unknown format"
			
	def get_length(self, inp_file, format):
		if (format == "FASTA"):
			handle = open(inp_file, "rU")
			for record in SeqIO.parse(handle, "fasta") :
				length = len(record.seq)
				seq = str(record.seq)
				break
		else:
			handle = open(inp_file, "rU")
			for record in SeqIO.parse(handle, "fastq") :
				length = len(record.seq)
				seq = str(record.seq)
				break	
		return length
		
			
	def file_clean(self,input_file,t,output,format,per):
		f = open(input_file)
		co = 0
		inpf = input_file.split("/")
		temp_file = inpf[-1]
		temp_file = temp_file.replace(".", "_")
		
		if (format == "FA"):
			l_seq = self.get_length(input_file, "FASTA")
		else:
			l_seq = self.get_length(input_file, "FASTQ") 

		int_file = output+"/"+temp_file+".fa"
		cmd = "jellyfish count -m " + str(l_seq)+ " -s 1000M -t 50 -C " + input_file+ " -o " + output+"/"+temp_file + ".jf"
		cmd_1 = "jellyfish dump "+ output+"/"+temp_file+".jf > "+ output+"/"+temp_file+".fa"
		os.system(cmd)
		os.system(cmd_1)
		int_temp = int_file.replace(".fa", "_cleared.fa")
		t_file = open(int_file, "r")
		t_file1 = open(int_temp, "w")
		t_file1.close()
		t_file1 = open(int_temp, "a")
		#line = t_file.readlines()
		id = 0		
		#for i in range(0, len(line)):
		while True:
			line_1 = t_file.readline()
			line_2 = t_file.readline()
			if (not line_1) or (not line_2):
				break
			if ">" in line_1:
				seq_id = line_1
				seq = line_2
				line_1 = line_1.replace(">", "")		
				num = int(line_1)
				p = float(per)
				if(num > t):
					p = float(per)
					if(p>1):
						p=float(p/100)
					mul_res = num * p
					new_t = int(round(max(t, mul_res))) 
					for i in range(0, new_t):
						t_file1.write(">" +str(id)+"\n")
						t_file1.write(seq)
						id = id + 1
				else:
					for i1 in range(0, num):
						t_file1.write(">" +str(id)+"\n")
						t_file1.write(line_2)
						id = id + 1
		t_file.close()
		t_file1.close()

class options():		
	def getoptions(self):
		parser = OptionParser()
		parser.add_option('-t', '--threshold',dest='threshold',help='Threshold value',metavar='NAME', action="store")
		parser.add_option('-i', '--input',dest='inputname',help='Input file',metavar='INPUT', action="store")
		parser.add_option('-o', '--output',dest='output',help='Output Directory', action="store")
		parser.add_option('-p', '--per',dest='perc',help='Percentage', action="store")
		(options, args) = parser.parse_args()
		return options
		
y1 = options()
opt = y1.getoptions()		
		
y = sequence_cleaner(opt.inputname, int(opt.threshold), opt.output,opt.perc)
