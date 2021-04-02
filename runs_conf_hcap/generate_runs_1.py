"""
Generate a par_* and sbatch* scripts + the queueing script
"""
import os
import shutil
import stat


# @ HARISMA
ROOT = "~/SAW/conf/"

# @ duneyrr
#ROOT = "~/sweethome/ferm/worm_disord/"

ROOT = os.path.expanduser(ROOT)


SLURM_TEMPLATE = \
r"""#!/bin/bash
#SBATCH --job-name=%(suffix)s
#SBATCH -n 1
#SBATCH -t 7-00:00

~/SAW/conf/a.out %(suffix)s > out%(suffix)s
"""


def get_suffix(dct):
    return "_U%(U)sL%(L)s" % dct


def read_par_template(fname):
    with open(fname, 'r') as f:
        template = f.read()
    return template


base_dct = {"L": 500, "U": "0.5", }  # physical
#            "seed1": 4836, "seed2": 2738,
#            "replica" : "1",
#            "cnf": 0, "stat": 0, "therm": "1e2",   # new or restart
#            "step_p": "5d8", "step_w": "5d8",      # printout/checkpoint
#       }


par_template = read_par_template("par_L500.clean.template")

slurmfnames = []

for L in [250, 500, 1000]:
#    for U in [0.5, 0.55, 0.6, 0.65, 0.7, 0.8]:
    for U in [0.62, 0.64, 0.66, 0.68 ]:
        dct = base_dct.copy()
        dct["L"] = L
        dct["U"] = U
        dct["suffix"] = get_suffix(dct)

        parfname = "par%s" % dct["suffix"]
        with open(parfname, "w") as parf:
            parf.write(par_template % dct)

        slurmfname = "slurm%s.sbatch" % dct["suffix"]
        with open(slurmfname, "w") as sf:
            sf.write(SLURM_TEMPLATE % dct)
        slurmfnames.append(slurmfname)


for sf in slurmfnames:
    print("sbatch " + sf)



'''


def write_out_one(base_dct, replica, par_template):
    """Write out a single par/slurm file, return the sbatch line."""

    dct = base_dct.copy()
    target_path = os.path.join(ROOT, "runs_conf_hcap" % dct)

    # write out the par file
    parfname = "par_%s" % dct["suffix"]
    parfname = os.path.join(target_path, parfname)
    
    with open(parfname, "w") as parf:
        parf.write(par_template % dct)

    # sanity check:
    # FIXME
    if float(dct["stat"]) != 0 and float(dct["therm"]) != 0:
        print("!!! ", parfname, "stat & therm")

    # write out the slurm file
    slurmfname = "slurm_%s.sbatch" % dct["suffix"]
    slurmfname = os.path.join(target_path, slurmfname)
    with open(slurmfname, "w") as sf:
        sf.write(SLURM_TEMPLATE % dct)
    
    # chmod u+x for SLURM
    st = os.stat(slurmfname)
    os.chmod(slurmfname, st.st_mode | stat.S_IEXEC)
    
    # copy the replica over
    r_path = "disord_L%sr%s.dat" % (dct["L"], replica)
    r_path = os.path.join(replicas_store, r_path)
    shutil.copy(r_path,
                os.path.join(target_path, "disord_%s.dat" % dct["suffix"]))
    # FIXME: create a replica if not exists

    return slurmfname


def read_par_template(fname):
    with open(fname, 'r') as f:
        template = f.read()
    return template


#########################################
if __name__ == "__main__":

    sbatch_files = []
    
    for replica in range(1, 3):
        dct = base_dct.copy()
        dct["replica"] = replica
        dct["seed2"] += replica
        dct["suffix"] = get_suffix(dct)
        
        # write out the par file
        parfname = "par_%s" % dct["suffix"]
        parfname = os.path.join(TARGET_PATH, parfname)
        
        with open(parfname, "w") as parf:
            parf.write(PAR_TEMPLATE % dct)
        
        # write out the slurm file
        slurmfname = "slurm_%s.sbatch" % dct["suffix"]
        slurmfname = os.path.join(TARGET_PATH, slurmfname)
        with open(slurmfname, "w") as sf:
            sf.write(SLURM_TEMPLATE % dct)
        sbatch_files.append(slurmfname)
        
        # chmod u+x for SLURM
        st = os.stat(slurmfname)
        os.chmod(slurmfname, st.st_mode | stat.S_IEXEC)
        
        # copy the replica over
        r_path = "disord_L%sr%s.dat" % (dct["L"], replica)
        r_path = os.path.join(REPLICAS_STORE, r_path)
        shutil.copy(r_path,
                    os.path.join(TARGET_PATH, "disord_%s.dat" % dct["suffix"]))

    # write out the run file to queue them all
    for sf in sbatch_files:
        print("sbatch " + sf)
        
'''

