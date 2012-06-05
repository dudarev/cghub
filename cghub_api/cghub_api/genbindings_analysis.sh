FILE='SRA.analysis.xsd'
PREFIX='analysis'

pyxbgen \
   -m "${PREFIX}" \
   -u "${FILE}" \
   --archive-path .:+ \
