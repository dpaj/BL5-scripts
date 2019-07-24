import numpy as np
import pandas as pd
from StringIO import StringIO
import os


def list2range(lst):
    '''make iterator of ranges of contiguous numbers from a list of integers'''

    tmplst = lst[:]
    tmplst.sort()
    start = tmplst[0]

    currentrange = [start, start + 1]

    for item in tmplst[1:]:
        if currentrange[1] == item:
            # contiguous
            currentrange[1] += 1
        else:
            # new range start
            yield tuple(currentrange)
            currentrange = [item, item + 1]

    # last range
    yield tuple(currentrange)

def runs_as_ranges(this_run_set):
    #this_run_set_as_range = list(list2range(this_run_set))
    ranges_string = ''
    for x in list(list2range(this_run_set)):
       ranges_string += 'range'+str(x)+'+'
    return ranges_string[:-1]


my_experiment_log_file = '/SNS/SEQ/IPTS-23197/shared/autoreduce/experiment_log.csv'

#just put the path to the file you downloaded from https://oncat.ornl.gov right here
my_ONCAT_file = my_experiment_log_file


#this part should be OK to just run
print('****************')
print('using data file:')
print(my_ONCAT_file)

my_ONCAT_data = pd.read_csv(my_ONCAT_file, skipinitialspace=True, sep=',',index_col=False)

#

print(my_ONCAT_data['Title'])

unique_run_titles = []
for idx, val in enumerate(my_ONCAT_data['Title']):
    #single crystal, remove omega values
    val = val.split('__w')[0]
    if val in unique_run_titles:
		pass
    else:
		unique_run_titles.append(val)

print('************************')
print('found unique run titles:')
for idx, val in enumerate(unique_run_titles):
    print(idx, val)

runs_lists = []
for i in range(len(unique_run_titles)):
	runs_lists.append([])

for idx, val in enumerate(my_ONCAT_data['Title']):
	for jdx,jal in enumerate(unique_run_titles):
		if unique_run_titles[jdx] in val:
			runs_lists[jdx].append(my_ONCAT_data['RunNumber'][idx])


print('***********************')
print('runs digest:')
for idx, val in enumerate(unique_run_titles):
	print(idx, unique_run_titles[idx], "num of runs = {0}".format(len(runs_lists[idx])), runs_lists[idx], runs_as_ranges(runs_lists[idx]) )

# Create directories
my_working_base_directory = '/SNS/CNCS/IPTS-23272/shared/scripts/'
for this_run_title in unique_run_titles:
    dirName = my_working_base_directory+this_run_title
    try:
        # Create target Directory
        os.mkdir(dirName)
        print("Directory " + dirName +  " Created ") 
    except:
        print("Directory " , dirName ,  " already exists")
