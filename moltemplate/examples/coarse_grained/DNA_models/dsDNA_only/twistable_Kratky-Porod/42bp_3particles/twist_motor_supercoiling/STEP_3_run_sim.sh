# --- Running LAMMPS ---
#  -- Prerequisites: --
# The "run.in.nvt" file is a LAMMPS input script containing
# references to the input scripts and data files
# you hopefully have created earlier with moltemplate.sh:
#   system.in.init, system.in.settings, system.data
# If not, carry out the instructions in "README_setup.sh".
#
#  -- Instructions: --
# If "lmp_mpi" is the name of the command you use to invoke lammps,
# then you would run lammps on these files this way:


lmp_mpi -i run.in.min
lmp_mpi -i run.in



# If you have compiled the MPI version of lammps, you can run lammps in parallel
#mpirun -np 8 lmp_mpi -i run.in
# (assuming you have 8 processors available)