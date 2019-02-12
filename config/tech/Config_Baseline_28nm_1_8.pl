#Architecture Params
$NCORES=4;
$ncompute=256;
$NUM_CACHE_LEVELS=2;
@NCACHE=(2*$NCORES,$NCORES);
$NCONTROLLERS=4;
$leakage_power = 0.097;#W
$Dynamic_E_per_op = 0.00048;#nJ
$Frequency=1; #Core frequency in GHz
$reg_bit_width=8;
$reg_e_per_bit=0.4;#pJ/bit
#Power/Performance Parameters
@CACHE_E=(0.009,0.009,0.0814);#Cache energy access nJ
@CACHE_LKG=(0.068,0.068,0.174); #mW
@MEM_E_per_bit=(0,0); # Additional Energy per bit in memories in pJ/bit for DRAM based memories (Rd, Wr energy for MD1 model) 
# TODO need to define MEM_LKG here?
$LINE_SIZE=256; #line size in Bits
$Do_power_map=0;
#$Initial_X_offset=700;
#$Initial_Y_offset=1100;
#$mem_C_xy=1100;
#$mem_C_yx=700;
#$Core_x=600;
#$Core_y=1000;
#$L1_I_x=240;
#$L1_I_y=100;
#$L1_D_x=360;
#$L1_D_y=100;
#$L2_x=600;
#$L2_y=1000;
#$offset_x=100;
#$offset_y=1100;
#$CoreNAME="NNEngine_";
#$L1_Inst= "Rdbuf_";
#$L1_Data="Wrbuf_";
#$L2="Globalbuf_";
#$Slot_time=1e-2;
#$memC_power=1;
#$L1I_power=0.174;
#$L1D_power=0.174;
#$L2_power=0.3745;
1;