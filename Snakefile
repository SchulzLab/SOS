import os

configfile: "config/config.yaml"
norm=config["General"]["normalization"]
jellyfish="third_party/seecer/jellyfish-1.1.11/bin/jellyfish"
bindir = "third_party/seecer/SEECER/bin"

kmer=config["General"]["kmer"]
skmer=config["ErrorCorrection"]["seecerkmer"]
base=config["Normalization"]["ornabase"]
outdir=config["General"]["outdir"]
type = config["Reads"]["type"]
interleaved = config["Reads"]["interleaved"]
deinterleave = False
libtype = config["Quantification"]["libtype"]
readlength=config["Reads"]["readlength"]

INPUT=config["General"]["input"].split(",")
readformat = INPUT[0].split(".")[-1]

os.makedirs(outdir+"/LogFiles/", exist_ok=True)

if(readformat.upper()=="FASTA" or readformat.upper()=="FA"):
	readformat="fa"
else:
	readformat="fq"

if interleaved:
	READFILENAME=["read_1."+readformat, "read_2."+readformat]
else:
	READFILENAME=[path.split('/')[-1] for path in INPUT]	

if config["Assembly"]["kpname"]=="SOAPdenovo-Trans-31mer all" or config["Assembly"]["kpname"]=="SOAPdenovo-Trans-127mer all":
	config["Assembly"]["kpname"]="soapdenovo-trans"

rule all:
	input:
		expand(outdir+"/read_{number}."+readformat, number={1,2}) if interleaved else [],
		expand(outdir+"/ErrorCorrected/{reads}_corrected.fa",reads=READFILENAME),
		#expand(outdir+"/Normalized/Normalized_{number}.fa", number={1,2}) if len(INPUT)>1 else expand(outdir+"/Normalized.fa"),
		expand(outdir+"/configKreation.txt"),
		expand(outdir+"/Assembly/Final/p_value.txt"),
		expand(outdir+"/Quantification/Quant/quant.sf")

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
		expand(outdir+"/ErrorCorrected/{reads}_corrected.fa",reads=READFILENAME)
	priority:
		2
	message:
		"Executing error correction for the pipeline"
	benchmark:
       		outdir+"/LogFiles/TimeCorrection.txt"
	conda: f"config/conda/seecer.yaml"
	shell:
		"""
		third_party/seecer/SEECER/bin/run_seecer.sh -k {skmer} -t {outdir}/seecer_tmp -c {bindir} -o {outdir}/ErrorCorrected/ {INPUT} &> {outdir}/LogFiles/LogCorrection.txt
		"""

if norm:
	rule read_normalization:
		input:
			expand(outdir+"/ErrorCorrected/{reads}_corrected.fa",reads=READFILENAME)
		output:
			expand(outdir+"/Normalized/Normalized_{number}.fa", number={1,2}) if len(INPUT)>1 else expand(outdir+"/{reads}_Normalized.fa", reads=READFILENAME) 
		params:
			bs={base},
			kmr={kmer},
			linput = 2 if len(INPUT)>1 else 1
		message:
			"Executing normalization"
		conda: f"config/conda/orna.yaml"
		benchmark:
        		outdir+"/LogFiles/TimeNormalization.txt"
		shell:
			"""
			size={params.linput}
			if (((($size)) == 1))
			then
				ORNA -input {input[0]} -kmer {kmer} -base {base} -type fa -output {outdir}/Normalized &> {outdir}/LogFiles/LogNormalization.txt
				mv {outdir}/Normalized.fa {output}
			else
				ORNA -pair1 {input[0]} -pair2 {input[1]} -kmer {kmer} -base {base} -output {outdir}/Normalized/Normalized &> {outdir}/LogFiles/LogNormalization.txt			
			fi
			#rm -r *.h5
			"""
					
rule createConfigforKREATION:
	input:
		cf="config/config.yaml", 
		inf=rules.read_normalization.output if norm else (expand(outdir+"/ErrorCorrected/{reads}_corrected.fa",reads=READFILENAME))
	output:
		outdir+"/configKreation.txt"
	message:
		"Creating config file for KREATION"
	params:
		"paired" if type=="paired" else "single"
	shell:
		"""
		python scripts/configFileGenerator.py {input.cf} {output} {params} {input.inf}
		"""	
		
rule runAssemblerWithKREATION:
	input:
		cf=outdir+"/configKreation.txt"
	output:
		pvalue = outdir+"/Assembly/Final/p_value.txt",
		transcripts = outdir+"/Assembly/Final/transcripts.fa"
	message:
		"running KREATION with"+config["Assembly"]["kpname"]
	params:
		rl=readlength,
		threshold = config["Assembly"]["kthreshold"],
		output = outdir+"/Assembly/"
	conda: f"config/conda/"+config["Assembly"]["kpname"]+".yaml"
	shell:
		"""
		python third_party/KREATION/KREATION.py -c {input.cf} -s 2 -r {params.rl} -t {params.threshold} -o {params.output} &> {outdir}/LogFiles/LogAssembly.txt
		mv {params.output}/Cluster/Combined/combined_clust.fa {output.transcripts}
		rm -r {outdir}/Assembly/transcripts.fa
		"""

rule runSalmon:
	input:
		inputf=expand(outdir+"/ErrorCorrected/{reads}_corrected.fa",reads=READFILENAME),
		transcripts = outdir+"/Assembly/Final/transcripts.fa"
	output:
		outdir+"/Quantification/Quant/quant.sf"
	message:
		"Running salmon index generation and quantification"
	params:
		ltype = libtype,
		k = {kmer},
		linput = 2 if len(INPUT)>1 else 1,
		output=outdir+"/Quantification/",
	conda: 
		f"config/conda/Quantification.yaml"
	shell:
		"""
		salmon index -t {input.transcripts} -i {params.output}/Index -k {params.k} &> {outdir}/LogFiles/LogQuantificationIndex.txt
		size={params.linput}
		if (((($size)) == 2))
		then
			salmon quant -i {params.output}/Index -l {params.ltype} -1 {input[0]} -2 {input[1]} -o {params.output}/Quant &> {outdir}/LogFiles/LogQuantificationQuant.txt
		else
			salmon quant -i {params.output}/Index -l {params.ltype} -r {input[0]} -o {params.output}/Quant &> {outdir}/LogFiles/LogQuantificationQuant.txt
		fi 	
		"""
