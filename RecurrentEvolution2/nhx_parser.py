#This script is to parse through the large nhx file of Ensembl

nhxdata = []
with open("Compara.108.protein_default.nhx.emf") as fh:
    for line in fh:
        if line.startswith("("):
            strip_lines=line.strip()
            nhxdata.append(strip_lines)

for i in range(len(nhxdata)):
    ofile = open("".join(["/linuxhome/tmp/nate/RecurrentEvolution2/EnsemblData/Tree", str(i), ".nhx"]), "w")
    ofile.write(nhxdata[i])