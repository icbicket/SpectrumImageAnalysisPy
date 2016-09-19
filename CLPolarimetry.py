import argparse
import os
import CLSet
#FUTUREME: CLSet class file!
#Pol set file too!

# Input arguments to be entered by user in command line
parser = argparse.ArgumentParser(description='Calculate Stokes parameters.')
parser.add_argument('folder', type=str,
                    help='folder (inside CL) holding polarimetry files')
parser.add_argument('filebase',
                    help='file prefix for polarimetry files to analyze')

args = parser.parse_args()

#Code will break if files aren't named properly! Must have all QWP/Pol combinations!
# prefix_added_above + QWPstate_Polarizerstate + _full + .h5 (sample data)
# prefix_added_above + QWPstate_Polarizerstate + _dark + .h5 (dark reference)
# prefix_added_above + QWPstate_Polarizerstate + _SiN + .h5 (substrate reference)
folderbase = os.path.join('/home/isobel/Documents/McMaster/CL/', args.folder, args.filebase)
filetype = '.h5'
Polstates = ('QWP0_Pol0', 'QWP315_Pol45', 'QWP270_Pol45', 'QWP270_Pol90', 'QWP270_Pol135', 'QWP45_Pol135')
Sets = {}

for pp in Polstates:
	Sets[pp] = CLSet.CLSet(folderbase + pp + '_full' + filetype,
	                 folderbase + pp + '_dark' + filetype,
	                 folderbase + pp + '_SiN' + filetype)

Polarization = CLSet.PolarimetrySet(Sets)
