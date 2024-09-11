# step

Please refer to the specific type of steps for details.

For any steps available, a default **asymmetric** **banded** dense storage is used. This storage scheme fits most
problems. The LAPACK driver used is `_gbsv()`. The main reason behind such a choice stems from two aspects.

1.  For 2D and 3D problems, most material models have asymmetric stiffness moduli. The global stiffness matrix is then
    asymmetric.
2.  If the problem shows softening behaviour, the stiffness matrix is not always positive definite, the symmetric solver
    fails to solve such a matrix.
