#!/bin/bash
#SBATCH --job-name=_U0.5L250
#SBATCH -n 1
#SBATCH -t 1-00:00

~/SAW/conf/a.out _U0.5L250 > out_U0.5L250
