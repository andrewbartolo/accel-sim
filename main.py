#!/usr/bin/env python3

################################################################################
## Top-level simulation driver.
##
## TODO: clean up nested loops
################################################################################

import sys, os

from template import *
from util import *


#networks = ['alex_net', 'langmod', 'resnet152', 'vgg19_net']
networks = ['langmod', 'resnet152']
wordSizes = ['8']
#batchSizes = ['1', '4', '8', '16']
batchSizes = ['1', '4']
configs = ['Baseline']  ## NOTE: we'll append auto-swept configs to this later

bandwidths = [4.6, 9, 18, 74, 106, 418, 840]        # in GB/s.
latencies = [(24, 23), (10, 15), (5, 12), (4, 12)]  # (rdLat, wrLat) tuples. In ns.
nMemChannels = 4     # for calculating perChannelBW



if __name__ == '__main__':
    # TODO: remove old network directories and results dir for good measure?


    #################################################
    ## Generate param-sweep directory names and config files
    #################################################

    # first, straight-copy the template files to Baseline files
    # TODO can't do this, they need to have macros replaced with 0s.
    # Just leave Baseline files in the directories for now.
    '''
    os.system('cp %s ./config/zsim/zsim_Baseline_8.cfg' % zTemplate)
    os.system('cp %s ./config/tech/Config_Baseline_28nm_1_8.pl' % tTemplate)
    os.system('chmod a+x ./config/tech/Config_Baseline_28nm_1_8.pl')
    '''

    # now, templatize the swept parameter files
    for bw in bandwidths:
        for lat in latencies:
            configName = 'newMem_%sGBs_%sns_%sns' % (str(bw), str(lat[0]), str(lat[1]))
            configs.append(configName)

            # templatize the zsim .cfg file
            zTemplate = './config/templates/zsim.ztemplate'
            zFile = './config/zsim/zsim_%s_8.cfg' % configName
            perChannelBW = int((int(bw) * 1e3) / nMemChannels);  # TODO round?
            fillTemplate(zTemplate, zFile, {'perChannelBW':     str(perChannelBW),
                                            'rdLat':            str(lat[0]),
                                            'wrLat':            str(lat[1])});

            # templatize the tech .pl file
            # TODO - this doesn't make any substitutions right now,
            # it's just a placeholder (just copies and renames the file)
            tTemplate = './config/templates/tech.ttemplate'
            tFile = './config/tech/Config_%s_28nm_1_8.pl' % configName
            fillTemplate(tTemplate, tFile, {})
            os.system('chmod a+x %s' % tFile)   # make the .pl file executable


    #################################################
    #################################################




    #################################################
    ## Create (by cloning) the directory structure ##
    #################################################
    print_nobr("Creating directory structure...")

    for net in networks:
        for wordSize in wordSizes:
            for batchSize in batchSizes:
                for config in configs:
                    traceSrcSubDir = 'traces/%s/%s/%s/*' % (net, wordSize, batchSize)
                    configSubDir = '%s/%s/%s/%s' % (net, wordSize, batchSize, config)

                    os.system('mkdir -p %s' % configSubDir)   # create the subdir
                    linkclone_dir(traceSrcSubDir, configSubDir) # clone the trace directory

    print(" done.")
    #################################################
    #################################################




    #################################################
    ## do the zim run, then the tech post-processing
    #################################################
    print("Beginning simulation runs...")

    for net in networks:
        for wordSize in wordSizes:
            for batchSize in batchSizes:
                for config in configs:
                    baseDir = os.getcwd()
                    workDir = '%s/%s/%s/%s' % (net, wordSize, batchSize, config)

                    # run zsim simulation
                    os.system('cd %s && %s/simulate_zsim.sh %s %s' % (workDir, baseDir, config, wordSize))
                    print('%s_%s_%s %s zsim finished' % (net, wordSize, batchSize, config))

                    # post-process with energy, etc. perl script
                    if (config != 'Baseline'):
                        os.system('./Parse_all_results.pl %s %s %s' % (net, batchSize, config))


    print("Finished simulation runs.")
    #################################################
    #################################################

    # Done.
