#!/ccnc_bin/venv/bin/python2.7
# -*- coding: utf-8 -*-

import re
import sys
import os
import argparse
import textwrap

def walklevel(some_dir, level=1):
    some_dir = some_dir.rstrip(os.path.sep)
    assert os.path.isdir(some_dir)
    num_sep = some_dir.count(os.path.sep)
    for root, dirs, files in os.walk(some_dir):
        yield root, dirs, files
        num_sep_this = root.count(os.path.sep)
        if num_sep + level <= num_sep_this:
            del dirs[:]

def findT1Dir(dir,nifti):
    #Regrex for T1
    t1 = re.compile(r'tfl|[^s]t1|t1',re.IGNORECASE)
    scout = re.compile(r'scout',re.IGNORECASE)

    try:
        for root,dirs,files in walklevel(dir, level=1):
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
        toPrint = 'T1 directory not found, \
                or dicom is not found in T1 directory. \
                Use -n flag for nifti'
        sys.exit(re.sub('\s+',' ',toPrint))


def main(inputValue, output):
    if os.path.isdir(inputValue):
        FS_out_address = inputValue
        file_input_address = [x for x in os.listdir(inputValue) \
                if re.search('dcm|ima|nii.gz', x, re.IGNORECASE)][-1]
    else:
        FS_out_address = os.path.dirname(inputValue)
        file_input_address = inputValue

    os.environ["FREESURFER_HOME"] = '/Applications/freesurfer'
    os.environ["SUBJECTS_DIR"] = '{0}'.format(FS_out_address)

    command = 'recon-all \
            -all \
            -i "{file_input_address}" \
            -subjid {FS_out_name}'.format(file_input_address=file_input_address,
                                          FS_out_name=FS_out_name)

    command = re.sub('\s+',' ',command)
    print command

    freesurferScreenOutput = os.popen(command).read()


if __name__=='__main__':
    parser = argparse.ArgumentParser(formatter_class=argparse.RawDescriptionHelpFormatter,
            description = textwrap.dedent('''\
                    {codeName} : Runs freesurfer recon-all -all
                    ====================
                        eg) {codeName}
                        eg) {codeName} --dir /Users/kevin/NOR04_CKI
                    '''.format(codeName=os.path.basename(__file__))))

            #epilog="By Kevin, 26th May 2014")
    parser.add_argument('-i','--input',
            help='Input data either dicom, nifti or T1 directory',
            default=os.getcwd())
    parser.add_argument('-o','--output',
            help='Output directory',
            default='FREESURFER')

    args = parser.parse_args()

    # Check for the double selection of the options
    if not args.nifti and not args.dicom:
        sys.exit('Please choose one of the input options')
    else:
        main(args.input, args.output)
