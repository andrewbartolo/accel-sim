#!/usr/bin/perl
use strict;
use warnings;
use List::Util qw(first);
my $schedule_file=$ARGV[0];
my $opfile=$ARGV[1];
my $net_type=$ARGV[2];
my $arg_type=$ARGV[3];
my $array_index=0;
my @layer_names=();
my @num_ops=();
my @Keywords=("time","unit_size","access","to","cost","ti","tb","orders","size","part_lprev","part_lcurr","total_nhops","unit_nhops","part","total","unit");
my $checklayernames=0;
open my $file_pointer, '<', $schedule_file or die $!;
while (my $line= <$file_pointer>){
	if (index($line,"\"ops\"")>=0){
		 my ($num_ops_extracted)= $line=~ /([0-9]+)/;
		 $num_ops[$array_index]=$num_ops_extracted;
		 $array_index++;
	 }
	 elsif (index($line,"\"mappings\"")>=0){
		 $checklayernames=1;
	 }
	 elsif (index($line,"\"")>=0 && $checklayernames==1){
		 my($extracted_name)= $line=~/([a-zA-Z][a-zA-Z0-9_]+)/;
		 if(!first { $_ eq $extracted_name} @Keywords){
			 $layer_names[$array_index]=$extracted_name;
		 }
	 }
}
close ($file_pointer);

if($net_type>=2){
my $checklayernames=0;
open my $file_pointer, '<', $schedule_file."_2" or die $!;
while (my $line= <$file_pointer>){
	if (index($line,"\"ops\"")>=0){
		 my ($num_ops_extracted)= $line=~ /([0-9]+)/;
		 $num_ops[$array_index]=$num_ops_extracted;
		 $array_index++;
	 }
	 elsif (index($line,"\"mappings\"")>=0){
		 $checklayernames=1;
	 }
	 elsif (index($line,"\"")>=0 && $checklayernames==1){
		 my($extracted_name)= $line=~/([a-zA-Z][a-zA-Z0-9_]+)/;
		 if(!first { $_ eq $extracted_name} @Keywords){
			 $layer_names[$array_index]=$extracted_name;
		 }
	 }
}
close ($file_pointer);


if($net_type==3){
my $checklayernames=0;
open my $file_pointer, '<', $schedule_file."_1" or die $!;
while (my $line= <$file_pointer>){
	if (index($line,"\"ops\"")>=0){
		 my ($num_ops_extracted)= $line=~ /([0-9]+)/;
		 $num_ops[$array_index]=$num_ops_extracted;
		 $array_index++;
	 }
	 elsif (index($line,"\"mappings\"")>=0){
		 $checklayernames=1;
	 }
	 elsif (index($line,"\"")>=0 && $checklayernames==1){
		 my($extracted_name)= $line=~/([a-zA-Z][a-zA-Z0-9_]+)/;
		 if(!first { $_ eq $extracted_name} @Keywords){
			 $layer_names[$array_index]=$extracted_name;
		 }
	 }
}
close ($file_pointer);
}
}

if($arg_type==0){
	open $file_pointer, '>', $opfile or die $!;
	print $file_pointer "\% NNops =(\n";
	for (my $i=0;$i<$array_index;$i++){
		print $file_pointer $layer_names[$i],"=>",$num_ops[$i],",\n";
	}
	print $file_pointer ");\n1;\n";
	close ($file_pointer);
}else{
        open $file_pointer, '>>', $opfile or die $!;
	print $file_pointer "\% NNops$arg_type =(\n";
	for (my $i=0;$i<$array_index;$i++){
		print $file_pointer $layer_names[$i],"=>",$num_ops[$i],",\n";
	}
	print $file_pointer ");\n1;\n";
	close ($file_pointer);
}
