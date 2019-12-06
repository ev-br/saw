FF = gfortran -O2

spins:
	$(FF) saw_mar8.f90 cluster_mar8.f90 rndm_mumbers.f
