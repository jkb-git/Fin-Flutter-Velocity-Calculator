# Fin-Flutter-Velocity-Calculator
Calculates the velocity at which rocket fins are likely to experience "flutter,"
the velocity beyond which catastrophic fin failure is probable due to aerodynamically
induced undampened fin oscillation. Read the accompanying article 
"Calculating_Fin_Flutter_Velocity_Bennett-12-25.pdf" for guidance on how to use the spreadsheet. 

The companion article "Calculating_Fin_Flutter_Velocity_For_Complex_Fin_Shapes.pdf"
describes how to apply these techniques to fin shapes other than trapezoids or ellipses.
Python source code to perform these calculations is in the "src" directory. This code 
is described in some detail in the companion article. Example input configuration
files for all fin examples used in both articles can be found in the "Examples" directory.

Note: the initial versions of the spreadsheet and the accompanying article
(including the one that appeared in "Peak of Flight") had two errors:
incorrect setting of initial conditions when using the optional feature of
offsetting temperature and pressure to account for local launch site conditions, and 
incorrect altitude of maximum velocity in the worked example. These errors have
been corrected in both the spreadsheet and the accompanying article.
