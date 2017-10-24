# Developed by Viacheslav Nesterov (the Developer) - version 1.0
# Python 3.6.0

## Script to scrap images by its web links stored in .txt file (the Script).

## User - person, who runs this script in full agreement with 
## Terms and Conditions set forth below (the User).

# Script will create ready to go dataset to plug in deep learning algorythm for
# image classification and recognition. Script version supports any number of image classes.

# Script will go through each line of .txt file for each image class supposed to have web link for image location.
# Than it will upload the image to automatically created directory tree for 
# deep learning. Script will check the corect number of images in each appropriate 
# directory to fit learning algorythm. Scrapping will try to avoid small junk files, 
# which may contain ads or 'no longer available' images, using (too small to be image) principle.
# Scrapping will validate jpeg files.

##### LEGAL DISCLAIMER - TERMS and CONDITIONS #####
# User should respect athors' rights, i.e. intellectual property rights for images,
# retrieved using this Script. The Script downloads images from publicly available links 'as is'.
# Using this Script, User is liable for any intellectual property rights violation with respect to
# retrieved images. The Developer is not liable for any inapropriate Script usage by User, 
# as well as not liable for any User's third parties rights violations and liabilities.
# User should utilise this Script for non-commercial purposes only. Non-commercial purposes
# include following: eduactional, personal use for self-education.

# Script Begins:

from __future__ import division
import urllib
from urllib.request import urlopen
import os
import sys
from random import randint
import imghdr
import csv

# NAME YOUR DATASET
dsetname = "myset"

# ENTER NAMES OF IMAGE CLASSES YOU WILL BE DOWNLOADING stored
# in categories.csv file in categories folder located
# in script directory

nmlst = []


with open('categories/categories.csv','rt') as csvfile:
    reader = csv.reader(csvfile)
    for row in reader:
        for i in row:
            nmlst.append(i)
     
clas_dir_name_lst = []

def copy(source, destination):
    '''Function to copy uploaded file to right directories, making the dataset.
    Arguments:
            'source': directory file was uploaded to;
            'destination': directory to copy file to.'''
            
    inputfile = open(source, 'rb') # reading binary
    outputfile = open(destination, 'wb') # writing binary

    buffersize = 124000
    buffer = inputfile.read(buffersize)

    while len(buffer):
        outputfile.write(buffer)
        buffer = inputfile.read(buffersize)
    outputfile.close  

def uploading(structure, refs, fl_name, fld, logfile):
    '''Function to scrap the images from resources specified in 
    http:// links stored in .txt file.
    This function downloads images that exist and call required functions to
    store images in dataset directories, equlaising the number of images.
    Arguments:
        'structure': name of folder that will contain dataset (see variables section);
        'refs': real name of .txt file where the list of images links are stored;
        'fl_name': name of folder in classified dataset;
        'fld': name of images in classified dataset;
        'logfile': name of log file. '''
    
    reflist = open(refs, 'r')
    n = 0

    for i in reflist:
        n += 1
    
    reflist = open(refs, 'r')
    log = open(logfile, 'w')
    filename = fl_name
    train_fld = structure + '/train/' + fld
    valid_fld = structure + '/valid/' + fld
    sample_train_fld = structure + '/sample/train/' + fld
    sample_valid_fld = structure + '/sample/valid/' + fld
    test_fld = structure + '/test/unknown/'
    trash_fld = structure + '/trash/'

    count = 0
    errors = 0
    removed = 0
    downloaded = 0
    
    # creating directory tree
    if not os.path.exists(os.path.dirname(train_fld)):
        os.makedirs(os.path.dirname(train_fld))
    if not os.path.exists(os.path.dirname(valid_fld)):
        os.makedirs(os.path.dirname(valid_fld))
    if not os.path.exists(os.path.dirname(sample_train_fld)):
        os.makedirs(os.path.dirname(sample_train_fld))
    if not os.path.exists(os.path.dirname(sample_valid_fld)):
        os.makedirs(os.path.dirname(sample_valid_fld))
    if not os.path.exists(os.path.dirname(test_fld)):
        os.makedirs(os.path.dirname(test_fld))
    if not os.path.exists(os.path.dirname(trash_fld)):
        os.makedirs(os.path.dirname(trash_fld))         
    print ("created directory tree...")
    print ("Started download/parsing for " + fld)
    msg = "Started download/parsing for " + fld
    log.write(str(msg) + "\n")
    
    for ref in reflist:  
        count += 1
        
        # generating random image name for test directory
        test_name = str(randint(0, 9)) + str(randint(0, 9)) + \
        str(randint(0, 9)) + str(randint(0, 9)) + str(randint(0, 9))
        
        try:
            # bypassing IO errors
            urllib.request.urlopen(ref, timeout=5)
            
        except urllib.request.HTTPError as e:
            errors += 1
            log.write("HTTP Error: " + str(e.code) + "\n")
            # print ("HTTP Error: ", e.code)
       
        except urllib.request.URLError as e:
            errors += 1
            log.write("URL Error: " + str(e.args) + "\n")
            # print ("URL Error: ", e.args)
        
        except KeyboardInterrupt:
            log.write("Interrupted!")
            print ('Interrupted!')
            sys.exit(0) 
        except:
            errors += 1
            log.write("Unknown Error for opening" + "\n")
            # print ("Uknown error for opening")
        
        else:
            # print ("IOError check passed")
            log.write("IOError check passed" + "\n")
            
            try:
                               
                
                # uploading to train directory    
                urllib.request.urlretrieve(ref, train_fld + filename + str(count) + '.jpg')
            
            except:
                errors += 1
                # print ("unknown error while uploading!")
                log.write("Unknown Error while uploading" + "\n")
           
            else: 
                filesize = os.path.getsize(train_fld + filename + str(count) + '.jpg')
                
                if filesize <= 13000:   # get rid of small garbage, putting to
                                        # separate directory for further analysis
                    os.rename(train_fld + filename + str(count) + '.jpg', trash_fld + filename + str(count) + '.jpg')
                    removed += 1
                    msg = 'Photo ' + filename + str(count) + '.jpg' + ' skipped as unavailable or junk (ads or similar garbage).'
                    log.write(msg + "\n")
                    # print (msg)
                
                # checking correct format
                elif imghdr.what(train_fld + filename + str(count) + '.jpg') != 'jpeg':
                    os.rename(train_fld + filename + str(count) + '.jpg', trash_fld + filename + str(count) + '.jpg')
                    removed += 1
                    msg = 'Photo ' + filename + str(count) + '.jpg' + ' skipped as not jpeg format.'
                    log.write(msg + "\n")
                    # print (msg)
                
                else:
                    # print ("ready to copy...")
                    # uploading to test directory
                    copy(train_fld + filename + str(count) + '.jpg', test_fld + test_name + str(count) + '.jpg')
                    # print ("copied to train")
             
                    if count <= n/100*20:
                        # uploading to valid directory
                        copy(train_fld + filename + str(count) + '.jpg', valid_fld + filename + str(count) + '.jpg')
                        # print ("copied to valid")
    
                    if count <= 10:       
                        # uploading to sample_train directory
                        copy(train_fld + filename + str(count) + '.jpg', sample_train_fld + filename + str(count) + '.jpg')
                        # uploading to sample_valid_fld directory
                        copy(train_fld + filename + str(count) + '.jpg', sample_valid_fld + filename + str(count) + '.jpg')
                        # print ("copied to sample")
                    
                    msg = filename + str(count) + '.jpg' + ' of ' + str(filesize) + 'b downloaded ok.'
                    downloaded += 1
                    log.write(msg + "\n")
                    # print (msg)
                    progress = int(count/n*100)
                    print (str(progress) + " % completed...    \r",)
                
    reflist.close
    
    msg = "Download/parsing complete for " + fld
    log.write(str(msg) + "\n")
    print (msg)
    msg = "Total files uploaded: ", downloaded, " of ", count
    log.write(str(msg) + "\n")
    print (msg)
    msg = "Removed as junk or unavailable: ", removed
    log.write(str(msg) + "\n")
    print (msg)
    msg = "Failed to download due to all errors: ", errors
    log.write(str(msg) + "\n")
    print (msg)

    log.close
    
# creating log folder
if not os.path.exists(os.path.dirname("logs/")):
    os.makedirs(os.path.dirname("logs/"))

log_gen = open("logs/" + dsetname + "_gen_log.txt", 'w')    

log_gen.write("Started downloading for " + str(len(nmlst)) + " classes. \n")
print ("Started downloading for " + str(len(nmlst)) + " classes.")    
    
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
    
    # CALLING function to UPLOAD    
    uploading(data_set_name, ref_list_class_name, class_filename, class_directory_name, logfile_class_name)
    
    log_gen.write("done with " + inst + "\n")
    print ("done with " + inst)
    print ("*********************************************************")

print ("Dataset has not been equalised!")
print ("Please use equaliser.py to complete equalisation.")
