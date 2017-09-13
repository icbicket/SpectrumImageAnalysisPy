import argparse
import os
import CLSet
import AlignLib
import AlignCrop
folder = 'T9-3_Sq1A_(1,3)'
filebase = 'T9-3_Sq1A_(1,3)h_Gr800at750_30keV_Ap3Spot4_2s_Slit12185um_'
#Code will break if files aren't named properly! Must have all QWP/Pol combinations!
# prefix_added_above + QWPstate_Polarizerstate + _full + .h5 (sample data)
# prefix_added_above + QWPstate_Polarizerstate + _dark + .h5 (dark reference)
# prefix_added_above + QWPstate_Polarizerstate + _SiN + .h5 (substrate reference)

folderbase = os.path.join('/home/isobel/Documents/McMaster/CL/', folder, filebase)
filetype = '.h5'
Polstates = ('QWP0_Pol0')
Sets = {}

Sets['QWP0_Pol0'] = CLSet.CLSet(folderbase + 'QWP0_Pol0' + '_full' + filetype,
                 folderbase + 'QWP0_Pol0' + '_dark' + filetype,
                 folderbase + 'QWP0_Pol0' + '_SiN' + filetype)
