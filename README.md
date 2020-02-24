## About
De novo transcriptome assembly of RNA-Seq data is an important problem. Studies of novel model organisms with a poorly annotated reference sequence can make use of different tools that have been proposed for de-novo transcriptome assembly. While successful, current tools rarely represent integrated solutions that can cope with large and diverse data sets. SOS pipeline is an integrated solution for the transcriptome assembly consisting of read error correction, read filtering, multi-k parameter optimized de-novo transcriptome assembly and transcript level expression estimates. SOS has the following workflow:
### Error correction: 
The input reads are first error corrected using SEECER. We use a modified version of seecer which can be downloaded via https://zenodo.org/record/3686150

### Read normalization:
SOS normalizes the dataset using ORNA which can be downloaded and installed via https://github.com/SchulzLab/ORNA. This step is optional. We advise the users to skip this step if the coverage of the dataset is low, i.e. if there is not a problem with runtime/memory consumption of the assembly process. For datasets> 100 million reads, normalization is recommended.

### Transcriptome assembly:
The pipeline is flexible and can incorporate any transcriptome assembler by changing a few lines of codes (details given below). We tested SOS on four different assemblers namely:

* TransABySS
* SOAPdenovo-Trans
* TransLiG
* Oases 

Note: SOS generates multiple assemblies using multiple kmer sizes and merges them to form a single non-redundant assembly. The lower kmer size is by default set to one-third of the read length and the higher kmer size of the range is decided using the KREATION tool. Hence, if oases is selected for assembly, then the modified version of the assembler (provided with KREATION script) should be used. 

### Transcript level expression estimates:
The pipeline uses salmon for transcript level expression estimation, which can be downloaded and installed via https://github.com/COMBINE-lab/salmon. 


## Running SOS:

### Requirements
Basic skeleton of SOS requires:

1.	64-bit linux operating system. 
2.	A physical memory of 12 GB or higher is recommended (more is always better!)
3.	[Jellyfish](http://www.cbcb.umd.edu/software/jellyfish/) version 2.0  
4.	GNU Scientific Library (SEECER)
5.      Any version of [g++](gcc.gnu.org) >= 4.7 (ORNA and Salmon)
6.	cd-hit-est (required for KREATION)

Note: Requirements may change depending upon the assembler used in the pipeline

### Download:
The pipeline can be downloaded using the following command:

    git clone https://github.com/SchulzLab/SOS

The downloaded folder should have the following files:

* Snakemake file
* Sample config file for snakemake: config.yaml
* install_script.py	
* A folder consisting of sample data
* A folder consisting of supporting scripts

### Installation

1.	After downloading the SOS distribution, change into the directory
		cd SOS	
2.	Download the SEECER tar file from the provided link and unwrap it into the current folder
	```
		tar -zxvf SEECER.tar.gz
	```
3.	Optional: Run the python script install_script.py to install the softwares (OASES, KREATION, ORNA and SALMON)
	```
		python install_script.py -f <destination_folder>
	```
	This should install OASES, ORNA and SALMON and KREATION in the provided destination folder. Additional assembly algorithms should be downloaded and installed seperately.
	
4.	Set the following paths in the environment variable $PATH:
	```
		export PATH=$PATH:path_to_seecer_bin
		export PATH=$PATH:path_to_orna_bin_folder 
		export PATH=$PATH:path_to_assembler_executable
		export PATH=$PATH:path_to_kreation_folder
		export PATH=$PATH:path_to_cd-hit_est
		export PATH=$PATH:path_to_salmon
	```

## Config file
The config.txt should have the following configuration
```
#General Parameters
input: input_files //Two comma seperated files if input is paired end data
outdir: Output directory to store the results 
kmer: kmer to be used for error correction, normalization and assembly

#Read Characteristics
type: single or paired 
readlength: 101  
inslength: 200

#Seecer Parameters (See seecer manual for more details)
seecertmp: path to temp folder for seecer intermediate files
jellyfish: path to jellyfish
scriptsfolder: path to the scripts folder of seecer
seecerdir: path to the bin folder of seecer
seecerkmer: a seecer kmer if different than the kmer from general parameters

#ORNA parameters
ornabase: Base parameter of ORNA (set to 1.7 by default)

#KREATION Parameters (See KREATION manual for more details)
kstep: step size for kmer parameter of KREATION (set to 2 by default)
kthreshold: Threshold parameter of seecer (set to 0.01 by default)
kpname: Assembly algorithm to be used with KREATION (Current supported assemblers: Oases, TransABySS, TransLiG and SOAPdenovotrans)
kpadditional: Additional commands to be used with KREATION

#Salmon Parameters
libtype: library type
```


## Usage
The pipeline can be run using the following command from the SOS folder:
```
	snakemake all
```

###### Output Folder
The output folder will have a folders generated by KREATION runs namely - Assembly, Cluster and Final(containing the final assembly result). Additionally, the output folder would have four more folders namely: 
1.	CorrectedReads which contains the error corrected reads.
2.	NormalizedReads which contains the normalized reads from ORNA. 
3.	Index which contains index files used by Salmon. 
4.	Quant file which contains results from expression estimation for assembled transcripts.

##### Contact
For questions or suggestions regarding SOS please contact

* Dilip A Durai (ddurai_at_contact.mmci.uni-saarland.de)
* Marcel H Schulz (mschulz_at_mmci.uni-saarland.de)


##### Version
Version 0.2

