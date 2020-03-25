## About
De novo transcriptome assembly of RNA-Seq data is an important problem. Studies of novel model organisms with a poorly annotated reference sequence can make use of different tools that have been proposed for de novo transcriptome assembly. While successful, current tools rarely represent integrated solutions that can cope with large and diverse data sets. The SOS pipeline is an integrated solution for the transcriptome assembly consisting of read error correction, read normalization, multi-k parameter optimized de novo transcriptome assembly and transcript level expression estimates. SOS has the following workflow 
![SOS flowchart](https://github.com/SchulzLab/SOS/blob/master/SOSflowchart.pdf)


1. **Error correction**: 
The input reads are first error corrected using SEECER. 

2. **Read normalization**:
SOS normalizes the dataset using ORNA [https://github.com/SchulzLab/ORNA]. 

3. **Transcriptome assembly**:
The pipeline is flexible and can incorporate any transcriptome assembler by changing a few lines of codes (details given below). We tested SOS on four different assemblers namely:

* TransABySS
* SOAPdenovo-Trans
* TransLiG
* Oases 

Note: SOS generates multiple assemblies using multiple kmer sizes and merges them to form a single non-redundant assembly. The lower kmer size is by default set to one-third of the read length and the higher kmer size of the range is decided using the KREATION tool. Hence, if Oases is selected for assembly, then the modified version of the assembler (provided with the KREATION script) should be used. 

4. **Transcript level expression estimates**:
The pipeline uses Salmon for transcript level expression estimation, which can be downloaded and installed via https://github.com/COMBINE-lab/salmon. 


## Running SOS:

### Requirements
Basic skeleton of SOS requires:

1.	Python >= version 3.1 
2.	64-bit linux operating system. 
2.	A physical memory of 12 GB or higher is recommended (more is always better!)
3.	GNU Scientific Library (SEECER)
4.      Any version of [g++](gcc.gnu.org) >= 4.7 (ORNA and Salmon)
5.	zlib (ORNA)
6.	cd-hit-est (required for KREATION)

Note: Requirements may change depending upon the assembler used in the pipeline

### Download:
The pipeline can be downloaded using the following command:

    git clone https://github.com/SchulzLab/SOS

The downloaded folder should have the following files:

* Snakemake file
* Sample config file for snakemake
* install_script.py	
* A folder consisting of sample data
* A folder consisting of supporting scripts

### Installation

1.	After downloading the SOS distribution, change into the directory
```
		cd SOS	
```
2.	Optional: Run the python script install_script.py to install the softwares (OASES, KREATION, ORNA and SALMON)
	```
		python install_script.py -f <destination_folder>
	```
	This can install OASES, ORNA, SEECER and SALMON and KREATION in the provided destination folder. Additional assembly algorithms should be downloaded and installed seperately. SOS installs SEECER using a precompiled version that was prepared for the SOS repository specifically (accessible under https://zenodo.org/record/3686150).
	
3.	Set the following paths in the environment variable $PATH:
	```
		export PATH=$PATH:path_to_seecer_bin
		export PATH=$PATH:path_to_orna_bin_folder 
		export PATH=$PATH:path_to_assembler_executable
		export PATH=$PATH:path_to_kreation_folder
		export PATH=$PATH:path_to_cd-hit_est
		export PATH=$PATH:path_to_salmon
	```

## Config file
The config.txt has the following configuration
```
## Config file for the execution of SOS. All parameters are required unless otherwise stated
##For more information about the parameters, please refer to the manual/readme files of the individual algorithm

#General Parameters
input: path to read files. Multiple files should be combined into one file
outdir: path to the output directory
kmer: kmer to be used for normalization, assembly and quantification
normalization: false if you want to skip the normalization step. otherwise true

#Read Specific parameters
type: paired/single 
interleaved: true/false (required if the input is paired end)
readlength: length of the reads given as input.  
inslength: insert-length if the data is paired end (required if the input is paired end)

#Seecer Parameters
seecertmp: tmp folder required for SEECER
jellyfish: path to jellyfish executable
binfolder: path to SEECER bin folder
seecerkmer: kmer used for error correction

#ORNA parameters
ornabase: logarithm base for calculating the kmer abundance threshold in ORNA

#KREATION Parameters
kstep: step size required for KREATION execution
kthreshold: d_score cutoff for KREATION
kpname: assembler executable name 
kpadditional: 

#Salmon Parameters
libtype: library type for the reads given as input to salmon

```

### Config file parameters

**General Parameters**



parameter | value | explanation 
-----------|--------------|---------
input | /path/to/readfile | Absolute path of the input read fasta/q file. If the data is paired end, then they should either be interleaved together to form a single file or given as two comma separated filenames. Multiple files of singl-end reads should be combined together to form one file. Please avoid using symbols such as ~ in the file path. 
outdir | /path/to/output | Absolute path to the output directory. The folder will be created if not present.
kmer | numeric (default 1/3 of read length) | kmer size to be used for read normalization, transcript assembly and quantification. We suggest a kmer size equivalent to 1/3rd of the read length. 
normalization | true/false | Indicates whether ORNA should be run on the datasets. We suggest to include normalization step for large datasets(>200M reads) 

**Read specific parameters**
	
parameter | value | explanation 
-----------|--------------|---------
type | single/paired |  Denotes whether single-end or paired-end reads are used.
interleaved | true/false | This parameter is required if the input data is paired-end. Some assemblers do not accept interleaved paired-end files. Hence, such files will be separated into two individual files representing the pairs.
readlength | numeric | Length of the reads. If reads have different sizes then the length of the longest read in the dataset needs to be provided.
ins-length | numeric | Insert size for paired end data.

**SEECER specific parameters**

parameter | value | explanation 
-----------|--------------|---------
seecertmp | foldername | Temporary folder to store intermediate files generated from SEECER. The folder would be deleted after the completion of the error correction step.
jellyfish | /path/to/jellyfish | Absolute path to the jellyfish library. SEECER uses jellyfish to count kmers and build a consensus sequence. 
binfolder | /path/to/SEECER | Absolute path to SEECER bin folder.
seecerkmer | numeric | kmer size to be used for error correction. 

**ORNA parameters**

parameter | value | explanation 
-----------|--------------|---------
ornabase | numeric (default 1.7) | The base of the log function, which is used by ORNA for calculating the threshold for each kmer in the dataset. Refer to the manual of ORNA for more details. For good average performance we suggest a value of 1.7.

**KREATION parameters**

parameter | value | explanation 
-----------|--------------|---------
kstep | numeric | kmer increment size to be used by KREATION. For instance, if the kstep=2 and the value of kmer=17, then assemblies would be generated for k=17,19,21... till an optimal assembly is reached. For more details refer to KREATION manual.
kthreshold | numeric | d_score threshold be used by KREATION. For more details, refer to KREATION manual.
kpname | executableName | Name of the assembler to be used. Please note that the name should match the assembler executable file.
kpadditonal | parameter string | Additional assembler parameters to be used. This can vary depending on the assembler used. 

**salmon parameters**

parameter | value | explanation 
-----------|--------------|---------
libtype | salmon libtypes | Type of the sequencing library from which the reads originate. For more details, please refer to salmon manual. 


## Usage
The pipeline can be run using the following command from the SOS folder:
```
	snakemake all
```

## Output Folder
The output folder will have a folders generated by KREATION runs namely - *Assembly*, *Cluster* and *Final* (containing the final assembly result). Additionally, the output folder would have four more folders namely: 
1.	CorrectedReads: This folder contains the error corrected reads (As readname_corrected.fa). The output produced is always in fasta format. Please note that the tmp file produced by SEECER is deleted by SOS.

2.	NormalizedReads: This folder consists of ORNA normalized reads (as Normalized_\*.fa). The format of the output file is same as the input format. Since, error coorected reads are always in fasta format, the output produced by the normalization algorithm is always in fasta format.   

3.	Assembly: The assembly results generated are transferred to this folder (as transcripts.fa). The output file consists of contigs generated by the assembler. KREATION changes the header of the sequence to identify which kmer iteration produced the sequence. Hence, the header of the sequences in the final assembly file is as follows:
```
	>k_transcript_id
```
where k is the kmer size which was used to generate the sequence.
Additional, the assembly folder would also contain intermediate sub-folders created by Kreation namely:

	* Intermediate: Contains intermediate assembly generated after each kmer iteration
	* Cluster: Contains sequence clusters generated after every kmer iteration
	* Final: Contains a log file reporting the d_score after every kmer iteration.

Please refer to Kreation manual/manuscript for more details.

4.	Index: Generated by Salmon for sorting the index files. 
5.	Quant: Generated by Salmon and contains the expression estimates from the assembly (in file quant.sf).

###
### Contact
For questions or suggestions regarding SOS please contact

* Dilip A Durai (ddurai_at_contact.mmci.uni-saarland.de)
* Marcel H Schulz (marcel.schulz_at_em.uni-frankfurt.de)

## FAQ

1. When should I use read normalization with ORNA?

We advise the users to skip this step if the coverage of the dataset is low, i.e. if there is not a problem with runtime/memory consumption of the assembly process. For datasets> 100 million reads, normalization is recommended.

2. Can I run SOS on multiple input files?

Yes, SOS can be run on multiple input files. If there are multiple input files generated from the same study/experiment, the user have to concatenate the read file to form a single fasta(q) file. 

If the multiple inut files belong to different study/experiment, then the user has to make separate config file for each input read file. The user also has to provide a different output folder for each input file. The pipeline can then be run using the following command:
```
snakemake --configfile path_to_the_new_config_file all
``` 
