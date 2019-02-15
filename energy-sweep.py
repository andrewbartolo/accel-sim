#!/usr/bin/env python3

import sys, os

from template import *
from util import *


rdWrEnergies = [(5.8, 6.2),
                (4.5, 4.9),
                (4.3, 4.7),
                (3.9, 4.3),
                (2.4, 2.7),
                (2.2, 2.5),
                (1.8, 2.2)]
perChannelLeakages = [8.3, 18, 24, 30.25]

networks = ['langmod', 'resnet152']
wordSizes = ['8']
batchSizes = ['1', '4']

bandwidths = [4.6, 9, 18, 74, 106, 418, 840]        # in GB/s.
latencies = [(24, 23), (10, 15), (5, 12), (4, 12)]  # (rdLat, wrLat) tuples. In ns.

netBatchCSVColumnNames = ['BW', 'rdLat', 'wrLat', 'rdEnergy', 'wrEnergy', 'perChLkg',
                          'tProc', 'tMem', 'tTotal', 'eActive', 'eIdle', 'eMem', 'eTotal',
                          'bDelay', 'bEnergy', 'bProduct']


class collectedCSVLine:
    def __init__(self, bw, rdLat, wrLat, rdEnergy, wrEnergy, perChLkg):
        self.bw             = bw
        self.rdLat          = rdLat
        self.wrLat          = wrLat
        self.rdEnergy       = rdEnergy
        self.wrEnergy       = wrEnergy
        self.perChLkg       = perChLkg

    def fillRemaining(self, benefitsLine):
        benefitsToks = benefitsLine.split(',')
        self.tProc          = benefitsToks[1]
        self.tMem           = benefitsToks[2]
        self.tTotal         = benefitsToks[3]
        self.eActive        = benefitsToks[4]
        self.eIdle          = benefitsToks[5]
        self.eMem           = benefitsToks[6]
        self.eTotal         = benefitsToks[7]
        self.bDelay         = benefitsToks[8]
        self.bEnergy        = benefitsToks[9]
        self.bProduct       = benefitsToks[10]


    def getLineStr(self):
        return ','.join([self.bw, self.rdLat, self.wrLat, self.rdEnergy, self.wrEnergy,
                         self.perChLkg, self.tProc, self.tMem, self.tTotal,
                         self.eActive, self.eIdle, self.eMem, self.eTotal,
                         self.bDelay, self.bEnergy, self.bProduct]) + '\n'




def gen_sweeps(processPerl=False,collectResults=False):
    for net in networks:
        for batchSize in batchSizes:
            netBatchCSVPath = './results-energy/%s_%s.csv' % (net, batchSize)
            netBatchCSV = open(netBatchCSVPath, 'w+')   # always creates file (may be empty)
            netBatchCSV.write(','.join(netBatchCSVColumnNames) + '\n') # write the CSV header

            for bw in bandwidths:
                for lat in latencies:
                    configName = 'newMem_%sGBs_%sns_%sns' % (str(bw), str(lat[0]), str(lat[1]))

                    for lkg in perChannelLeakages:
                        for rdWrEn in rdWrEnergies:
                            bitRdEnStr = str(rdWrEn[0])
                            bitWrEnStr = str(rdWrEn[1])
                            perChLkgStr = str(lkg)

                            #print('<%s %s %s>' % (bitRdEnStr, bitWrEnStr, perChLkgStr))


                            # csvTempName is the name of the file that ./Parse_all_results.pl
                            # spits out, that we need to rename to reflect energy values.
                            csvTempName =   '%s_8_%s_' % (net, batchSize)
                            csvTempName +=  configName
                            csvTempName +=  '.csv'

                            csvFullName =   '%s_8_%s_' % (net, batchSize)
                            csvFullName +=  configName
                            csvFullName +=  '_%spJ_%spJ_%smW' % (bitRdEnStr, bitWrEnStr, perChLkgStr)
                            csvFullName +=  '.csv'


                            if processPerl:
                                # For simplicity's sake, we re-generate and overwrite the .pl file
                                # for the energy post-processing (this to avoid changing the
                                # naming scheme expected by the .pl script).
                                tTemplate = './config/templates/tech-energy.ttemplate'
                                tFile = './config/tech/Config_%s_28nm_1_8.pl' % configName
                                fillTemplate(tTemplate, tFile, {'bitRdEn':      bitRdEnStr,
                                                                'bitWrEn':      bitWrEnStr,
                                                                'perChLkg':     perChLkgStr})
                                os.system('chmod a+x %s' % tFile)   # make the .pl file executable


                                # run the current templatization of the tech file
                                os.system('./Parse_all_results.pl %s %s %s' % (net, batchSize, configName))

                                # rename the .csv to its full (with energy) name
                                os.system('mv ./results/%s ./results/%s' % (csvTempName, csvFullName))



                            if collectResults:
                                singleRunCSV = open('./results/'+csvFullName, 'r')
                                benefitsLine = singleRunCSV.readlines()[-1]

                                collectedLine = collectedCSVLine(str(bw), str(lat[0]), str(lat[1]),
                                                bitRdEnStr, bitWrEnStr, perChLkgStr)
                                collectedLine.fillRemaining(benefitsLine)

                                netBatchCSV.write(collectedLine.getLineStr())
                                singleRunCSV.close()


            netBatchCSV.close()


if __name__ == '__main__':
    #gen_sweeps(processPerl=True,collectResults=False)
    gen_sweeps(processPerl=False,collectResults=True)

