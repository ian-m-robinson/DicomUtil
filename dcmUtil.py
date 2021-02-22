"""
IANR - Task2 items 1-4
example use cases
1) python dcmutil.py dcmfile=C:\DICOM\IANR.dcm
2) python dcmutil.py dcmfile=C:\DICOM\IANR.dcm updatename=JoeBloggs updateage=17 updategender=F
3) python dcmutil.py dcmfolder=C:\DICOM\brain
4) python dcmutil.py dcmfolder=C:\DICOM\brain applyage=true
"""

import sys
import pydicom
from datetime import datetime

inputArgs = {'dcmfile': None, 'dcmfolder': None, 'updatename': None, 'updateage': None, 'updategender': None, 'applyage': None}

if len(sys.argv) >= 2:
    for user_input in sys.argv[1:]:  # iterate over argv[1:] (argv[0] is the program name)
        if "=" not in user_input:
            'Args supplied are not in the correct format....  name=value'
            continue
        varname = user_input.split("=")[0]
        varname = varname.lower()
        varvalue = user_input.split("=")[1]
        if varname in inputArgs:
            inputArgs[varname] = varvalue
        else:
            print('\n@@@ Ignoring input Args: ', user_input)

        #print(inputArgs)
else:
    print("No options supplied")
    exit(0)

dcmFile = inputArgs.get("dcmfile")
dcmFolder = inputArgs.get("dcmfolder")
updateName = inputArgs.get('updatename')
updateAge = inputArgs.get('updateage')
updateGender = inputArgs.get('updategender')
applyAge = inputArgs.get('applyage')


### read and print ALL data ###
def readDcmTags(dcmFile, display):
    dataset = pydicom.filereader.dcmread(dcmFile)
    if display:
        print(dataset)
    return (dataset)


def modifyTags(dcmFile, updateName, updateAge, updateGender):
    dataset = readDcmTags(dcmFile, False)
    dataset.PatientName = updateName
    dataset.PatientSex = updateGender
    dataset.PatientAge = updateAge
    print("Updated: Name:{} - Gender:{} - Age:{}".format(dataset.PatientName, dataset.PatientSex, dataset.PatientAge))
    ### Update / write DCM file
    dataset.save_as(dcmFile, True)
    ### Verify save is correct
    updateDataset = readDcmTags(dcmFile, False)
    print("NewRead: Name:{} - Gender:{} - Age:{}".format(updateDataset.PatientName, updateDataset.PatientSex, updateDataset.PatientAge))

def updateFolderContentMetadata(dcmFolder):
    current_date = datetime.today().strftime('%Y%m%d')
    current_time = datetime.today().strftime('%H%M%S')
    print("Current Date: {} Time: {}".format(current_date, current_time))

    for file in os.listdir(dcmFolder):
        current_file = os.path.join(dcmFolder, file)
        folderFileData = pydicom.filereader.dcmread(current_file)
        print("Current Content Metadata: ", current_file, folderFileData.ContentDate, folderFileData.ContentTime)
        folderFileData.ContentDate = current_date
        folderFileData.ContentTime = current_time
        #Save data back
        folderFileData.save_as(current_file, True)
        #reload to verify
        updatedFileData = pydicom.filereader.dcmread(current_file)
        print("Updated Content Metadata: ", current_file, updatedFileData.ContentDate, updatedFileData.ContentTime)

def getAge(PatientBirthDate, StudyDate):
    BirthDate = datetime.strptime(PatientBirthDate, "%Y%m%d")
    StudyDate = datetime.strptime(StudyDate, "%Y%m%d")
    Age = StudyDate - BirthDate
    return (int(Age.days/365.25))

def applyPatientAgeAtStudyDate(dcmFolder):
    for file in os.listdir(dcmFolder):
        current_file = os.path.join(dcmFolder, file)
        folderFileData = pydicom.filereader.dcmread(current_file)
        print("Current File:{}   Age:{}   DOB:{}   Study:{}".format( current_file, folderFileData.PatientAge, folderFileData.PatientBirthDate, folderFileData.StudyDate))
        ageAtStudy = getAge(folderFileData.PatientBirthDate, folderFileData.StudyDate)
        folderFileData.PatientAge = str(ageAtStudy)
        #Save data back
        folderFileData.save_as(current_file, True)
        #reload to verify
        updatedFileData = pydicom.filereader.dcmread(current_file)
        print("Updated File:{}   Age:{}   DOB:{}   Study:{}".format( current_file, updatedFileData.PatientAge, updatedFileData.PatientBirthDate, updatedFileData.StudyDate))


## read tags only ##
if dcmFile and dcmFolder==None and updateName==None and updateAge==None and updateGender==None and applyAge==None:
    readDcmTags(dcmFile, True)

## modify tags as ##
if dcmFile and updateName and updateAge and updateGender:
    modifyTags(dcmFile, updateName, updateAge, updateGender)

## modify Multiple Files from folder ##
if dcmFolder and not dcmFile and not applyAge:
    updateFolderContentMetadata(dcmFolder)

## modify Age based on Study Date across folder ##
if applyAge != None:
    applyAge=applyAge.lower()
    if dcmFolder and applyAge=="true" and not dcmFile:
        applyPatientAgeAtStudyDate(dcmFolder)

