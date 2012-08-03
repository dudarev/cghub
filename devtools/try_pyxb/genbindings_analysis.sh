FILE='../data/schemas/1.4/SRA.analysis.xsd'
PREFIX='analysis'

pyxbgen \
   -m "${PREFIX}" \
   -u "${FILE}" \
   --archive-path .:+ \
