#!/Users/admin/anaconda/bin/python
# -*- coding: utf-8 -*-

import re
import sys
import os
import argparse
import textwrap


def findT1Dir(dir,nifti):
    #Regrex for T1
    t1 = re.compile(r'tfl|[^s]t1|t1',re.IGNORECASE)
    scout = re.compile(r'scout',re.IGNORECASE)

    try:
        for root,dirs,files in os.walk(dir):
            if t1.search(os.path.basename(root)) and not scout.search(os.path.basename(root)):
                if [x for x in files if not x.startswith('.')][0].endswith('nii.gz'): #if it's nifti directory
                    if nifti:
                        print root
                        t1Dcm = [x for x in files][0]
                        t1Directory = root
                        t1DcmAddress = os.path.join(t1Directory,t1Dcm)
                    else:
                        pass
                else: #if it's dicom directory
                    print root
                    t1Dcm = [x for x in files if not x.startswith('.')][-1]
                    t1Directory = root
                    t1DcmAddress = os.path.join(t1Directory,t1Dcm)
    except:
        sys.exit('Arrange T1 dicoms in the T1 directory')


    try:
        if t1DcmAddress and t1DcmAddress:
            return t1Directory,t1DcmAddress
    except:
        sys.exit('T1 directory not found')

def main(args):
    subjAddress = args.directory
    #print subjAddress
    t1Directory,t1DcmAddress = findT1Dir(subjAddress,args.nifti)

    if 'dicom' in t1Directory:
        outDirectory = os.path.dirname(os.path.dirname(t1Directory))
    else:
        outDirectory = os.path.dirname(t1Directory)

    os.environ["FREESURFER_HOME"] = '/Applications/freesurfer'
    os.environ["SUBJECTS_DIR"] = '{0}'.format(outDirectory)

    if args.nifti:
        freesurferScreenOutput = os.popen('recon-all -all -i "{t1DcmAddress}" -subjid FREESURFER'.format(
                t1DcmAddress=t1DcmAddress)).read()
    else:
        freesurferScreenOutput = os.popen('recon-all -all -i "{t1DcmAddress}" -subjid FREESURFER'.format(
                t1DcmAddress=t1DcmAddress)).read()

    with open('{0}/freesurferLog.txt'.format(outDirectory),'w') as f:
        f.write(freesurferScreenOutput)


if __name__=='__main__':
    parser = argparse.ArgumentParser(formatter_class=argparse.RawDescriptionHelpFormatter,
            description = textwrap.dedent('''\
                    {codeName} : Runs freesurfer recon-all -all
                    ====================
                        eg) {codeName}
                        eg) {codeName} --dir /Users/kevin/NOR04_CKI
                    '''.format(codeName=os.path.basename(__file__))))

            #epilog="By Kevin, 26th May 2014")
    parser.add_argument('-dir','--directory',help='Data directory location, default = pwd',default=os.getcwd())
    parser.add_argument('-n','--nifti',help="This option searches for 'T1' directory and uses co*.nii.gz within the T1 directory to run freesurfer",action='store_true')
    args = parser.parse_args()

    main(args)

