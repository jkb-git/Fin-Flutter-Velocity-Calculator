# © 2024 John K. Bennett; BSD 2-Clause License
# (details at https://github.com/jkb-git/Fin-Flutter-Velocity-Calculator/blob/main/LICENSE)
import numpy as np
import matplotlib.pyplot as plt
import triangle as tr

# Read in the vertex file exported by OpenRocket
verts = np.genfromtxt("peregrinefins.csv", delimiter=",")
verts = np.delete(verts, 0, 0)  # delete the header row of the csv file 
verts = np.delete(verts, 2, 1)  # delete third column of csv file (created by extra comma)  
segs = []                       # must specify segments as well as verts to create a PSLG
for i in range (len(verts)):    # create segments of a closed PSLG from list of vertices
    seg = []
    seg.append(i)
    if (i == (len(verts)-1)):
        seg.append(0)
    else:
        seg.append(i+1)
    segs.append(seg)
tr_input = dict(vertices=verts, segments=segs)  # triangle expects a Python dict as input
tr_output = tr.triangulate(tr_input,'p')        # make triangles. 'p' = input is a PSLG
tris = tr_output['triangles'].tolist()          # convert output of triangle to Python list 
# tr.compare(plt, tr_input, tr_output)          # set up what we are going to plot
# plt.show()
# print ("Number of Triangles Produced = ", len(tris))
# print (tris)
# print("First Triangle Vertices = (", \
#       verts[1].tolist(), ", ", verts[0].tolist(), ", " , verts[20].tolist(),")")

# for each of our triangles, compute an area and a Cx
tri_areas = []      # this list will hold the areas of each triangle  
tri_Cxs = []        # this list will hold the Cx’s of each triangle
fin_area = 0
fin_Cx = 0
for tri in tris:
    A = verts[tri[0]]       #extract the vertices of this triangle
    B = verts[tri[1]]
    C = verts[tri[2]]
    # compute triangle area; 0 is the index of the x coord; 1 is the index of the y coord
    ar = ((A[0]*(B[1]-C[1])) + (B[0]*(C[1] - A[1])) + (C[0]*(A[1] - B[1])))/2
    tri_areas.append(ar)    # add the area of this triangle to our list of areas
    fin_area += ar          # add the area of this triangle to the total fin area
    # compute triangle Cx; 0 is the index of the x coord
    tri_Cx = (A[0] + B[0] + C[0]) / 3
    tri_Cxs.append(tri_Cx)  # add the Cx of this triangle to our list of Cx's
# compute Fin Cx by taking the weighted average of all of the triangle Cx's 
for i in range(len(tri_areas)):             # first get the numerator
    fin_Cx += (tri_Cxs[i] * tri_areas[i])   # use fin_Cx to hold intermediate result
fin_Cx = (fin_Cx / fin_area)                # now divide by the total fin area
print ("Fin Area = ", "{:2.2f}".format(fin_area))
print ("Fin Cx = ", "{:2.2f}".format(fin_Cx))



