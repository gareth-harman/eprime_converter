import os
import argparse
import sys

def print_usage():

    print('\n---:Edat Converter:---\n')
    print('Written: 04-20-2018 - Gareth Harman')
    print('\nConverts all .edat files into .txt or csv files\n')
    print('--Arguments--\n')
    print('  -eprime => Path to Eprime executible')
    print('  -data   => Path to all .edat files')
    print('  -out    => Output path for .txt/.csv files if not specified dame as -data')
    print('  -format => Defaults to .txt but but will take "csv" as well')
    print('\nex.\npython auto_EPRIME.py -u "C:/Users/Program Files(x86)/Eprime... -data "C:/Users/documents/my_data/"\n\t')
    print('\nNOTES: \n')
    print(' * Paths must include quotes')
    print(' * Options for format = txt or csv')
    print(' * If using \ as filesep make sure last filesep is \\')
    print(' * Watch spaces in file paths')


def parse_func(args):
    parser = argparse.ArgumentParser(
            description = 'Test Arg Parser: ',
            usage = 'Arg Parser for SCAN_INIT')
            
    parser.add_argument('-eprime', dest = 'eprime', help = 'Path to Eprime')
    parser.add_argument('-data', dest = 'data_dir', help = 'Path to .edat files')
    parser.add_argument('-out', dest = 'out_dir', help = 'Path to put outfiles')
    parser.add_argument('-format', dest = 'format_type', help = 'Output Format')
    
    return parser.parse_args(args)

parser_results = parse_func(sys.argv[1:])
EPRIME_DIR = parser_results.eprime
PARENT_DIR = parser_results.data_dir
OUT_DIR = parser_results.out_dir
FORMAT_TYPE = parser_results.format_type

#------------------------------------------------------------------------------

# QUICKLY CHECK FORMAT TYPE

if FORMAT_TYPE.lower() in '.csv':
    FORMAT_TYPE = '.csv'
else:
    FORMAT_TYPE = '.txt'

print('\nEprime Path: {}'.format(EPRIME_DIR))
print('Data Path: {}'.format(PARENT_DIR))
print('Output Path: {}\n'.format(OUT_DIR))

#------------------------------------------------------------------------------

# Check EPRIME path
def check_eprime(EPRIME_DIR):

    if len(sys.argv) == 1:
        print_usage()
        sys.exit(0)

    if EPRIME_DIR != None:
        if EPRIME_DIR[0] == '"' and EPRIME_DIR[-1] == '"':
            if os.path.isfile(EPRIME_DIR[1:-1]):
                return 1
            else:
                return 0
        else:
            return 0
    else:
        return 0
    
eCHECK = check_eprime(EPRIME_DIR)

if eCHECK == 0:
    # If eprime path not specificed check if it exists in typical location
    constE = '"C:/Program Files (x86)/PST/E-Prime 2.0/program/E-DataAid.exe"'
    if os.path.isfile(constE[1:-1]):
        EPRIME_DIR = constE
    else:
        print('Invalid EPRIME file location: Exiting...')
        print_usage()
        sys.exit(0)
else:
    print('Invalid EPRIME file location: Exiting...')
    print_usage()
    sys.exit(0)

#------------------------------------------------------------------------------

# Quotes needed for argparse but then remove them


if PARENT_DIR != None:

    if PARENT_DIR[-1] == '"' and PARENT_DIR[0] == '"':
        PARENT_DIR = PARENT_DIR[1:-1]
    if PARENT_DIR[-1] not in ['\\', '/']:
        PARENT_DIR += '\\'

    if not os.path.isdir(PARENT_DIR) and not os.path.isdir(PARENT_DIR[1:-1]):
        print('Invalid DATA path: Exiting...')
        print_usage()
        sys.exit(0)
else:
    print('Invalid DATA path: Exiting...')
    print_usage()
    sys.exit(0)

#------------------------------------------------------------------------------

# Check OUT_DIR if not working cast to DATA_DIR
if OUT_DIR == None:
    OUT_DIR = PARENT_DIR
else:
    if not os.path.isdir(OUT_DIR):
        print('Invalid OUT path: Outing to DATA path')
        OUT_DIR = PARENT_DIR

    if OUT_DIR[-1] == '"' and OUT_DIR[0] == '"':
        OUT_DIR = OUT_DIR[1:-1]
    if OUT_DIR[-1] not in ['\\', '/']:
        OUT_DIR += '\\'

#------------------------------------------------------------------------------

file_list = []

for ii in os.listdir(PARENT_DIR): # Get all edat files in -data
    if ii[-4:] == 'edat' or ii[-5:] == 'edat2':
        file_list.append(ii)

if len(file_list) == 0: # Error if no edats (.edat2 and .edat)
    print('No .edat files found: Exiting...')
    print_usage()
    sys.exit(0)

#------------------------------------------------------------------------------

# Create .txt command to execute conversion of EPRIME
# Calls program without splash and runs conversion

bulk = ['Inheritance=true',
        'InFile=in_VAL',
        'OutFile=out_VAL',
        'ColFlags=0',
        'ColNames=1',
        'Comments=0',
        'BegCommentLine=',
        'EndCommentLine=',
        'DataSeparator=\t',
        'VarSeparator=\t',
        'BegDataLine=',
        'EndDataLine=',
        'MissingData=',
        'Unicode=1']

CMD = EPRIME_DIR + '/e /f '

#------------------------------------------------------------------------------
# Process each edat

for ii in file_list:
    bulk[1] = bulk[1].replace('in_VAL', (PARENT_DIR + ii))
    bulk[2] = bulk[2].replace('out_VAL', (OUT_DIR + ii.split('.')[0] + FORMAT_TYPE))
   
    if '/' in bulk[2]:
        print('Writing: {}'.format(bulk[2].split('/')[-1]))
    elif '\\' in bulk[2]:
        print('Writing: {}'.format(bulk[2].split('\\')[-1]))
    else:
        print('Writing: {}'.format(bulk[2]))
        
    with open(OUT_DIR + 'cmd.txt', 'w') as f:
        for jj in bulk:
            f.write(jj + '\n')
            
    bulk[1] = 'InFile=in_VAL'
    bulk[2] = 'OutFile=out_VAL'
    
    os.system(CMD + OUT_DIR + 'cmd.txt')

print('\nCOMPLETED EDAT CONVERSION SUCCESSFULLY')

