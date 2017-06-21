folder=$1
ABSPAT=$(readlink -f ${folder})
export PATH=${ABSPAT}/SEECER-0.1.3/SEECER/bin/:$PATH
export PATH=${ABSPAT}/oases/:$PATH
export PATH=${ABSPAT}/velvet/:$PATH
export PATH=${ABSPAT}/Sailfish-0.6.2-Linux_x86-64/bin/:$PATH
