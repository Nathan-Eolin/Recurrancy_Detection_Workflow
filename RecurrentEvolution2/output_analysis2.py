import os, glob
import pandas as pd
import matplotlib.pyplot as plt

def Convert(string):
    li = list(string.split("/"))
    return li
score_rows = []

#define path to output files
output_path = '/linuxhome/tmp/nate/RecurrentEvolution2/Output/'
indies_path = '/linuxhome/tmp/nate/RecurrentEvolution2/Data/'

#Specify that python is only reading .indies files
for filename in glob.glob(os.path.join(output_path, '*.out')):
    ortho_name = filename[47:-4]
    zvalue = "N/A"
    pvalue = "N/A"
    sig_pairs = "N/A"
    species_rep = "N/A"
    ensembl_link = "N/A"
    with open(indies_path + ortho_name + ".indies") as r:
        dupline_count = (len(r.readlines()) - 1)
        
    with open(os.path.join(os.getcwd(), filename), 'r') as f:
        #Loop through each line of the file
        for line in f:
            if line.startswith('P ='):
                pvalue_list = line.strip().split('= ')
                pvalue_list.pop(0)
                pvalue = pvalue_list[0]
                
            if line.startswith('<ZF>'):
                zvalue_list = line.strip().split('= ')
                for i in range(0,len(zvalue_list)):
                    zvalue_list2 = zvalue_list[i].split("\t")
                zvalue = zvalue_list2[0]
                sig_pairs = 'N/A'
                if len(zvalue_list2) == 2:
                    sig_pairs = zvalue_list2[1][1:-1]
            if line.startswith('Fate 1:'):
                name_list = line.strip().split(': ')
                for i in range(0,len(name_list)):
                    name_list2 = name_list[i].split("\t")
                species_rep = ("ENS" + name_list2[0][0:3] + 'P0' + name_list2[0][4:20])
                ensembl_link = "https://www.ensembl.org/Multi/Search/Results?q=" + species_rep + ";site=ensembl_all"
            		
    score_rows.append([ortho_name, pvalue, zvalue, sig_pairs, dupline_count, species_rep, ensembl_link])


scores_df = pd.DataFrame(score_rows, columns=["Ortho-Group","P-Value", "Z-Score","Sig-Pairs", "Dups", "Gene-Name", "Ensembl"])
scores_df.to_csv('/linuxhome/tmp/nate/RecurrentEvolution2/Output/Scores_Dataframe.csv', index=False)
