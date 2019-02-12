#!/usr/bin/perl

use strict;
use warnings;

# Note -- $ARGV[0] is the first argument to the script, *not* the script itself
# (*not* like C's argv[0])
my $network_name=$ARGV[0];
my $param_batch_size=$ARGV[1];
my $comparison_config=$ARGV[2];
my $NN_DATAFLOW_PATH=$ENV{'NN_DATAFLOW_PATH'};
my $op_directory="ops";
my $results="results";
system("mkdir -p ./$op_directory");
system("mkdir -p ./$results");
my @word_size=(8);
my @batch_size=($param_batch_size);
my @config_range=("Baseline", $comparison_config); # Always compare vs. Baseline
foreach my $word (@word_size){
	foreach my $batch (@batch_size){
		my $schedule_name=$network_name."_".$word."_".$batch;
		my $Operations_file_name=$network_name."_".$word."_".$batch."_Ops.pl";
		my $multipliers_file_name=$network_name."_multipliers.pl";
#		my $iter=0;
#		foreach my $config (@config_range){	
#			my $schedule_directory="$NN_DATAFLOW_PATH/mod_schedule/$config";
#			system("./Extract_operations.pl $schedule_directory/$schedule_name ./$op_directory/$Operations_file_name $network_type $iter");
#			$iter=$iter+1;
#                }
        # TODO unify $op_file_name with $comparison_config as we pass to Acc_results_compare_trace.pl
		my $op_file_name=$network_name."_".$word."_".$batch."_".$comparison_config.".csv";
		system("./Acc_results_compare_trace.pl ./$network_name ./$op_directory/$Operations_file_name $word $batch $op_file_name ./config/multipliers/$multipliers_file_name $comparison_config");
	}
}
