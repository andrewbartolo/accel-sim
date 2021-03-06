#!/usr/bin/env python3

import csv
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import FormatStrFormatter
from matplotlib.ticker import MaxNLocator
from matplotlib.ticker import ScalarFormatter

import sys, os

from template import *
from util import *


PLOT_DPI = 600
#PLOT_COLORMAP = 'gist_yarg'
#PLOT_COLORMAP = 'coolwarm_r'
#PLOT_COLORMAP = 'winter'
#PLOT_COLORMAP = 'RdYlBu'
#PLOT_COLORMAP = 'RdYlGn'
PLOT_COLORMAP = 'coolwarm'




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

            # make a list of all the (x,y) points to be plotted
            # so that we can put labels on them later
            bwValues = np.unique(csv['BW'])
            rdLatValues = np.unique(csv['rdLat'])
            rdEnergyValues = np.unique(csv['rdEnergy'])

            bwRdLatCoords = [(x, y) for x in bwValues for y in rdLatValues]
            bwRdEnergyCoords = [(x, y) for x in bwValues for y in rdEnergyValues]









################################################################################
#########################rdLat bDelay###########################################
################################################################################

            fig, ax = plt.subplots()

            C = []
            for x, y in bwRdLatCoords:
                filteredRows = np.array([row for row in csv if row['BW'] == x and row['rdLat'] == y])
                bestBDelay = np.max(filteredRows['bDelay'])
                C.append(bestBDelay)
            C = np.array(C)
            C = C.reshape(len(bwValues), len(rdLatValues))
            C = C.T     # row-major to x-y
            X, Y = np.meshgrid(bwValues, rdLatValues)
            p = ax.contour(X, Y, C, cmap=PLOT_COLORMAP)
            plt.clabel(p, inline=0, fontsize='large', colors='k', fmt='%1.1f')

            #ax.set_title('%s, batch size %s' % (networkLayNames[net], batchSize))
            ax.xaxis.set_label_text('Bandwidth (GB/s)')
            ax.yaxis.set_label_text('Read latency (ns)')
            ax.set_xscale('log')
            ax.set_xticks(bwValues)
            ax.xaxis.set_major_formatter(ScalarFormatter())
            ax.xaxis.set_major_formatter(FormatStrFormatter('%d'))
            ax.yaxis.set_major_locator(MaxNLocator(integer=True))


#            cbar = plt.colorbar(ax.get_children()[0])    # TODO don't mix fig/ax and plt paradigms
#            cbar.ax.set_ylabel('Delay Benefits', rotation=270)
#            cbar.ax.get_yaxis().labelpad = 15

            fig.savefig('./plots/%s_rdLat_bDelay.png' % configName, format='png', dpi=PLOT_DPI)


################################################################################
#########################rdLat bEnergy##########################################
################################################################################

            fig, ax = plt.subplots()

            C = []
            for x, y in bwRdLatCoords:
                filteredRows = np.array([row for row in csv if row['BW'] == x and row['rdLat'] == y])
                bestBEnergy = np.max(filteredRows['bEnergy'])
                C.append(bestBEnergy)
            C = np.array(C)
            C = C.reshape(len(bwValues), len(rdLatValues))
            C = C.T     # row-major to x-y
            X, Y = np.meshgrid(bwValues, rdLatValues)
            p = ax.contour(X, Y, C, cmap=PLOT_COLORMAP)
            plt.clabel(p, inline=0, fontsize='large', colors='k', fmt='%1.1f')


            #ax.set_title('%s, batch size %s' % (networkLayNames[net], batchSize))
            ax.xaxis.set_label_text('Bandwidth (GB/s)')
            ax.yaxis.set_label_text('Read latency (ns)')
            ax.set_xscale('log')
            ax.set_xticks(bwValues)
            ax.xaxis.set_major_formatter(ScalarFormatter())
            ax.xaxis.set_major_formatter(FormatStrFormatter('%d'))
            ax.yaxis.set_major_locator(MaxNLocator(integer=True))


#            cbar = plt.colorbar(ax.get_children()[0])    # TODO don't mix fig/ax and plt paradigms
#            cbar.ax.set_ylabel('Energy Benefits', rotation=270)
#            cbar.ax.get_yaxis().labelpad = 15

            fig.savefig('./plots/%s_rdLat_bEnergy.png' % configName, format='png', dpi=PLOT_DPI)



################################################################################
#########################rdEnergy bDelay########################################
################################################################################

            fig, ax = plt.subplots()


            C = []
            for x, y in bwRdEnergyCoords:
                filteredRows = np.array([row for row in csv if row['BW'] == x and row['rdEnergy'] == y])
                bestBDelay = np.max(filteredRows['bDelay'])
                C.append(bestBDelay)
            C = np.array(C)
            C = C.reshape(len(bwValues), len(rdEnergyValues))
            C = C.T     # row-major to x-y
            X, Y = np.meshgrid(bwValues, rdEnergyValues)
            p = ax.contour(X, Y, C, cmap=PLOT_COLORMAP)
            plt.clabel(p, inline=0, fontsize='large', colors='k', fmt='%1.1f')




            #ax.set_title('%s, batch size %s' % (networkLayNames[net], batchSize))
            ax.xaxis.set_label_text('Bandwidth (GB/s)')
            ax.yaxis.set_label_text('Read energy (pJ/bit)')
            ax.set_xscale('log')
            ax.set_xticks(bwValues)
            ax.xaxis.set_major_formatter(ScalarFormatter())
            ax.xaxis.set_major_formatter(FormatStrFormatter('%d'))



#            cbar = plt.colorbar(ax.get_children()[0])    # TODO don't mix fig/ax and plt paradigms
#            cbar.ax.set_ylabel('Delay Benefits', rotation=270)
#            cbar.ax.get_yaxis().labelpad = 15

            fig.savefig('./plots/%s_rdEnergy_bDelay.png' % configName, format='png', dpi=PLOT_DPI)



################################################################################
#########################rdEnergy bEnergy########################################
################################################################################

            fig, ax = plt.subplots()

            C = []
            for x, y in bwRdEnergyCoords:
                filteredRows = np.array([row for row in csv if row['BW'] == x and row['rdEnergy'] == y])
                bestBEnergy = np.max(filteredRows['bEnergy'])
                C.append(bestBEnergy)
            C = np.array(C)
            C = C.reshape(len(bwValues), len(rdEnergyValues))
            C = C.T     # row-major to x-y
            X, Y = np.meshgrid(bwValues, rdEnergyValues)
            p = ax.contour(X, Y, C, cmap=PLOT_COLORMAP)
            plt.clabel(p, inline=0, fontsize='large', colors='k', fmt='%1.1f')


            #ax.set_title('%s, batch size %s' % (networkLayNames[net], batchSize))
            ax.xaxis.set_label_text('Bandwidth (GB/s)')
            ax.yaxis.set_label_text('Read energy (pJ/bit)')
            ax.set_xscale('log')
            ax.set_xticks(bwValues)
            ax.xaxis.set_major_formatter(ScalarFormatter())
            ax.xaxis.set_major_formatter(FormatStrFormatter('%d'))



#            cbar = plt.colorbar(ax.get_children()[0])    # TODO don't mix fig/ax and plt paradigms
#            cbar.ax.set_ylabel('Energy Benefits', rotation=270)
#            cbar.ax.get_yaxis().labelpad = 15

            fig.savefig('./plots/%s_rdEnergy_bEnergy.png' % configName, format='png', dpi=PLOT_DPI)











            """
            # TODO this actually overwrites the value nPoints times, but w/e
            #for i in range(784):
            #    ax.annotate(1, (csv['BW'][i], csv['rdLat'][i]))
            """

