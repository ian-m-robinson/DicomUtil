IANR - Task2 items 1-4
example use cases
1) python dcmutil.py dcmfile={filePath}
ie python dcmutil.py dcmfile=C:\DICOM\IANR.dcm

2) python dcmutil.py dcmfile={str(filePath)} updatename={str(newName)} updateage={int(Age)} updategender={str(gender)}
ie python dcmutil.py dcmfile=C:\DICOM\IANR.dcm updatename=JoeBloggs updateage=17 updategender=F

3) python dcmutil.py dcmfolder={str(folderPath)}
ie python dcmutil.py dcmfolder=C:\DICOM\brain

4) python dcmutil.py dcmfolder={str(folderPath)} applyage=str(True)}
ie python dcmutil.py dcmfolder=C:\DICOM\brain applyage=true
