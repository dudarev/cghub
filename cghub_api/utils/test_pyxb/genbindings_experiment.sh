FILE='../data/schemas/SRA.experiment.xsd'
PREFIX='experiment'

pyxbgen \
   -m "${PREFIX}" \
   -u "${FILE}" \
   --archive-path .:+ \
