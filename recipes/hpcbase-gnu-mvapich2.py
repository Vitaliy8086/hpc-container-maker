"""
HPC Base image

Contents:
  CUDA version 9.0
  FFTW version 3.3.7
  GNU compilers (upstream)
  HDF5 version 1.10.1
  Mellanox OFED version 3.4-1.0.0.0
  MVAPICH version 2.3rc2
  Python 2 and 3 (upstream)
"""
# pylint: disable=invalid-name, undefined-variable, used-before-assignment

# Choose between either Ubuntu 16.04 (default) or CentOS 7
# Add '--userarg centos=true' to the command line to select CentOS
devel_image = 'nvidia/cuda:9.0-devel-ubuntu16.04'
runtime_image = 'nvidia/cuda:9.0-runtime-ubuntu16.04'
if USERARG.get('centos', False):
    devel_image = 'nvidia/cuda:9.0-devel-centos7'
    runtime_image = 'nvidia/cuda:9.0-runtime-centos7'

######
# Devel stage
######

Stage0 += comment(__doc__, reformat=False)

Stage0 += baseimage(image=devel_image, _as='devel')

# Python
python = python()
Stage0 += python

# GNU compilers
gnu = gnu()
Stage0 += gnu

# Setup the toolchain.  Use the GNU compiler toolchain as the basis.
tc = gnu.toolchain
tc.CUDA_HOME = '/usr/local/cuda'

# Mellanox OFED
ofed = mlnx_ofed(version='3.4-1.0.0.0')
Stage0 += ofed

# MVAPICH2
mv2 = mvapich2(version='2.3rc2', toolchain=tc)
Stage0 += mv2

# FFTW
fftw = fftw(version='3.3.7', toolchain=tc)
Stage0 += fftw

# HDF5
hdf5 = hdf5(version='1.10.1', toolchain=tc)
Stage0 += hdf5

######
# Runtime image
######

Stage1 += baseimage(image=runtime_image)

# Python
Stage1 += python.runtime()

# GNU compiler
Stage1 += gnu.runtime()

# Mellanox OFED
Stage1 += ofed.runtime()

# MVAPICH2
Stage1 += mv2.runtime()

# FFTW
Stage1 += fftw.runtime()

# HDF5
Stage1 += hdf5.runtime()
