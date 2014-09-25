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



def main(args):

    # t1Directory, file_input_address grep
    if args.directory:
        FS_out_address,file_input_address = findT1Dir(args.directory,
                                                   args.nifti)
    elif args.cwd:
        FS_out_address,file_input_address = findT1Dir(os.getcwd(),
                                                   args.nifti)
    elif args.file_input:
        FS_out_address,file_input_address = (os.path.dirname(args.file_input),
                                          args.file_input)
    else:
        sys.exit('Please specify one of the input options, [-i, -c, -d] or --help')

    if args.output:
        FS_out_address = os.path.dirname(args.output)
        FS_out_name = os.path.basename(args.output)
    else:
        FS_out_name = 'FREESURFER'

    #for server
    #if 'dicom' in FS_out_address:
        #FS_out_address = os.path.dirname(os.path.dirname(t1Directory))

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

    with open('{0}/freesurferLog.txt'.format(FS_out_address),'w') as f:
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
            help='Output directory')

    args = parser.parse_args()

    # Check for the double selection of the options
    if args.directory and args.file_input:
        sys.exit('Please choose one of the input options')
    elif args.directory and args.cwd:
        sys.exit('Please choose one of the input options')
    elif args.file_input and args.cwd:
        sys.exit('Please choose one of the input options')
    else:
        main(args)
