# -*- coding: utf-8 -*-
"""
Created on Thu Sep  7 20:26:16 2017

@author: vyachez
Python 3.6.0
"""
import os
import csv

# NAME OF DATASET
dsetname = "myset"

# USE NAMES OF IMAGE CLASSES YOU have DOWNLOADed stored
# in categories.csv file in categories folder located
# in script directory

nmlst = []


with open('categories/categories.csv','rt') as csvfile:
    reader = csv.reader(csvfile)
    for row in reader:
        for i in row:
            nmlst.append(i)
     
clas_dir_name_lst = []

def equal(dset, dirlist):
    '''Function to make equal number of uploaded images of all classes
    throughout all dataset. For example, directory with class1 images contains 'x'
    images, therefore class2 directory should contain the same number of images
    or vice versa, depending which directory contains less.
    This function contains executive function inside.
    Arguments:
        'dset': name of dataset (data_set_name var);
        'dirlist includes dir_n_1, dir_n_n...: names of comparative directories (class_n_directory_name var).'''
    
    # forming path for all necessary directories
    # lists of directories
    dir_train_l = []
    dir_valid_l = []
    dir_sampl_tr_l = [] 
    dir_sampl_vl_l = [] 
    
    for i in dirlist:
        dir_train_l.append(dset + '/train/' + i)
        dir_valid_l.append(dset + '/valid/' + i)
        dir_sampl_tr_l.append(dset + '/sample/train/' + i)
        dir_sampl_vl_l.append(dset + '/sample/valid/' + i)

    # executive function
    def equalising(eachlist):

        catlist = []
        variance = 0        
        
        for e in eachlist:
            try:
                print ("Trying to check directory: ", e)
                c_lst = [name for name in os.listdir(e) if os.path.isfile(os.path.join(e, name))]

            except:
                print ("No equalising!")
            else:
                catlist.append(c_lst)
            
        if len(dirlist) == len(catlist):            
            
            lenlist = []                
            
            for x in catlist:
                lenlist.append(len(x))
                
            smallest = min(lenlist)
            print ("directory with smallest number of images (" + str(smallest) + ") has been found.")
            
            for index, cat, num in zip(eachlist, catlist, lenlist):
                if num != smallest:
                    variance  = num - smallest
                    print (index + ' has more on: ' + str(variance))
                    for f in cat:
                        if variance != 0:
                            print ('removing ' + index + str(f))
                            os.remove(index + f)
                            variance -= 1   
            print ("Equalised successfully")
   
    equalising(dir_train_l)
    equalising(dir_valid_l)
    equalising(dir_sampl_tr_l)
    equalising(dir_sampl_vl_l)

for inst in nmlst:
    
    class_img = inst

    # MAKING NAME OF TXT File where list of URLs is located
    ref_list_class_name = "categories/" + inst + '.txt'
    
    # Defining variables for dataset
    data_set_name = dsetname                          # name of folder that will contain dataset
    
    class_filename = class_img + '_'                  # names of images in classified dataset
    
    class_directory_name = class_img + '/'           # names of folders with classified images
    # making list of directories for equalissation    
    clas_dir_name_lst.append(class_directory_name)    
    
    logfile_class_name = "logs/" + class_img + '_files_upload_log.txt' # names of log files

# running function
equal(dsetname, clas_dir_name_lst)
