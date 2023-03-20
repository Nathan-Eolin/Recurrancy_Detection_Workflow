#This script will be to parse through the large protein fasta file

i = 0

with open("Compara.108.protein_default.aa.fasta") as c:
        
    for line in c:
        
        name = "/linuxhome/tmp/nate/RecurrentEvolution2/EnsemblData/Tree" + str(i) + ".fa"
        tree_fasta = open(name, "a") #CAREFULLLLL, Always perform this on an empty folder!! Otherwise it will append the lines to the existing files
            
        if '//' in line:
            i = i + 1

            
        else:    
            tree_fasta.write(line)