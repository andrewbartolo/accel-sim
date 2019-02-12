zsim_path=$ZSIMPATH
current_dir=${PWD}

zsim_path=$(echo $zsim_path | sed 's./.\\/.g')
current_dir=$(echo $current_dir | sed 's./.\\/.g')

mkdir -p config/tech
mkdir -p config/zsim

cp /scratch0/malviya/modSim/config/tech/Config_Baseline_28nm_1_8.pl config/tech/Config_Baseline_28nm_1_8.pl
cp /scratch0/malviya/modSim/config/tech/Config_N3XT_28nm_3_8.pl config/tech/Config_N3XT_28nm_3_8.pl
cp /scratch0/malviya/modSim/config/zsim/zsim_Baseline_8.cfg config/zsim/zsim_Baseline_8.cfg
cp /scratch0/malviya/modSim/config/zsim/zsim_N3XT_8.cfg config/zsim/zsim_N3XT_8.cfg

cp -r /scratch0/malviya/modSim/config/multipliers config/multipliers
cp -r /scratch0/malviya/modSim/ops .
cp /scratch0/malviya/modSim/Acc_results_compare_trace.pl .
cp /scratch0/malviya/modSim/Acc_results_processing_silent.pl .
cp /scratch0/malviya/modSim/Extract_operations.pl .
cp /scratch0/malviya/modSim/Parse_all_results.pl .
cp /scratch0/malviya/modSim/psim.sh .
cp /scratch0/malviya/modSim/simulate_zsim.sh .

sed -i "7 s/.*/    (cd \$D \&\& echo \"[Y] Running \$\{PWD##*\/\}\" \&\& ${zsim_path}\/build\/opt\/zsim ${current_dir}\/config\/zsim\/zsim_\$\{1\}_\$\{2\}\.cfg \&>\/dev\/null)/" simulate_zsim.sh

sed -i "3 s/.*/network=(langmod alex_net captioning vgg19_net resnet152)/" psim.sh

sed -i "4 s/.*//" psim.sh
sed -i "5 s/.*/word_size=(8)/" psim.sh
sed -i "6 s/.*/batch_size=(1)/" psim.sh
sed -i "7 s/.*/config=(Baseline N3XT)/" psim.sh
sed -i "8 s/.*//" psim.sh
sed -i "18 s/.*/        	path=${current_dir}\/\$i\/\$j\/\$k\/\$x/" psim.sh
sed -i "20 s/.*/            	bash ${current_dir}\/simulate_zsim.sh \$x \$j/" psim.sh

sed -i "15 s/.*/my @config_range=(\"Baseline\",\"N3XT\");/" Parse_all_results.pl
# if you get an error about an op file not existing, uncomment lines 21 thru 26 in Parse_all_results.pl and point the $schedule_directory variable to the right path

sed -i "16 s/.*/my \$Config_BaseDir=\"${current_dir}\/config\/tech\"; #TODO: Fill with the correct path/" Acc_results_compare_trace.pl
sed -i "17 s/.*/my @arch=(\"Baseline\",\"N3XT\");/" Acc_results_compare_trace.pl
sed -i "18 s/.*/my @Freq=(1,3); #TODO: Feed them as inputs later/" Acc_results_compare_trace.pl
sed -i "19 s/.*/my \$availtypes=2;/" Acc_results_compare_trace.pl
sed -i "23 s/.*/my @Summary=([0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0]);/" Acc_results_compare_trace.pl

mkdir -p alex_net/8/1/
cp -r /scratch0/malviya/modSim/alex_net/8/1/Baseline alex_net/8/1
cp -r alex_net/8/1/Baseline alex_net/8/1/N3XT

mkdir -p langmod/8/1/
cp -r /scratch0/malviya/modSim/langmod/8/1/Baseline langmod/8/1
cp -r langmod/8/1/Baseline langmod/8/1/N3XT

mkdir -p captioning/8/1/
cp -r /scratch0/malviya/modSim/captioning/8/1/Baseline captioning/8/1
cp -r captioning/8/1/Baseline captioning/8/1/N3XT

mkdir -p vgg19_net/8/1/
cp -r /scratch0/malviya/modSim/vgg19_net/8/1/Baseline vgg19_net/8/1
cp -r vgg19_net/8/1/Baseline vgg19_net/8/1/N3XT

mkdir -p resnet152/8/1/
cp -r /scratch0/malviya/modSim/resnet152/8/1/Baseline resnet152/8/1
cp -r resnet152/8/1/Baseline resnet152/8/1/N3XT

#./psim.sh

#./Parse_all_results.pl alex_net 1
#./Parse_all_results.pl resnet152 1
#./Parse_all_results.pl vgg19_net 1
#./Parse_all_results.pl langmod 3
#./Parse_all_results.pl captioning 3
