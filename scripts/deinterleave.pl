$filename = $ARGV[0];
$outdir = $ARGV[1];
$format = $ARGV[2];
$fn="read";
if((uc $format eq "FASTA") or (uc $format eq "FA")) 
{
	open(FP,$filename);	

	$output1=$outdir."/".$fn."_1.fa";
	$output2=$outdir."/".$fn."_2.fa";
	#$output1=~s/".fasta"/"_1.fa"/g;
	#$output2=~s/".fasta"/"_2.fa"/g;
	@sequences=split(">",join("",<FP>));
	open(FP1,">>$output1");
	open(FP2,">>$output2");
	for($i=1;$i<@sequences;$i++)
	{
		@var=split("\n",$sequences[$i]);
		if($i%2!=0)
		{
			print FP1 ">".$var[0]."/1\n";
			for($j=1;$j<@var;$j++)
			{
				print FP1 $var[$j],"\n"; 
			}
		}
		else
		{
			print FP2 ">".$var[0]."/2\n";
			for($j=1;$j<@var;$j++)
			{
				print FP2 $var[$j],"\n"; 
			}
		}
	}
}
else
{	
	$output1=$outdir."/".$fn."_1.fq";
	$output2=$outdir."/".$fn."_2.fq";
	open(FP,$filename);	
	@sequences=split("\@SRR",join("",<FP>));
	open(FP1,">>$output1");
	open(FP2,">>$output2");
	for($i=1;$i<@sequences;$i++)
	{
		@var=split("\n",$sequences[$i]);
		if($i%2!=0)
		{
			print FP1 "\@SRR".$var[0]."/1\n";
			for($j=1;$j<@var;$j++)
			{
				print FP1 $var[$j],"\n"; 
			}
		}
		else
		{
			print FP2 "\@SRR".$var[0]."/2\n";
			for($j=1;$j<@var;$j++)
			{
				print FP2 $var[$j],"\n"; 
			}
		}
	}
}
