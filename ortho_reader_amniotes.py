from ete3 import Tree, NodeStyle, TreeStyle, PhyloTree
from collections import Counter
import random
import pandas as pd
import matplotlib.pyplot as plt
import os
import glob

n = 0
total_ortho_count = 0
total_empty_ortho = 0
tree_rows = []

path_directory = '/linuxhome/tmp/nate/RecurrentEvolution2/EnsemblData'
path_output = '/linuxhome/tmp/nate/RecurrentEvolution2/Data'

file_count = len(glob.glob1(path_directory,"*.nhx"))
print(file_count)
for files in os.listdir(path_directory):
    while (n < file_count):
        whole_tree = PhyloTree(path_directory + "/Tree" + str(n) + ".nhx", alignment = path_directory + "/Tree" + str(n) + ".fa", alg_format="fasta")

        #Functions to define the species identifiers in the 2 files for Sam's workflow
        def species_name(node_name_string):
            spname = node_name_string[3:18]
            return spname

        def species_name2(node_name_string):
            spname2 = node_name_string[3:6]
            return spname2


        #iterate and store all Euteleostomi nodes in a list
        all_nodes = []
        tree_dup_count = 0
        tree_ortho_count = 0
        tree_empty_ortho = 0
        tree_ortho_count = 0
        tree_indep_dups = 0
        for node in whole_tree.traverse():
            if node.T == '32524':
                if node.DD == 'N' and node.D == 'N':
                    all_nodes.append(node)
                    #Count number of orthologous groups
                    total_ortho_count += 1
                    tree_ortho_count += 1

        #iterate through each orthologous group and get information from each group to add together
        for i in range(len(all_nodes)):
            #Write the species names (First 4 Letters) into a new file if they occur at either side of duplication 
            ofile = open("".join([path_output + "/Tree", str(n), "-", str(i), ".mafft"]), "w")
            ofile2 = open("".join([path_output + "/Tree", str(n), "-", str(i), ".indies"]), "w")
            ofile2.write("#Bootstraps = 100" + "\n")
            vert_tree = all_nodes[i]
            all_dups = []
            indepen_dups = []
            prev_sp1 = []
            prev_sp2 = []
            dup_count = 0

            #This loop counts the independent and empty
            for node in vert_tree.traverse():
                if node.D == 'Y':
                    dup_count += 1
                    tree_dup_count += 1
                    all_dups.append(node)
            if dup_count == 0:
                total_empty_ortho += 1
                tree_empty_ortho += 1

            for dup_node in all_dups:
                nested_dups = 0
                for node in dup_node.traverse():
                    if node.D == 'Y':
                        nested_dups = nested_dups + 1
                if nested_dups == 1:
                    tree_indep_dups += 1
                    indepen_dups.append(dup_node)
            
            for node in indepen_dups:
                whole_tree.set_species_naming_function(species_name) #Set the naming function for the entire tree
                dup_sp = node.get_leaves() #create list of all leaves in dupl node
                mafft_list = []
                dup_pairs = []
                dup_leaves4 = []
                unique_leaves = []
                bootstrap = random.uniform(0.6, 1)

                #double for-loop to count each species in the dup_sp and filter out two-copy genes
                for species in dup_sp:
                    count = 0
                    for chk_species in dup_sp:
                        if chk_species.species[0:3] == species.species[0:3]:
                            count += 1
                    if count == 2:
                        mafft_list.append(species)
                        dup_pairs.append(species.species[0:3])
                unique_leaves = list(set(dup_pairs))    

             #THIS BLOCK IS FOR THE .INDIES FILE            
                for i in range(len(unique_leaves)): 
                    count = 0
                    for j in range(len(prev_sp1)):
                        if unique_leaves[i] == prev_sp1[j]:
                            count += 1 #This counts matches and changes the species code
                    species_code = unique_leaves[i] + chr(256 + count)
                    dup_leaves4.append(species_code)
                prev_sp1.extend(unique_leaves)
                #Write to the indies file
                ofile2.write(str(bootstrap) + "\t" + '\t'.join(dup_leaves4)  + "\n")

            #THIS BLOCK IS FOR THE .MAFFT FILE        
                for i in range(len(mafft_list)):
                    count = 0
                    count2 = 0
                    for j in range(len(prev_sp2)):
                         if mafft_list[i].species[0:3] == prev_sp2[j].species[0:3]:
                            count += 1
                            if count == 2: #This makes a letter change only when there's a pair
                                count2 += 1
                                count = 0
                    #Below adds all of the parts of the name together
                    species_code2 = mafft_list[i].species[0:3] + chr(256 + count2) + mafft_list[i].species[5:15]
                    #Write to the mafft file
                    ofile.write(">" + species_code2 + "\n" + mafft_list[i].sequence + "\n")
                prev_sp2.extend(mafft_list)
            #Closing the file after the writing is done
            ofile2.close()
            ofile.close()

        tree_rows.append([n, tree_ortho_count, tree_empty_ortho, tree_dup_count, tree_indep_dups])
        print(n)
        n += 1
tree_df = pd.DataFrame(tree_rows, columns=["Tree", "Ortho Groups", "Empty-Ortho Groups", "Dups", "Ind. Dups"])
tree_df.to_csv('/linuxhome/tmp/nate/RecurrentEvolution2/Data/Tree_Dataframe.csv', index=False)
print(tree_df)
