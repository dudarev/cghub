FILE='../data/schemas/SRA.run.xsd'
PREFIX='run'

pyxbgen \
   -m "${PREFIX}" \
   -u "${FILE}" \
   --archive-path .:+ \
