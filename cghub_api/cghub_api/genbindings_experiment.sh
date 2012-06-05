URI='ftp://ftp.sra.ebi.ac.uk/meta/xsd/sra_1_3/SRA.experiment.xsd'
PREFIX='experiment'

pyxbgen \
   -m "${PREFIX}" \
   -u "${URI}" \
   --archive-path .:+ \
