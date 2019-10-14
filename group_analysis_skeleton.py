#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
scene-cat problem set for PSY 1210 - Fall 2018

@author: Michael Mack
"""

#%% import block 
import numpy as np
import scipy as sp
import scipy.stats
import os
import shutil


#%%
# copy files from testing room folders to raw data, rename files to include
# testing room letter in the filename

os.getcwd() #checking to see the current working directory, it is '/Users'
os.chdir('Users/arianagiuliano/Desktop/programming_hwk') #I want to work from the programming_hwk file on my desktop

testingrooms = ['A','B','C']
for room in testingrooms:
    shutil.copy('testingroom' + room + '/experiment_data.csv', 'rawdata')
    os.rename('rawdata/experiment_data.csv', 'rawdata/experiment_data_' + room + '.csv')

#now everything has been copied to rawdata

#%%
# read in all the data files in rawdata directory using a for loop
# columns: subject, stimulus, pairing, accuracy, median RT

data = np.empty((0,5))
for room in testingrooms:
    alldata = sp.loadtxt('rawdata/experiment_data_' + room + '.csv', delimiter = ',')
    data = np.vstack([data, alldata])

#%%
# calculate overall average accuracy and average median RT

acc_avg = np.average(data[:,3])   # mean is 91.48%
mrt_avg = np.average(data[:,4])   # mean is 477.34ms

#%%
# calculate averages (accuracy & RT) split by stimulus using a for loop and an 
# if statement. (i.e., loop through the data to make a sum for each condition, 
# then divide by the number of data points going into the sum)

#we are working with the following acc and RT averages (which first need to be summed):
accwords_sum = 0
RTwords_sum = 0 
words = 0
accfaces_sum = 0
RTfaces_sum = 0
faces = 0

for x in range(len(data)):
    if data[x,1] == 1:
        accwords_sum += data[x,3]
        RTwords_sum += data[x,4]
    else:
        words += 1
        accfaces_sum += data[x,3]
        RTfaces_sum += data[x,4]
        faces += 1

#now we have the sums of each measure, by stimulus type, and can use these to get averages

accwords_mean = accwords_sum/words #accuracy average is 88.56%
RTwords_mean = RTwords_sum/words #reaction time average is 489.37ms
accfaces_mean = accfaces_sum/faces #accuracy average is 94.40%
RTfaces_mean = RTfaces_sum/faces#reaction time average is 465.30ms

# words: 88.6%, 489.4ms   faces: 94.4%, 465.3ms

#%%
# calculate averages (accuracy & RT) split by congruency using indexing, 
# slicing, and numpy's mean function 
# wp - white/pleasant, bp - black/pleasant
# (hint: only one line of code is needed per average)

acc_wp = np.mean(data[data[:,2] == 1, 3]) # 94.0%
acc_bp = np.mean(data[data[:,2] == 2, 3]) # 88.9%
mrt_wp = np.mean(data[data[:,2] == 1, 4]) # 469.6ms
mrt_bp = np.mean(data[data[:,2] == 2, 4]) # 485.1ms

#%% 
# calculate average median RT for each of the four conditions
# use for loops, indexing/slicing, or both!
# (hint: might be easier to slice data into separate words and faces datasets)

#going the easy route by splitting the data

wrddata = data[data[:,1]==1,:]
facedata = data[data[:,1]==2,:]

#using numpy mean function as above 

mRT_WP_wrds = np.mean(wrddata[wrddata[:,2]==1,4]) #478.41ms
mRT_BP_wrds = np.mean(wrddata[wrddata[:,2]==2,4]) #500.33ms
mRT_WP_faces = np.mean(facedata[facedata[:,2]==1,4]) #460.76ms
mRT_BP_faces = np.mean(facedata[facedata[:,2]==2,4]) #469.85ms

#%%        
# compare pairing conditions' effect on RT within stimulus using scipy's 
# paired-sample t-test: scipy.stats.ttest_rel()

import scipy.stats as ss
t_result_wrd = ss.ttest_rel(wrddata[wrddata[:,2]==1,4], wrddata[wrddata[:,2]==2,4]) # t = -5.36 p = 2.19e-5
t_result_face = ss.ttest_rel(facedata[facedata[:,2]==1,4], facedata[facedata[:,2]==2,4]) # t = -2.84 p = 0.0096
# words: t=-5.36, p=2.19e-5
# faces: t=-2.84, p=0.0096

#%%
# print out averages and t-test results
# (hint: use the ''.format() method to create formatted strings)
print('\nOVERALL: {:.2f}%, {:.1f} ms'.format(100*acc_avg,mrt_avg))

##For median reaction times

print('\nFor word blocks, the average median reaction time for BP pairings ({:.1f}ms) was significantly different from the average median reaction time for WP pairings ({:.1f}ms),t = {:.2f}, p < .05.'.format(mRT_BP_wrds, mRT_WP_wrds, t_result_wrd[0]))
#For word blocks, the average median reaction time for BP pairings (500.3ms) was significantly different from the average median reaction time for WP pairings (478.4ms),t = -5.36, p < .05.

print('\nFor face blocks, the average median reaction time for BP pairings ({:.1f}ms) was significantly different from the average median reaction time for WP pairings ({:.1f}ms),t = {:.2f}, p < .05.'.format(mRT_BP_faces, mRT_WP_faces, t_result_face[0]))
#For face blocks, the average median reaction time for BP pairings (469.8ms) was significantly different from the average median reaction time for WP pairings (460.8ms),t = -2.84, p < .05.

##For accuracy, just BP v. WP

print('\nNo t-tests were run, however, the average accuracy for BP pairings,({:.1f}%) seemed to differ from the average accuracy for WP pairings ({:.1f}%).'.format((100*acc_bp),(100*acc_wp)))
#No t-tests were run, however, the average accuracy for BP pairings,(88.9%) seemed to differ from the average accuracy for WP pairings (94.0%).

##For accuracy, words v. faces

print('\nNo t-tests were run, however, the average accuracy for words,({:.1f}%) seemed to differ from the average accuracy for faces ({:.1f}%).'.format((100*accwords_mean),(100*accfaces_mean)))
#No t-tests were run, however, the average accuracy for words,(88.6%) seemed to differ from the average accuracy for faces (94.4%).
