import os

configfile: "config.yaml"
norm=config["normalization"]
jellyfish=config["jellyfish"]
bindir = config["seecerdir"]
tmpdir=config["seecertmp"]
kmer=config["kmer"]
skmer=config["seecerkmer"]
base=config["ornabase"]
outdir=config["outdir"]
type = config["type"]
interleaved = config["interleaved"]
deinterleave = False
cort = config["correction"]

INPUT=config["input"].split(",")
readformat = INPUT[0].split(".")[-1]

if(readformat.upper()=="FASTA" or readformat.upper()=="FA"):
	readformat="fa"
else:
	readformat="fq"

if interleaved:
	READFILENAME=["read_1."+readformat, "read_2."+readformat]
else:
	READFILENAME=[path.split('/')[-1] for path in INPUT]	

rule all:
	input:
		expand(outdir+"/read_{number}."+readformat, number={1,2}) if interleaved else [],
		expand(outdir+"/{reads}_corrected.fa",reads=READFILENAME) if cort else [],
		expand(outdir+"/Normalized_{number}.fa", number={1,2}) if len(INPUT)>1 else expand(outdir+"/Normalized.fa"),
		expand(outdir+"/configKreation.txt"),
		#expand(outdir+"Assembly/Final/p_value.txt")

rule preprocess:
	input:
		expand("{reads}",reads=INPUT)
	output:
		expand(outdir+"/read_{number}."+readformat, number={1,2}) if interleaved else []
	priority:
		1
	message:
		"Executing preprocess"		
	run:
		if interleaved:
			shell("perl scripts/deinterleave.pl {input} "+outdir+" "+readformat)

if cort:
	rule run_seecer:
		input:
			rules.preprocess.output	if interleaved else expand("{reads}",reads=INPUT)	
		output:
			expand(outdir+"/{reads}_corrected.fa",reads=READFILENAME)
		params:
			tmp={tmpdir}
		priority:
			2
		message:
			"Executing error correction for the pipeline"
		benchmark:
        		outdir+"/correction.txt"
		run:
			shell("mkdir "+outdir+"/LogFiles")
			shell("run_seecer.sh -k {skmer} -t {params.tmp} -c {bindir} -j {jellyfish} {input} &> "+outdir+"/LogFiles/LogCorrection.txt")
			for i in input:
				if(os.path.dirname(i+"_corrected.fa")!=outdir):
					shell("mv "+i+"_corrected.fa {outdir}")
				shell("rm -r "+i+"_N")
			shell("rm -r {params.tmp}")
if norm:
	rule read_normalization:
		input:
			expand(outdir+"/{reads}_corrected.fa",reads=READFILENAME) if cort else rules.preprocess.output
		output:
			expand(outdir+"/Normalized_{number}.fa", number={1,2}) if len(INPUT)>1 else expand(outdir+"/Normalized.fa") 
		params:
			bs={base},
			kmr={kmer}
		message:
			"Executing normalization"
		priority:
			3
		benchmark:
        		outdir+"/Normalization.txt"
		run:
			shell("mkdir "+outdir+"/LogFiles")
			if(len(INPUT)>1):
				shell("ORNA -pair1 {input[0]} -pair2 {input[1]} -kmer {kmer} -base {base} -output "+outdir+"/Normalized &> "+outdir+"/LogFiles/LogNormalization.txt")
				#shell("fastaq interleave Normalized_1.fa Normalized_2.fa {output}")
				#shell("mv Normalized_1.fa "+outdir+"/")
				#shell("mv  Normalized_2.fa "+outdir+"/")
			else:
				shell("ORNA -input {input[0]} -kmer {kmer} -base {base} -output Normalized &> "+outdir+"/LogFiles/LogNormalization.txt")
				shell("mv Normalized.fa {output}")
					
rule createConfig:
	input:
		cf="config.yaml", 
		inf=rules.read_normalization.output if norm else (expand(outdir+"/{reads}_corrected.fa",reads=READFILENAME) if cort else expand("{reads}",reads=INPUT))
		
	output:
		outdir+"/configKreation.txt"
	message:
		"Creating config file for KREATION"
	params:
		"paired" if type=="paired" else "single"
	run:
		shell("python scripts/configFileGenerator.py {input.inf} {input.cf} {output} {params}")	
		
rule runKREATION:
	input:
		cf=outdir+"/configKreation.txt"
	output:
		outdir+"Assembly/Final/p_value.txt"
	message:
		"running KREATION with"+config["kpname"]
	params:
		rl=config["kreadlength"],
		threshold = config["kthreshold"],
		output=outdir+"/Assembly/"
	run:
		shell("python2 scripts/KREATION/KREATION.py -c {input.cf} -s 2 -r {params.rl} -t {params.threshold} -o {params.output}")



