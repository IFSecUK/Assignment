
"""Notes: For this program to run, you need to have the wordlist and the python program in the same directory"""

#!/usr/bin/python3


#Importing necessary modules
import hashlib
from itertools import chain


#Initializing an empty list and adding all the words from the file to the list 
list_of_numbers = ["0","1","2","3","4","5","6","7","8","9","10","11","12","13","14","15"]
#with open("wordlist.txt", 'r') as f:
#	for line in f.readlines():
#		list_of_words.append(line.rstrip())
#	f.close()



list_of_hashes = [] #Initializing an empty hash list
for number in list_of_numbers:
	number_hash = hashlib.sha256(number.encode()).hexdigest() #Calculating hash of all the words stored in the list
	list_of_hashes.append(number_hash) #Adding hash to the list one by one



"""Defining MY24SHA function which takes list of hashes as the input and outputs first 6 hex digits or nibbles"""
def MY24SHA(hash_list):
	new_hash_list = []
	for word_hash in hash_list:
		new_hash = word_hash[:16]
		new_hash_list.append(new_hash)
	return new_hash_list

nibbles_hash_list = MY24SHA(list_of_hashes) #Calling the function and storing the list of 24 bits hashes into new list.



dictionary_of_pass_and_hash = dict(zip(list_of_numbers,nibbles_hash_list)) #Creating a dictionary of words and their 24 bits hashes
#print(dictionary_of_pass_and_hash)


#Creating a set of unique hashes and then printing result of those words whose first 24bits hashes match. 
rev_dict = {}
for key, value in dictionary_of_pass_and_hash.items():
    rev_dict.setdefault(value, set()).add(key)

result = set(chain.from_iterable(
         values for key, values in rev_dict.items()
         if len(values) > 1))
  
# printing result
print("resultant collision: ", str(result))

