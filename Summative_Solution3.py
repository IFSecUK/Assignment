from hashlib import sha256
from datetime import date,timedelta


IV = 15304484387517434811
cipher_text = "a75da6155e61662665dfdec2264097b460cea3eb09c84461b5f728d9b0058361"


byte_IV = IV.to_bytes(8,"big") #Converts IV to Big Endian Format and stores the value in bytes.
byte_of_ciphertext = bytes.fromhex(cipher_text) #converts ciphertext into byte array

#Initializing empty lists. One for days and one for concatenation of byte array of IV and date.
list_of_days = []
list_of_IV_plus_days_in_bytes = []
start_date = date(2000, 11, 29)
end_date = date.today()
delta = end_date - start_date #Calculating the time difference from today.

#Iterates over each date and concatenates the byte array of IV with the calculated byte array of date using temporenc module.
for i in range(delta.days + 1):
	day = start_date + timedelta(days=i)
	date_in_byte = str(day).encode()
	list_of_IV_plus_days_in_bytes.append(byte_IV + date_in_byte)
	list_of_days.append(str(day))


#Creating a list of hashes from the byteArray list of IV plus date.
list_of_hashes = []
for item in list_of_IV_plus_days_in_bytes:
	hashes = sha256(item).digest()
	list_of_hashes.append(hashes)


#Creating a dictionary of key as date and its associated hash value in bytes.
Days_and_their_byteArrays_hash_dict = dict(zip(list_of_days,list_of_hashes))

#Defining the xor function for bytes.
def byte_xor(ba1, ba2):
	return bytes([_a ^ _b for _a, _b in zip(ba1, ba2)])



#Function for xoring the byte value of cipher text and byte value of each hash.
def create_decoded_dict(encoded_dict):
	decoded_dict = {}
	for key,value in encoded_dict.items():

		try:
			result = byte_xor(value, byte_of_ciphertext) 
			decoded_dict[key] = result
		
		except UnicodeDecodeError:
			decoded_dict[key] = "Cannot decode this value back"
			continue
		except ValueError:
			decoded_dict[key] = "Cannot decode this value back. Continuingg"
			continue

	#print(decoded_dict)
	return decoded_dict

#Store resultant dictionary of dates as keys and their values as decoded strings. 
decoded_dictionary = create_decoded_dict(Days_and_their_byteArrays_hash_dict)


#Function to check if the dictionary conatins any value whose value starts with "Our"
def check_for_secret_key(dict_to_check):
	for key,value in dict_to_check.items():
		if b"Our" in value:
			print("Found the secret value: {}".format(key))
			break
		else:
			continue
	print("Nothing found")

check_for_secret_key(decoded_dictionary)
