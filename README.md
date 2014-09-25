usage: freesurfer.py [-h] [-n] [-i FILE_INPUT] [-c] [-d DIRECTORY] [-o OUTPUT]

freesurfer.py : Runs freesurfer recon-all -all
====================
eg) freesurfer.py
    eg) freesurfer.py --dir /Users/kevin/NOR04_CKI

    optional arguments:
    -h, --help            Show this help message and exit
    -n, --nifti           Allows nifti input
    -i FILE_INPUT, --file_input FILE_INPUT
                          Specify the input(dicom or nifti)
    -c, --cwd             Search all 'T1' directory and run freesurfer under the
                          current location
    -d DIRECTORY, --directory DIRECTORY
                          Data input directory location
    -o OUTPUT, --output OUTPUT
                          Output directory
