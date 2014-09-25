#!/ccnc_bin/venv/bin/python2.7
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
                        if len(files)==1:
                            t1Dcm = files[0]
                        else:
                            t1Dcm = [x for x in files if x.startswith('co')][0]
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
    if args.file_input:
        outDirectory = os.path.dirname(args.file_input)
        os.environ["FREESURFER_HOME"] = '/Applications/freesurfer'
        os.environ["SUBJECTS_DIR"] = '{0}'.format(outDirectory)
        command = 'recon-all \
                -all \
                -i "{file_input}" \
                -subjid FREESURFER'.format(file_input=args.file_input)
        command = re.sub('\s+',' ',command)
        print command
        sys.exit('Done')
        #freesurferScreenOutput = os.popen(command).read()

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
    parser.add_argument('-n','--nifti',
            help="Allows nifti input",
            action='store_true')
    parser.add_argument('-i','--file_input',
            help="Specify the input(dicom or nifti)")
    parser.add_argument('-c','--cwd',
            help="Search all 'T1' directory and run freesurfer under the current location",
            action='store_true')
    parser.add_argument('-d','--directory',
            help='Data input directory location')
    parser.add_argument('-o','--output',
            help='Output directory full name',default='FREESURFER')

    args = parser.parse_args()

    # If no options --> raise error
    if not args.nifti and \
        not args.file_input and \
        not args.cwd and \
        not args.directory:
        sys.exit('Please specify (at least an option)')

    else:
        main(args)
