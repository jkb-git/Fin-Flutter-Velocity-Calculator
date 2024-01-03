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
TC = 0              # TC = 0 for triangular fin; if TC == -1, calculate TC/Pseudo TC)
RC = 7.5            # Root Chord length
Height = 3          # Fin Height
GE = 600000         # Shear Modulus
T2T  = "NO"         # Tip-to-Tip reinforcing present? "YES" or "NO"
Fin_Vertex_File_Name = "tri.csv" # Name of csv file output from OpenRocket
# End of Inputs

