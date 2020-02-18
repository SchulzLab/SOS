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
libtype = config["libtype"]
readlength=config["readlength"]

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
		expand(outdir+"read_{number}."+readformat, number={1,2}) if interleaved else [],
		expand(outdir+"{reads}_corrected.fa",reads=READFILENAME),
		expand(outdir+"Normalized_{number}.fa", number={1,2}) if len(INPUT)>1 else expand(outdir+"Normalized.fa"),
		expand(outdir+"configKreation.txt"),
		expand(outdir+"Assembly/Final/p_value.txt"),
		expand(outdir+"Quantification/transcript_quant.sf")

rule preprocess:
	input:
		expand("{reads}",reads=INPUT)
	output:
		expand(outdir+"/read_{number}."+readformat, number={1,2}) if interleaved else [],
		expand(outdir+"LogFiles/")
	priority:
		1
	message:
		"Executing preprocess"		
	run:
		if interleaved:
			shell("perl scripts/deinterleave.pl {input} "+outdir+" "+readformat)

rule error_correction:
	input:
		rules.preprocess.output	if interleaved else expand("{reads}",reads=INPUT)	
	output:
		expand(outdir+"{reads}_corrected.fa",reads=READFILENAME)
	params:
		tmp={tmpdir}
	priority:
		2
	message:
		"Executing error correction for the pipeline"
	benchmark:
       		outdir+"correction.txt"
	run:
		shell("mkdir "+outdir+"LogFiles/")
		shell("run_seecer.sh -k {skmer} -t {params.tmp} -c {bindir} -j {jellyfish} {INPUT} &> "+outdir+"LogFiles/LogCorrection.txt")
		for i in INPUT:
			if(os.path.dirname(i+"_corrected.fa")!=outdir):
				shell("mv "+i+"_corrected.fa {outdir}")
			shell("rm -r "+i+"_N")
		shell("rm -r {params.tmp}")

if norm:
	rule read_normalization:
		input:
			expand(outdir+"{reads}_corrected.fa",reads=READFILENAME)
		output:
			expand(outdir+"Normalized_{number}.fa", number={1,2}) if len(INPUT)>1 else expand(outdir+"Normalized.fa") 
		params:
			bs={base},
			kmr={kmer}
		message:
			"Executing normalization"
		priority:
			3
		benchmark:
        		outdir+"Normalization.txt"
		run:
			if(len(INPUT)>1):
				shell("ORNA -pair1 {input[0]} -pair2 {input[1]} -kmer {kmer} -base {base} -output "+outdir+"Normalized &> "+outdir+"LogFiles/LogNormalization.txt")
			else:
				shell("ORNA -input {input[0]} -kmer {kmer} -base {base} -output Normalized &> "+outdir+"/LogFiles/LogNormalization.txt")
				shell("mv Normalized.fa {output}")
					
rule createConfigforKREATION:
	input:
		cf="config.yaml", 
		inf=rules.read_normalization.output if norm else (expand(outdir+"{reads}_corrected.fa",reads=READFILENAME))
		
	output:
		outdir+"configKreation.txt"
	message:
		"Creating config file for KREATION"
	params:
		"paired" if type=="paired" else "single"
	run:
		shell("python scripts/configFileGenerator.py {input.cf} {output} {params} {input.inf[0]},{input.inf[1]}")	
		
rule runAssemblerWithKREATION:
	input:
		cf=outdir+"configKreation.txt"
	output:
		pvalue = outdir+"Assembly/Final/p_value.txt",
		transcripts = outdir+"Assembly/Final/transcripts.fa"
	message:
		"running KREATION with"+config["kpname"]
	params:
		rl=readlength,
		threshold = config["kthreshold"],
		output = outdir+"Assembly/"
	run:
		shell("python2 scripts/KREATION/KREATION.py -c {input.cf} -s 2 -r {params.rl} -t {params.threshold} -o {params.output}"),
		shell("mv {params.output}/Cluster/Combined/combined_clust.fa {output.transcripts}")

rule runSalmon:
	input:
		inputf=expand(outdir+"{reads}_corrected.fa",reads=READFILENAME),
		transcripts = outdir+"Assembly/Final/transcripts.fa"
	output:
		outdir+"Quantification/transcript_quant.sf"
	message:
		"Running salmon index generation and quantification"
	params:
		ltype = libtype,
		k = {kmer},
		output=outdir+"Assembly/"
	run:
		shell("salmon index -t {input.transcripts} -i "+outdir+"/Index -k {params.k}")
		if(len(INPUT)>1):
			shell("salmon quant -i "+outdir+"/Index -l {params.ltype} -1 {input[0]} -2 {input[1]} -o "+outdir+"Quantification")
		else:
			shell("salmon quant -i "+outdir+"/Index -l {params.ltype} -r {input[0]} -o "+outdir+"Quantification/"),
		shell("mv "+outdir+"Quantification/quant.sf "+outdir+"Quantification/transcript_quant.sf")	

