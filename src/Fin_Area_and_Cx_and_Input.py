# © 2024 John K. Bennett; BSD 2-Clause License
# (details at https://github.com/jkb-git/Fin-Flutter-Velocity-Calculator/blob/main/LICENSE)
import numpy as np
import matplotlib.pyplot as plt
import triangle as tr
import math
from pathlib import Path

# *** you must use the same name (e.g., "peregrine_rocket.py") in next four lines. i.e., 
    # peregrine_rocket = Path("peregrine_rocket.py")
    # if peregrine_rocket.is_file(): 	# if input file exists, use it
    #	# Read in the config file 
    #	from peregrine_rocket import *
peregrine_rocket = Path("peregrine_rocket.py")
if peregrine_rocket.is_file(): 	# if input file exists, use it
    # Read in the config file 
    from peregrine_rocket import *
else:  # no input file exists; initialize input variables here
    VERBOSE = 0    # '0' only prints final results; 1 prints intermediate results 
    # Inputs to be provided
    Units = "Imperial" # "Imperial" = inches,feet,psi,deg.F; "SI" = cm,meters,KPa,deg.C
    # Input provided below must match selection above
    # Rocket and Launch Site Specs
    MaxV = 1500         # maximum predicted rocket velocity
    AMaxV = 14000       # predicted altitude at predicted maximum rocket velocity (AGL)
    LSA = 4500          # launch site altitude (ASL)
    TLS = 65            # Temp (Fahrenheit or Centigrade, depending upon selected units)
    DEF = "DST"         # Use Default Sea-Level Temp ("DST") or Launch Site Temp ("LST")
    #Fin Specs
    Thickness = 0.1875  # Fin Thickness
    TC = 2.5             # if TC == -1, calculate TC (or a Pseudo TC)
    RC = 7.5            # Root Chord length
    Height = 3          # Fin Height
    GE = 600000         # Shear Modulus
    T2T  = "NO"         # Tip-to-Tip reinforcing present? "YES" or "NO"
    Fin_Vertex_File_Name = "trap.csv" # Name of csv file output from OpenRocket
# End of Inputs

# Read in the vertex file exported by OpenRocket (see articles for explanation)
verts = np.genfromtxt(Fin_Vertex_File_Name, delimiter=",")
verts = np.delete(verts, 0, 0)  # delete the header row of the csv file 
verts = np.delete(verts, 2, 1)  # delete third column of csv file (created by extra comma)  
segs = []                       # must specify segments and vertices to create a PSLG
for i in range (len(verts)):    # create segments of a closed PSLG from list of vertices
    seg = []
    seg.append(i)
    if (i == (len(verts)-1)):
        seg.append(0)
    else:
        seg.append(i+1)
    segs.append(seg)
tr_input = dict(vertices=verts, segments=segs)  # triangle expects Python dict as input
tr_output = tr.triangulate(tr_input,'p')        # make triangles. 'p' says input is a PSLG
tris = tr_output['triangles'].tolist()          # convert output of triangle to Python list 
# print("Number of Triangles Produced = ", len(tris))
# print (tris)
# print ("First Triangle Vertices = (", \
#        verts[1].tolist(), ", " , verts[0].tolist(), ", " , verts[20].tolist(),")")
# next two lines moved to end of file so plot can stay visible until closed
# tr.compare(plt, tr_input, tr_output)            # set up what we are going to plot
# plt.show()                                      # create the plot

# for each generated triangle, compute an area and a Cx
tri_areas = []      # this list will hold the area of each triangle  
tri_Cxs = []        # this list will hold the Cx of each triangle
fin_area = 0
fin_Cx = 0
for tri in tris:		# for every generated triangle
    A = verts[tri[0]]   # extract the vertices of this triangle
    B = verts[tri[1]]
    C = verts[tri[2]]
    # compute triangle area; 0 is index of vertex x coord; 1 is index of vertex y coord
    ar = ((A[0]*(B[1]-C[1])) + (B[0]*(C[1] - A[1])) + (C[0]*(A[1] - B[1])))/2
    tri_areas.append(ar)    # add the area of this triangle to our list of areas
    fin_area += ar          # add the area of this triangle to the total fin area
    # compute triangle Cx; 0 is the index of the vertex x coord
    tri_Cx = (A[0] + B[0] + C[0]) / 3
    tri_Cxs.append(tri_Cx)  # add the Cx of this triangle to our list of Cx's
# compute Fin Cx by taking the weighted average of all of the triangle Cx's 
for i in range(len(tri_areas)):  # first get the numerator (weighted sum of areas)
    fin_Cx += (tri_Cxs[i] * tri_areas[i])
fin_Cx = (fin_Cx / fin_area)     # now divide by the total fin area to get Cx

# Compute Vf; first compute all intermediate values
Fin_Eps = (fin_Cx / RC) - 0.25	# compute epsilon (see article for definition)
if (TC < 0):	# if TC is entered as -1, compute TC or pseudo TC
    TC = (((fin_area / Height) * 2) - RC)
ThicknessRatio = (Thickness / RC)	# compute three fin ratios
Lambda = (TC / RC)	# if TC = 0, Lambda will also be zero (triangular fin)
AspectRatio = ((Height * Height) / fin_area)
if (Units == "Imperial"):	# set constants and suffices to Imperial Units
    p0 = 14.696
    DST_Base_Temp = 59
    Temp_Dec_Per_Unit = 0.00356
    SoS_Mult = 49.03
    Low_Temp = 459.7
    T0 = 518.7
    velsuf = "ft/sec"
    finsuf = "in"
    altsuf = "feet"
    tempsuf = "deg F"
    GEsuf = "psi"
    areasuf = "sq in"
else: # set constants and suffices to SI Units
    p0 = 101.325
    DST_Base_Temp = 15
    Temp_Dec_Per_Unit = .0065
    SoS_Mult = 20.05
    Low_Temp = 273.16
    T0 = 288.16
    velsuf = "meters/sec"
    finsuf = "cm"
    altsuf = "meters"
    tempsuf = "deg C"
    GEsuf = "KPa"
    areasuf = "sq cm"
DN = (24 * Fin_Eps * 1.4 * p0) / math.pi	# compute "denominator constant"
if(DEF=="DST"):	# Use Default Sea-Level Temp ("DST") as base
    Temp = (DST_Base_Temp - (Temp_Dec_Per_Unit * (LSA + AMaxV)))
else:	# Use Launch Site Temp ("LST") as base
    Temp = (TLS-(Temp_Dec_Per_Unit * (AMaxV)))
Spd_of_Sound = SoS_Mult * math.sqrt(Low_Temp + Temp) # Compute speed of sound
airP = p0 * pow(((Temp  + Low_Temp)/T0),5.256)		 # Compute air pressure
Term1 = (DN * pow(AspectRatio, 3)) / (pow(ThicknessRatio, 3) * (AspectRatio + 2))
Term2 = (Lambda + 1)/2
Term3 = (airP / p0)
if (T2T == "YES"):	# if tip to tip reinforcing present, double GE
	GE = 2 * GE      
Vf = Spd_of_Sound * math.sqrt(GE/(Term1 * Term2 * Term3))
Margin = Vf - MaxV	# compute safety margin (see article)
Margin_Pct = 100 * ((Vf-MaxV)/MaxV)

# print the input for verification
print ("Unit System = ", Units)
# Rocket and Launch Site Specs, as provided
print ("****Rocket and Launch Site Specs****")
print ("MaxV = ", "{:2.1f}".format(MaxV), velsuf)
print ("AMaxV = ", "{:2.1f}".format(AMaxV), altsuf)
print ("LSA = ", "{:2.1f}".format(LSA), altsuf)
print ("TLS = ", "{:2.1f}".format(TLS), tempsuf)
print ("DEF = ", DEF)
print ("****Fin Specs****")
print ("RC = ", "{:2.3f}".format(RC), finsuf)
print ("Height = ", "{:2.3f}".format(Height), finsuf)
print ("Thickness = ", "{:2.4f}".format(Thickness), finsuf)
print ("TC = ", "{:2.3f}".format(TC), finsuf)
if (T2T == "YES"):
    print ("Tip-to-tip reinforcing present; GE doubled to: ","{:2.1f}".format(GE),GEsuf)
else:
    print ("GE = ","{:2.1f}".format(GE),GEsuf)
print ("T2T = ", T2T)
print ("Fin_Vertex_File_Name = ", Fin_Vertex_File_Name)
print()
if (VERBOSE): # print all the intermediate values, if VERBOSE is true
    print ("Fin Eps = ", "{:2.3f}".format(Fin_Eps))
    print ("TC or Pseudo TC = ", "{:2.2f}".format(TC), finsuf)
    print ("Thickness Ratio = ", "{:2.3f}".format(ThicknessRatio))
    print ("Lambda = ", "{:2.3f}".format(Lambda))
    print ("Aspect Ratio = ", "{:2.3f}".format(AspectRatio))
    print ("DN = ", "{:2.2f}".format(DN), GEsuf)
    print ("Temp at MaxV = ", "{:2.2f}".format(Temp), tempsuf)
    print ("Spd_of_Sound = ", "{:2.2f}".format(Spd_of_Sound), velsuf)
    print ("airP = ", "{:2.2f}".format(airP), GEsuf)
    print ("Term1 = ", "{:2.2f}".format(Term1), GEsuf)
    print ("Term2 = ", "{:2.2f}".format(Term2))
    print ("Term3 = ", "{:2.2f}".format(Term3))
# always print the important stuff
print ("Fin Area = ", "{:2.2f}".format(fin_area), areasuf)
print ("Fin Cx = ", "{:2.2f}".format(fin_Cx), finsuf)
print ("Vf = ", "{:2.1f}".format(Vf), velsuf)
print ("Margin = ", "{:2.1f}".format(Margin), velsuf)
print ("Margin% = ", "{:2.1f}%".format(Margin_Pct))
# plot moved to here so we wouldn't have to close plot to see results
tr.compare(plt, tr_input, tr_output)            # set up what we are going to plot
plt.show()                                      # create the plot
