import scipy.io as sio
import numpy as np
import matplotlib.pyplot as plt
import os
import itertools
import collections
from mpl_toolkits import mplot3d
import matplotlib.pyplot as plt
from matplotlib import cm
from stl import mesh

                                                     
filefolder = '/home/isobel/Documents/McMaster/MATLABSimulation/SRR_1/bl_75nm/'

filename = (
            'Charges_1902meV_(125,0)',            
            #'Map_1003meV',
            #'Map_1890meV',
            #'Map_2000meV',
            #'Map_2170meV',
            #'Map_2310meV',
            #'Map_2400meV',
            #'Map_2510meV',
            )


mEELS = collections.OrderedDict()
mCL = collections.OrderedDict()
lEELS = collections.OrderedDict()
lCL = collections.OrderedDict()
labels = iter((
                '1.902 eV',
                #'1.003 eV',
                #'1.890 eV',
                #'2.000 eV',
                #'2.170 eV',
                #'2.310 eV',
                #'2.400 eV',
                #'2.510 eV',
                ))

for ff in filename:

    m = sio.loadmat(str(os.path.join(filefolder, ff)), appendmat=True, struct_as_record=False)
    #mEELS[ff] = Image.Image(np.transpose(np.reshape(np.squeeze(m['psurf'] + m['pbulk']), m['x'].shape[::-1])))
    #mEELS[ff] = Image.Image(np.transpose(np.reshape(np.squeeze(m['sca1']), m['x'].shape[::-1])))
    faces = m['faces']
    verts = m['verts']
    charges = m['sig1_charges']
    #sCL[ff] = Spectrum.EELSSpectrum(np.squeeze(m['sca1']), SpectrumRange=np.squeeze(m['ene']), ZLP=False)
    #label = labels.next()
    #lEELS[ff] = label + ' (EELS)'
    #lCL[ff] = label + ' (CL)'
charge = charges.real.squeeze()
#r = 0.237 - 2.13*charge + 26.92*charge**2 - 65.5*charge**3+63.5*charge**4 - 22.36*charge**5
#g = ((0.572+1.524*charge-1.811*charge**2)/(1-0.291*charge+0.1574*charge**2))**2
#b = 1/(1.579-4.03*charge+12.92*charge**2-31.4*charge**3+48.6*charge**4-23.36*charge*5)
#rgb = np.transpose(np.squeeze(np.array([r, g, b])))

meshfile = '/home/isobel/Documents/McMaster/MatlabCodes/SRR_1/SRR1_bl5_subsurf3.stl'
SRRmesh = mesh.Mesh.from_file(meshfile)



fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
##ax.plot_surface(verts[:, 0], verts[:, 1], verts[:, 2])
###ax.plot_surface(mesh.v0, mesh.v1, mesh.v2)
##print(verts[:, 0].shape)
##axes = mplot3d.Axes3D(fig)

poly = mplot3d.art3d.Poly3DCollection(verts=SRRmesh.vectors)
#surf = axes.plot_trisurf(verts[:,0], verts[:,1], verts[:,2], triangles=faces)
ax.add_collection3d(poly)
scale = SRRmesh.points.flatten(-1)
ax.auto_scale_xyz(scale, scale, scale)
print(scale.shape)
print(np.max(SRRmesh.points))

Z = np.random.random(4864)

maxcolour = np.max(np.abs(charge))
chargeplus = (charge/maxcolour + 1)/2
print(np.max(chargeplus), np.min(chargeplus))
#colourscale = chargeplus/maxcolour

#poly.set_edgecolor('k')

poly.set_facecolors(cm.seismic(chargeplus))
face = faces[:, :-1].astype(int)

#print(face.shape, verts.shape)
#face_centers = (verts[::3, :] + verts[1::3, :] + verts[2::3, :])/3
#print(face_centers.shape)

#	

##verts2 = np.unique(verts, axis=0)[:-2, :]
##x = verts2[:, 0].reshape(64, 38)
###x2 = np.unique(verts, axis=0)
##y = verts2[:, 1].reshape(64, 38)
##z = verts2[:, 2].reshape(64, 38)

#X, Y = np.meshgrid(face_centers[:,0], face_centers[:,1])
#x = face_centers[:, 0].reshape(32, 152)
#y = face_centers[:, 1].reshape(32, 152)
#z = face_centers[:, 2].reshape(32, 152)
#V = np.random.random(z.shape)
##V = charge.reshape((64, 38))

#surf = ax.plot_surface(x, y, z, facecolors=cm.RdBu(V))
#fig.patch.set_facecolor('k')
#ax.patch.set_facecolor('k')
plt.axis('off')
plt.show()
