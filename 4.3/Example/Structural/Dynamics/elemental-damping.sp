node 1 0 0
node 2 1 0
node 3 0 0
node 4 1 0

material Elastic1D 1 100

element T2D2 1 1 2 1 1
element Mass 2 2 4 1

element T2D2 3 3 4 1 1
element Mass 4 4 4 1

fix 1 1 1 3
fix 2 2 1 2 3 4

plainrecorder 1 Node U1 2 4

modifier ElementalLee 1 .05 1 2
modifier ElementalLee 2 .2 3 4

step static 1 1
set ini_step_size .1
set fixed_step_size 1

displacement 1 0 .2 1 2 4

converger RelIncreDisp 1 1E-10 3 1

step dynamic 2 6
set ini_step_size .02
set fixed_step_size 1

integrator LeeElementalNewmark 1 .25 .5 1 5

converger RelIncreDisp 2 1E-10 3 1

analyze

save recorder 1

exit