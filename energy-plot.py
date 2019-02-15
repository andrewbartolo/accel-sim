#!/usr/bin/env python3

import csv
import numpy as np
import matplotlib.pyplot as plt
import sys, os

from template import *
from util import *


PLOT_DPI = 600
#PLOT_COLORMAP = 'gist_yarg'
#PLOT_COLORMAP = 'coolwarm_r'
#PLOT_COLORMAP = 'winter'
#PLOT_COLORMAP = 'RdYlBu'
PLOT_COLORMAP = 'RdYlGn'




networks = ['langmod', 'resnet152']
networkLayNames = {'langmod': 'LSTM', 'resnet152': 'CNN'}
wordSizes = ['8']
batchSizes = ['1', '4']

csvColumnNames = ['BW', 'rdLat', 'wrLat', 'rdEnergy', 'wrEnergy', 'perChLkg',
                  'tProc', 'tMem', 'tTotal', 'eActive', 'eIdle', 'eMem', 'eTotal',
                  'bDelay', 'bEnergy', 'bProduct']




## TODO TODO -- clean up copypasta
if __name__ == '__main__':

    for net in networks:
        for batchSize in batchSizes:
            print('-'*80)
            configName = '%s_%s' % (net, batchSize)
            csvFileName = './results-energy/%s.csv' % configName
            csv = np.genfromtxt(csvFileName, delimiter=',', names=True)
            print(csvFileName)

            #print('Min benefits: %f' % np.min(csv['bProduct']))
            #print('Max benefits: %f' % np.max(csv['bProduct']))



################################################################################
#########################rdLat bDelay###########################################
################################################################################

            fig, ax = plt.subplots()
            ax.scatter(csv['BW'], csv['rdLat'], c=csv['bDelay'], cmap=PLOT_COLORMAP)

            ax.set_title('%s, batch size %s' % (networkLayNames[net], batchSize))
            ax.xaxis.set_label_text('Bandwidth (GB/s)')
            ax.yaxis.set_label_text('Read latency (ns)')
            cbar = plt.colorbar(ax.get_children()[0])    # TODO don't mix fig/ax and plt paradigms
            cbar.ax.set_ylabel('Delay Benefits', rotation=270)
            cbar.ax.get_yaxis().labelpad = 15

            fig.savefig('./plots/%s_rdLat_bDelay.png' % configName, format='png', dpi=PLOT_DPI)



################################################################################
#########################rdLat bEnergy##########################################
################################################################################

            fig, ax = plt.subplots()
            ax.scatter(csv['BW'], csv['rdLat'], c=csv['bEnergy'], cmap=PLOT_COLORMAP)

            ax.set_title('%s, batch size %s' % (networkLayNames[net], batchSize))
            ax.xaxis.set_label_text('Bandwidth (GB/s)')
            ax.yaxis.set_label_text('Read latency (ns)')
            cbar = plt.colorbar(ax.get_children()[0])    # TODO don't mix fig/ax and plt paradigms
            cbar.ax.set_ylabel('Energy Benefits', rotation=270)
            cbar.ax.get_yaxis().labelpad = 15

            fig.savefig('./plots/%s_rdLat_bEnergy.png' % configName, format='png', dpi=PLOT_DPI)



################################################################################
#########################rdEnergy bDelay########################################
################################################################################

            fig, ax = plt.subplots()
            ax.scatter(csv['BW'], csv['rdEnergy'], c=csv['bDelay'], cmap=PLOT_COLORMAP)

            ax.set_title('%s, batch size %s' % (networkLayNames[net], batchSize))
            ax.xaxis.set_label_text('Bandwidth (GB/s)')
            ax.yaxis.set_label_text('Read energy (pJ/bit)')
            cbar = plt.colorbar(ax.get_children()[0])    # TODO don't mix fig/ax and plt paradigms
            cbar.ax.set_ylabel('Delay Benefits', rotation=270)
            cbar.ax.get_yaxis().labelpad = 15

            fig.savefig('./plots/%s_rdEnergy_bDelay.png' % configName, format='png', dpi=PLOT_DPI)



################################################################################
#########################rdEnergy bEnergy########################################
################################################################################

            fig, ax = plt.subplots()
            ax.scatter(csv['BW'], csv['rdEnergy'], c=csv['bEnergy'], cmap=PLOT_COLORMAP)

            ax.set_title('%s, batch size %s' % (networkLayNames[net], batchSize))
            ax.xaxis.set_label_text('Bandwidth (GB/s)')
            ax.yaxis.set_label_text('Read energy (pJ/bit)')
            cbar = plt.colorbar(ax.get_children()[0])    # TODO don't mix fig/ax and plt paradigms
            cbar.ax.set_ylabel('Energy Benefits', rotation=270)
            cbar.ax.get_yaxis().labelpad = 15

            fig.savefig('./plots/%s_rdEnergy_bEnergy.png' % configName, format='png', dpi=PLOT_DPI)











            """
            # TODO this actually overwrites the value nPoints times, but w/e
            #for i in range(784):
            #    ax.annotate(1, (csv['BW'][i], csv['rdLat'][i]))
            """

