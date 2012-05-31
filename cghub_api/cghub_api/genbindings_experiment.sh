URI='ftp://ftp.sra.ebi.ac.uk/meta/xsd/sra_1_3/SRA.experiment.xsd'
PREFIX='experiment'

mkdir -p ${PREFIX}
mkdir -p ${PREFIX}/raw

touch raw/__init__.py
pyxbgen \
   -m "${PREFIX}" \
   -u "${URI}" \
   --binding-root "${PREFIX}" \
   -r 

if [ ! -f ${PREFIX}/__init__.py ] ; then
  echo "from raw.${PREFIX} import *" > ${PREFIX}/__init__.py
fi
