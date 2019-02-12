#!/usr/bin/bash

# Make zsim dependency libraries visible to zsim
export LD_LIBRARY_PATH='/rsgs/pool0/bartolo/TSMC/proto/lib:/rsgs/pool0/bartolo/TSMC/hdf5/usr/lib64'
export HDF5_DISABLE_VERSION_CHECK=1

echo "Simulating: ${PWD##*/}"

for D in $PWD/*;
do
    #(cd $D && echo "[Y] Running ${PWD##*/}" && /pool0/bartolo/TSMC/ORNL-zsim-logic/build/opt/zsim /rsghome/mattlkf/pool/tsmc_eric/nov27_alexnet_vgg_table/sim/config/zsim/zsim_${1}_${2}.cfg &>/dev/null)
    (cd $D && echo "[Y] Running ${PWD##*/}" && /pool0/bartolo/TSMC/ORNL-zsim-logic/build/opt/zsim /rsgs/pool0/bartolo/TSMC/sim-auto/config/zsim/zsim_${1}_${2}.cfg &>/dev/null)
#exit
done

echo "Simulation Finished"
