VERBOSE = 1    # '0' only prints final results; 1 prints intermediate results 
# Inputs to be provided
Units = "SI"  # "Imperial" = inches,feet,psi,deg.F; "SI" = cm,meters,KPa,deg.C
# Input provided below must match selection above
# Rocket and Launch Site Specs
MaxV = 457.2       # maximum predicted rocket velocity
AMaxV = 4267.2     # predicted altitude at predicted maximum rocket velocity (AGL)
LSA = 1371.6       # launch site altitude (ASL)
TLS = 18.333       # Temp (Fahrenheit or Centigrade, depending upon selected units)
DEF = "DST"        # Use Default Sea-Level Temp ("DST") or Launch Site Temp ("LST")
#Fin Specs
Thickness = 0.47625   # Fin Thickness
TC = 6.35             # if TC == -1, calculate TC (or a Pseudo TC)
RC = 19.05            # Root Chord length
Height = 7.62         # Fin Height
GE = 4136854          # Shear Modulus
T2T  = "YES"          # Tip-to-Tip reinforcing present? "YES" or "NO"
Fin_Vertex_File_Name = "trap_SI.csv" # Name of csv file output from OpenRocket
# End of Inputs

