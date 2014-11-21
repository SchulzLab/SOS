import sys
import os
import optparse
from optparse import OptionParser
from optparse import Option, OptionValueError

class sequence_cleaner():
	def __init__(self, input_file, t):
		x = input_file.split(".")
		if (x[-1].upper() == "FASTA" or x[-1].upper() == "FA"):
			self.file_clean(input_file, t)
		elif (x[-1].upper() == "FASTQ" or x[-1].upper() == "FQ"):
			self.file_clean(input_file, t)
		else:
			print "The file is in unknown format"
			
	def file_clean(self, input_file, t):
		f = open(input_file)
		lines = f.readlines()
		co = 0
		inpf = input_file.split("/")
		temp_file = inpf[-1]
		temp_file = temp_file.replace(".", "_")
		l_seq = len(lines[1]) - 1
		int_file = temp_file+".fa"
		cmd = "jellyfish count -m " + str(l_seq)+ " -s 100M -t 10 -C " + input_file+ " -o " + temp_file + ".jf"
		cmd_1 = "jellyfish dump "+ temp_file+".jf > "+ temp_file+".fa"
		os.system(cmd)
		os.system(cmd_1)
		int_temp = int_file.replace(".fa", "_cleared.fa")
		t_file = open(int_file, "r")
		t_file1 = open(int_temp, "w")
		t_file1.close()
		t_file1 = open(int_temp, "a")
		line = t_file.readlines()
		id = 0		
		for i in range(0, len(line)):
			if ">" in line[i]:
				seq_id = line[i]
				seq = line[i+1]
				line[i] = line[i].replace(">", "")		
				num = int(line[i])
				if(num > t):
					for i in range(0, t):
						t_file1.write(">" +str(id)+"\n")
						t_file1.write(seq)
						id = id + 1
				else:
					for i1 in range(0, num):
						t_file1.write(">" +str(id)+"\n")
						t_file1.write(line[i+1])
						id = id + 1
		t_file.close()
		t_file1.close()

class options():		
	def getoptions(self):
		parser = OptionParser()
		parser.add_option('-t', '--threshold',dest='threshold',help='Threshold value',metavar='NAME', action="store")
		parser.add_option('-i', '--input',dest='inputname',help='Input file',metavar='INPUT', action="store")

		(options, args) = parser.parse_args()
		return options
		
y1 = options()
opt = y1.getoptions()		
		
y = sequence_cleaner(opt.inputname, int(opt.threshold))
