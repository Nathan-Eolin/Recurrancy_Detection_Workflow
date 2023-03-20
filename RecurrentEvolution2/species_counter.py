#This is where I will count the occurences of species in the .indies files
import os, glob

#define path to indies files
path = '/linuxhome/tmp/nate/RecurrentEvolution2/Data'
path_to_species = '/linuxhome/tmp/nate/RecurrentEvolution2/Data/species_prefixes_list.txt'

#Create an empty dictionary
d = dict()

#Specify that python is only reading .indies files
for filename in glob.glob(os.path.join(path, '*.indies')):
    with open(os.path.join(os.getcwd(), filename), 'r') as f:
        #Loop through each line of the file
        for line in f:
            #Remove the newline character and split on the tab delimeter
            my_list = line.rstrip('\n').split('\t')

            # Remove the last letter which is not part of the species code
            my_list2 = [x[:-1] for x in my_list]

            # Get rid of the bootstrap value which is always the first element in the list
            my_list2.pop(0)

        # Iterate over each word in line
            for name in my_list2:
            # Check if the word is already in dictionary
                if name in d:
                # Increment count of word by 1
                    d[name] = d[name] + 1
                else:
                # Add the word to dictionary with count 1
                    d[name] = 1


#Print the contents of dictionary
species_file = open("/linuxhome/tmp/nate/RecurrentEvolution2/species_occurences.txt", "w")
for key in list(d.keys()):
    with open(os.path.join(os.getcwd(), path_to_species), 'r') as f:
        for line in f:
            if line.startswith(key):
                species_file.write(str(key) + ":" + str(d[key]) + ":" + str(line[4:]) + "\n")
                print(key, ":", d[key], ":", line[4:])