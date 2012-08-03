FILE='../data/schemas/1.4/SRA.experiment.xsd'
PREFIX='experiment'

pyxbgen \
   -m "${PREFIX}" \
   -u "${FILE}" \
   --archive-path .:+ \
