#!/bin/bash
#SBATCH --job-name=_U0.8L500
#SBATCH -n 1
#SBATCH -t 7-00:00

~/SAW/conf/a.out _U0.8L500 > out_U0.8L500
