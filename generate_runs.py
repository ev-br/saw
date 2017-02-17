from __future__ import division, print_function, absolute_import

par_stub = """\
spins_only_v0
2       ! dimensionality
%(latt)s     ! Lattice size
%(L)s      ! L
%(U)s      ! U/T
%(J)s       ! J/T
0       ! 0 if new configuration, 1 if old one
0       ! 0 if new statistics,    1 if old one
0.0d0  ! initial U
22      ! * L**2 steps of thermallization 
1.d7    ! step for printing
1.d7    ! step for writing to disk
1000.d0    ! step for measuring, 'expensive'
0.4d0     ! move probability
0.2d0     ! reconnect probability
18.9       ! time limit, hrs
4836 2748  ! seeds for the random number generator

"""


run_tag_stub = "U%(U)sJ%(J)sL%(L)s"


par_fname_stub = "par_%(tag)s"


run_line_stub = """\
sbatch  -J %(tag)s -t %(time_mins)s -o %(tag)s.out -e %(tag)s.err --mem=2000 -n 1 run ../saw_spins_only _%(tag)s
"""


LATTICE_SIZE = 350
TIME_LIMIT = 24*60


RUN_STR = "XXX"
Us = [1.1]
Ls = [1600, 3600]
Js = [0.4, 0.5]

with open("run_%s" % RUN_STR, "w") as run_file:
    for U in Us:
        for L in Ls:
            for J in Js:
                subs = {"latt": LATTICE_SIZE,
                        "time_mins": TIME_LIMIT,
                        "U": U, "J": J, "L": L}
                tag = run_tag_stub % subs
                subs.update(**{"tag": tag})

                par_fname = par_fname_stub % subs
                with open(par_fname, 'w') as f:
                    f.write(par_stub % subs)

                run_file.write(run_line_stub % subs)

                print("********* ", par_fname_stub % subs)

