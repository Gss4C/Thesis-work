'''import argparse

parser = argparse.ArgumentParser(description='Plot efficienze e significance')
parser.add_argument('-significance',
                    dest     = "significance",   
                    type     = int,
                    help     = 'True/False: if true, the program will calculate significances and will write a csv which resume everything', 
                    required = True)
options      = parser.parse_args()
significance = options.significance

print(significance)
if significance:
    print("ok funz")
else:
    print('anche il false funz')'''

import argparse

parser = argparse.ArgumentParser(description='Plot efficienze e significance')
parser.add_argument('-s', '--significance',
                    type     = int,
                    help     = 'True/False: if true, the program will calculate significances and will write a csv which resume everything', 
                    required = True)
options      = parser.parse_args()

print(options.significance)
if options.significance:
    print("ok funz")
else:
    print('anche il false funz')