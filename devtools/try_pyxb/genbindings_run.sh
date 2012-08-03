FILE='../data/schemas/1.4/SRA.run.xsd'
PREFIX='run'

pyxbgen \
   -m "${PREFIX}" \
   -u "${FILE}" \
   --archive-path .:+ \
