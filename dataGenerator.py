import sys
import random
from random import randint
import json
import os, types
def generateNameOrSurname(var, names, surnames):
    temp = {}
    if var is "name":
        temp[var] = random.choice(names)
    elif var is "surname":
	    temp[var] = random.choice(surnames)
    else:
	    sys.exit("Invalid atribute detected, check -h for more")
    return temp

def accountNumber():
    return str(randint(100, 999999))+ chr(random.randrange(65, 65 + 26))		# 65 = ASCII value for 'A' with a range of 26(number of letters)
    
def phoneNumber():
    return randint(100, 99999999)
 
def credentials():
	credentials = {"username": random.choice(usernames), "password": random.choice(passwords)}
	return credentials
	

def checkIfUnique(arg, var, duplicates):	#checks if generated account number or  phone number was already assigned 
    if len(duplicates[arg]) is 0:		#if dict with given key is empty append given value
        duplicates[arg].append(str(var))	
    else:
        s= set(duplicates[arg]) 
        if var in s: #if generated value already exists generate a new one depending on the key
            if arg is "phoneNumber": 
                var = phoneNumber()
            elif arg is "accountNumber":
                var = accountNumber()
            else:
                sys.exit("Internal error occured, please try again")
            checkIfUnique(arg, var, duplicates) #call the same funcion but with new values
        else:
             duplicates[arg].append(str(var)) #if value doesn;t exists, add it to the ist of duplicates
    return var
	    
def generate(argument):
    if arg == 'name':
        return generateNameOrSurname('name', names, surnames)
    elif arg == 'surname':
        return generateNameOrSurname('surname', names, surnames)
    elif arg == 'accountNumber':
        temp = {}
        accountNmber = accountNumber()
        temp['accountNumber'] = checkIfUnique('accountNumber', accountNumber(), duplicates)
        return temp
    elif arg == 'phoneNumber':
        temp = {}
        temp['phoneNumber'] = checkIfUnique('phoneNumber', phoneNumber(), duplicates)
        return temp    
    elif arg == "credentials":
        var = credentials()
        return var
    elif arg == 'email':		#if one of the arguments entered was 'name', generate email based of it, else genereate random email
        temp = {}
        for d in listOfData:
            done = False
            for k,v in d.items():
                if k is 'name':
                    temp['email'] = v+str(randint(100, 333))+random.choice(domains)
                    done = True
                else:
                    temp['email'] = random.choice(names) + random.choice(domains)
            if done is True: break
        return temp
    else:
        sys.exit("Invalid atribute detected, check -h for more")
		
if __name__ == "__main__":
    placeHolder = []							#All the data is loaded here to avoid continous opening/closing of files -loadStart
    account = []
    phone = []
    duplicates = { "accountNumber" : account, "phoneNumber" : phone}
    domains = ["@gmail.com", "@onet.pl", "@hotmail.com", "@subview.pl", "@outlook.com", "@yahoo.com", "@inbox.com"]
    names = open("names.txt").read().splitlines()
    surnames = open("surnames.txt").read().splitlines()
    usernames = open("usernames.txt").read().splitlines()
    passwords = open("passwords.txt").read().splitlines()		#-loadEnd
    if '-h' in sys.argv:	# if -h argument exists, display help window
        helpArg = """		Syntax = dataGenerator.py arg arg arg int(size of data set to be created)
		example: python dataGenerator.py name surname email 1500
				Avaiable arguments are:
							- name (random name from a file of random names)
							- surname (random surname from a file of random surnames)
							- accountNumber (six digit account number followed by a letter)
							- email (if name exists, email is created based of it)
							- phoneNumber (nine digit phone number)
							- credentials (username and password)
				*No duplicate arguments are allowed
				*Order is determined by the sequence entered
				*Result is saved in data.json"""
        print(helpArg)
        sys.exit()
    try:
        int(sys.argv[-1])	#makes sure that the last argument entered is the number of rows to be generated
    except:
        sys.exit("Syntax errot detected, check -h for more")
    if len(set(sys.argv)) != len(sys.argv):			#if one or more of the same arguments are entered - exit with an error
        sys.exit("Duplicate argument detected, check -h for more")
    else:		#if all checks are completed generate the data
        n = 0
        iterations = int(sys.argv[-1])
        del sys.argv[-1]
        while n != iterations:
            listOfData = []		#stores complete rows of data
            for arg in sys.argv[1:]:
                data = {}
                data = generate(arg)
                listOfData.append(data)
            placeHolder.append(listOfData) #creates the structure list of dictionaries
            n = n +1
        with open('data.json', 'w') as filehandle:  #dump all of the data generated to a file
            json.dump(placeHolder, filehandle)
            filehandle.write("\n") 
