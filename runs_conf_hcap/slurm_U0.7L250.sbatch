#!/bin/bash
#SBATCH --job-name=_U0.7L250
#SBATCH -n 1
#SBATCH -t 7-00:00

~/SAW/conf/a.out _U0.7L250 > out_U0.7L250
