import argparse
import os
import pickle

#used to turn on/off way too many print debugging statements
DEBUG = False

#path in file system to user dict/pickle file
USER_DICT_PATH = "./tables/users.pickle"

# path in file system to parent dir holding all information
PARENT_PATH = "./tables"

# path to domain folder
DOMAIN_DIR_PATH = "./tables/domains"

# path to types folder
TYPES_DIR_PATH = "./tables/types"

# path to access rights/operations folder
ACCESS_RIGHTS_DIR_PATH = "./tables/operations"

# pickle file extension
PICKLE_EXT = ".pickle"

# message for successful command
SUCCESS_MSG = "Success"

#create directories and files for storage of data
def init():
    #os.path.isfile(filename)

    if os.path.isdir(PARENT_PATH):
        #if we've created the parent dir, all the subdirs should be created.
        return
                
    #create parent dir
    os.mkdir(PARENT_PATH)

    #create subdir for domains
    os.makedirs(DOMAIN_DIR_PATH)

    #create subdir for types
    os.makedirs(TYPES_DIR_PATH)

    #create subdir for operations
    os.makedirs(ACCESS_RIGHTS_DIR_PATH)

    #create pickle dict for users, start as empty
    empty_dict = {}
    users = open(USER_DICT_PATH, "wb")
    pickle.dump(empty_dict, users)
    users.close()


# adds a user to a pickle file (dict), stores all users for access control
#
# param user : username to be added
# param password : password corresponding to username
def addUser(user, password):

    if DEBUG:
        print("[In AddUser]")
        print("AddUser " + user + " " + password)

    #check for empty username
    if user == "":
        print("Error: username missing")
        return

    new_user = {user:password}
    
    user_in = open(USER_DICT_PATH, "rb")

    user_dict = pickle.load(user_in)

    if DEBUG:
        print("[AddUser] Loaded Dictionary:")
        print(user_dict)  

    #check for existing user
    if user in user_dict:
        print("Error: user exists")
        
        return
    
    #add user to dict
    #change so we only add new user, not write back entire user list?
    user_dict.update(new_user)

    if DEBUG:
        print("[AddUser] Updated Dictionary:")
        print(user_dict)

    # write dict back to pickle file
    user_out = open(USER_DICT_PATH, "wb")
    pickle.dump(user_dict, user_out)
    user_out.close()
    
    print(SUCCESS_MSG)


# Checks if a given (user, password) pair is in the user dict
#
# param user : username to check for in dict
# param password : password to check for in dict
def authenticate(user, password):
    #authenticate user
    #Authenticate cmd
    
    user_dict = pickle.load(open(USER_DICT_PATH, "rb"))

    if DEBUG:
        print("[In Authenticate]")
        print("Authenticate " + user + " " + password)
        print("[Authenticate] current user dict:")
        print(user_dict)

    if (user, password) in user_dict.items():
        #authenticated, (user, password) key/value matches entry in dict
        print(SUCCESS_MSG)
    elif user in user_dict:
        #user in dict, password is wrong
        print("Error: bad password")
    else:
        #user not in dict
        print("Error: no such user")
    
# Add a user to a domain, users can be in multiple domains
#
# param user : user to be added to the domain, if user is already in domain,
#               return success, but take no action. no duplicate users in a domain.
# param domain : name of domain to add user to, cannot be blank/empty
#                 create domain name if it does not already exist
def setDomain(user, domain):

    filename = domain + PICKLE_EXT

    if DEBUG:
        print("[In SetDomain]")
        print("SetDomain " + user + " " + domain)

    if domain == "":
        # domain name is empty
        print("Error: missing domain")
        return
    
    # check for user in user dict
    user_dict = pickle.load(open(USER_DICT_PATH, "rb"))
    if user not in user_dict:
        print("Error: no such user")
        return
    
    domain_path = os.path.join(DOMAIN_DIR_PATH, filename)

    if os.path.exists(domain_path):
        #domain already exists, check if user is in domain already
        if DEBUG:
            print("[SetDomain] Domain Exists")
        
        read_domain_users = pickle.load(open(domain_path, "rb"))
        
        if user in read_domain_users:
            #user already in domain, do nothing
            if DEBUG:
                print("[SetDomain] User already in domain")
            print(SUCCESS_MSG)
            return
        else:
            #user not in domain, add to domain
            read_domain_users.append(user)
            write_domain_users = open(domain_path, "wb")
            pickle.dump(read_domain_users, write_domain_users)
            write_domain_users.close()
    else:
        #domain does not exist, create domain file/pickle list 
        if DEBUG:
            print("[SetDomain] Domain Does Not Exist")
        
        #create pickle list for domain, add user
        new_user = [user]
        new_domain = open(domain_path, "wb")
        pickle.dump(new_user, new_domain)
        new_domain.close()

    print(SUCCESS_MSG)


# Provides list of users in a domain, prints nothing if domain does not exist,
# or there ar eno users in a domain. 
# 
# param domain : domain name we want information about (list of users in domain)
def domainInfo(domain):

    if DEBUG:
        print("[In DomainInfo]")
        print("DomainInfo " + domain)

    if domain == "":
        # empty string, report error
        print("Error: missing domain")
        return

    filename = domain + PICKLE_EXT
    domain_path = os.path.join(DOMAIN_DIR_PATH, filename)

    #check if domain exists
    if os.path.exists(domain_path):
        #domain exists
        if DEBUG:
            print("[DomainInfo] Domain Exists")
        
        read_domain = pickle.load(open(domain_path, "rb"))
        if len(read_domain) == 0:
            if DEBUG:
                print("[DomainInfo] Domain is empty")
            return
        else:
            # print all users in domain, one per line w/ no leading tabs/spaces
            for user in read_domain:
                print(user)
    else:
        #domain doesn't exist, print nothing and return
        if DEBUG:
            print("[DomainInfo] Domain does not exist")
    

# Assigns a type to an object, creates a type if it does not exist, neither
# parameter can be an empty string.
#
# param object_name : name of the object to be stored in a type
# param type : type for the object to be stored into.
def setType(object_name, type):

    filename = type + PICKLE_EXT
    type_path = os.path.join(TYPES_DIR_PATH, filename)

    if DEBUG:
        print("[In SetType]")
        print("SetType " + object_name + " " + type)

    #check for empty strings
    if object_name == "":
        print("Error: object name missing")
        return
    elif type == "":
        print("Error: type missing")
        return

    if os.path.exists(type_path):
        #type already exists, check if object is in type already
        if DEBUG:
            print("[SetType] Type Exists")
        
        read_type_objects = pickle.load(open(type_path, "rb"))
        
        if object_name in read_type_objects:
            #user already in domain, do nothing
            if DEBUG:
                print("[SetType] obj already in list")
            print(SUCCESS_MSG)
            return
        else:
            #user not in domain, add to domain
            read_type_objects.append(object_name)
            write_type_objects = open(type_path, "wb")
            pickle.dump(read_type_objects, write_type_objects)
            write_type_objects.close()
            
    else:
        # type does not exist, create type file/pickle list 
        if DEBUG:
            print("[SetType] Type Does Not Exist")
        
        #create pickle list for type, add obj
        new_obj = [object_name]
        new_type = open(type_path, "wb")
        pickle.dump(new_obj, new_type)
        new_type.close()

    print(SUCCESS_MSG)

# Lists objects of a given type, one per line.  Type name must be a non-empty string
# 
# param type : type name that we want information about (list of objects in type)
def typeInfo(type):

    filename = type + PICKLE_EXT
    type_path = os.path.join(TYPES_DIR_PATH, filename)
    
    if DEBUG:
        print("[In TypeInfo]")
        print("TypeInfo " + type)

    if type == "":
        # empty string, report error
        print("Error: missing type")
        return

    #check if domain exists
    if os.path.exists(type_path):
        #domain exists
        if DEBUG:
            print("[TypeInfo] Type Exists")
        
        read_type = pickle.load(open(type_path, "rb"))
        if len(read_type) == 0:
            #empty type? shouldn't really be possible with current implementation
            if DEBUG:
                print("[TypeInfo] Empty Type")
            return
        else:
            # print all objects in type, one per line w/ no leading tabs/spaces
            for object in read_type:
                print(object)

    else:
        #Type doesn't exist, print nothing and return
        if DEBUG:
            print("[TypeInfo] Type does not exist")
    

# Define access right, IE: Can a user in domain_name perform operation on type_name?
# Add domain names or type names if they do not exist (this is how we have empty
# domains and types). This is where the access matrix is built. Do not treat duplicate
# operations for a given domain/type pair as an error
# 
# param operation : specified action that will be performed on an object (type)
# param domain_name : specified domain (group of users) that will be granted access 
#                      rights to perform specified operation.
# param type_name : type of objects that will have given operation performed on them
def addAccess(operation, domain_name, type_name):

    # store each operation as separate pickle file (operation = filename)
    # pickle file contains dict of domains
    # domain corresponds to all type values that have operation permission
    # key = domain name, value = list of types that domain has access rights for 
    # operation

    if DEBUG:
        print("[In AddAccess]")
        print("AddAccess " + operation + " " + domain_name + " " + type_name)

    # check for null/empty string values
    if operation == "":
        print("Error: missing operation")
        return

    elif domain_name == "":
        print("Error: missing domain")
        return

    elif type_name == "":
        print("Error: missing type")
        return

    type_filename = type_name + PICKLE_EXT
    type_path = os.path.join(TYPES_DIR_PATH, type_filename)

    if not os.path.exists(type_path):
        #type doesn't exist
        newType(type_name)

    domain_filename = domain_name + PICKLE_EXT
    domain_path = os.path.join(DOMAIN_DIR_PATH, domain_filename)

    if not os.path.exists(domain_path):
        #domain doesn't exist
        newDomain(domain_name)

    filename = operation + PICKLE_EXT
    operation_path = os.path.join(ACCESS_RIGHTS_DIR_PATH, filename)

    if os.path.exists(operation_path):
        # operation exists, check for domain/type pair

        operation_read = open(operation_path, "rb")
        temp_op = pickle.load(operation_read)

        #check that domain exists in operation
        if domain_name not in temp_op:
            if DEBUG:
                print("[AddAccess] Need to Add Domain")
            temp_op = addDomain(domain_name, temp_op)

        if DEBUG:
            print("[AddAccess] Read operation from file: ")
            print(temp_op)
            print(temp_op[domain_name])
        
        for type in temp_op[domain_name]:
            if type == type_name:
                # pair already exists
                if DEBUG:
                    print("[AddAccess] Duplicate operation")
                print(SUCCESS_MSG)
                return
    
        #update operations file and write back to pickle
        temp_op[domain_name].append(type_name)

        operation_write = open(operation_path, "wb")
        pickle.dump(temp_op, operation_write)
        operation_write.close()
    else:
        # operation does not exist, create new pickle dict
        # have to iterate/add all domains, do this in helper function?

        new_op = newOperationDict(domain_name)
        new_op[domain_name].append(type_name)

        if DEBUG:
            print("[AddAccess] Writing Operation: " + operation)
            print(new_op)
        
        operation_write = open(operation_path, "wb")
        pickle.dump(new_op, operation_write)
        operation_write.close()

    print(SUCCESS_MSG)

# Creates dict that lists all domains (key) with a value (empty list of types)
# that corresponds to setting up a new operation (no permissions have been added)
#
# param domain_name : used to see if domain already exists, if not, we create a 
#                       new domain.
def newOperationDict(domain_name):
    # need to create domain or type if not already created.
    # iterate over all domains and add them to dict as keys
    # if domain doesn't exist, add it

    temp_dict = dict()
    domainFound = False

    #iterate through domains
    for filename in os.listdir(DOMAIN_DIR_PATH):
        if filename.endswith(PICKLE_EXT):
            # remove extension to get domain name
            key = os.path.splitext(filename)[0]

            if DEBUG:
                print("[newOperationDict] domain: " + domain_name)
                print("[newOperationDict] filename: " + filename)
                print("[newOperationDict] Key: " + key)

            if key == domain_name:
                #domain exists in domains
                domainFound = True

            temp_dict[key] = list()
    
    if domainFound == False:
        temp_dict = addDomain(domain_name, temp_dict)

    return temp_dict

# add Domain to dict
#
# param domain_name : domain to be added
# param dictionary : domain will be added to this dictionary
def addDomain(domain_name, dictionary):

    temp_list = list()
    dictionary[domain_name] = temp_list

    return dictionary

# Create empty domain list for users
#
# param domain_name : name for new domain
def newDomain(domain_name):

    temp_list = list()
    filename = domain_name + PICKLE_EXT
    domain_path = os.path.join(DOMAIN_DIR_PATH, filename)

    new_domain = open(domain_path, "wb")
    pickle.dump(temp_list, new_domain)
    new_domain.close()


# Create empty type list for objects
#
# param type_name : name for the new type
def newType(type_name):

    temp_list = list()
    filename = type_name + PICKLE_EXT
    type_path = os.path.join(TYPES_DIR_PATH, filename)

    new_type = open(type_path, "wb")
    pickle.dump(temp_list, new_type)
    new_type.close()


# "Can user perform operation on object" is how this method should be thought of.
# Need to find all domains the user belongs in, as well as types the object is present
# in, then get return value off of given operation pickle file with domain/type pairs
# 
# param operation : operation that needs to can or cannot be performed 
#                    by given user on given object
# param user : provided user whose access rights will be checked for given operation
#               on given object
# param object : provided object that operation can/cannot be performed on
def canAccess(operation, user, object):
    #TODO fix error in 527?
    err = "Error: Access Denied"

    if DEBUG:
        print("[In CanAccess]")
        print("CanAccess " + operation + " " + user + " " + object)

    # check for blank input
    if operation == "" or user == "" or object == "":
        print(err)
        return

    # check if params exist in respective fields
    # check if operation exists
    op_path = os.path.join(ACCESS_RIGHTS_DIR_PATH, operation + PICKLE_EXT)
    if not os.path.exists(op_path):
        print(err)
        return

    user_in = open(USER_DICT_PATH, "rb")
    user_dict = pickle.load(user_in)
    #user not present in user list
    if user not in user_dict.keys():
        print(err)
        return
    
    # look for domains that have username
    domain_membership = list()

    for filename in os.listdir(DOMAIN_DIR_PATH):
        if filename.endswith(PICKLE_EXT):
            # remove extension to get domain name
            key = os.path.splitext(filename)[0]
            if DEBUG:
                print("[CanAccess] filename: " + filename)
                print("[CanAccess] key: " + key)

            domain_path = os.path.join(DOMAIN_DIR_PATH, filename)
            read_domain = open(domain_path, "rb")
            temp_domain = pickle.load(read_domain)

            if DEBUG:
                print("[CanAccess] Domain " + key + " opened:")
                print(temp_domain)
            
            if user in temp_domain:
                domain_membership.append(key)
                if DEBUG:
                    print("[CanAccess] Domain " + key + " added to list")
            else:
                if DEBUG:
                    print("[CanAccess] User not in domain")
    
    # look for types that contain object
    type_membership = list()
    for filename in os.listdir(TYPES_DIR_PATH):
        if filename.endswith(PICKLE_EXT):
            key = os.path.splitext(filename)[0]

            type_path = os.path.join(TYPES_DIR_PATH, filename)

            read_type = open(type_path, "rb")
            temp_type = pickle.load(read_type)

            if DEBUG:
                print("[CanAccess] Type " + key + " opened:")
                print(temp_type)
            
            if object in temp_type:
                type_membership.append(key)
                if DEBUG:
                    print("[CanAccess] Type " + key + " added to list")
            else:
                if DEBUG:
                    print("[CanAccess] Object not in type")

    # we should now have a list of all domains the user belongs to,
    # and types the object belongs to
    if DEBUG:
        print("[CanAccess] Domain Membership of " + user)
        print(domain_membership)

        print("[CanAccess] Type Membership of " + object)
        print(type_membership)

    filename = operation + PICKLE_EXT
    operation_path = os.path.join(ACCESS_RIGHTS_DIR_PATH, filename)

    #if operation doesn't exist, return an error
    if os.path.exists(operation_path):
        #iterate through domain/type pairs

        read_operation = open(operation_path, "rb")
        operation_dict = pickle.load(read_operation)

        for domain in domain_membership:
            for type in type_membership:
                if type in operation_dict[domain]:
                    print(SUCCESS_MSG)
                    return
    
    # no match/access found
    print(err)


# Checks for correct number of arguments for given function, quits program if wrong 
# number of args is detected.
#
# param args : arguments taken from command line
# param numArgs : correct number of arguments for this function
def checkNumOfArgs(args, numArgs):

    # 1 arg: domainInfo(domain), typeInfo(type)
    # 
    # 2 args: AddUser(user, password), authenticate(user, password), 
    #           setdomain(user, domain), setType(object_name, type)
    #
    # 3 args: addAccess(operation, domain_name, type_name), 
    #           canAccess(operation, user, object)

    functionName = args[0]

    if( (len(args) - 1) > numArgs):
        #more arguments than needed, remove 1 for command
        print("Error: too many arguments for " + functionName)
        quit()
    elif ( (len(args) - 1) < numArgs):
        #less arguments than needed, remove 1 for command
        print("Error: missing arguments for " + functionName)
        quit()


def main():

    #TODO:
    # check params for usernames/types against google - see discussion board
    # https://support.google.com/a/answer/9193374?hl=en

    init()
    parser = argparse.ArgumentParser()
    parser.add_argument('input', metavar = 'N', type=str, nargs='+')

    args = parser.parse_args()

    function = args.input[0]

    #is there a better way to check the function name? probably.
    if function == "AddUser":
        
        checkNumOfArgs(args.input, 2)

        user = args.input[1]
        password = args.input[2]

        addUser(user, password)

    elif function == "Authenticate":

        checkNumOfArgs(args.input, 2)
    
        user = args.input[1]
        password = args.input[2]

        authenticate(user, password)

    elif function == "SetDomain":

        checkNumOfArgs(args.input, 2)

        user = args.input[1]
        domain = args.input[2]

        setDomain(user, domain)

    elif function == "DomainInfo":

        checkNumOfArgs(args.input, 1)

        domain = args.input[1]

        domainInfo(domain)
    
    elif function == "SetType":

        checkNumOfArgs(args.input, 2)

        object_name = args.input[1]
        type = args.input[2]

        setType(object_name, type)
    
    elif function == "TypeInfo":

        checkNumOfArgs(args.input, 1)

        type = args.input[1]

        typeInfo(type)
    
    elif function == "AddAccess":

        checkNumOfArgs(args.input, 3)

        operation = args.input[1]
        domain_name = args.input[2]
        type_name = args.input[3]

        addAccess(operation, domain_name, type_name)

    
    elif function == "CanAccess":

        checkNumOfArgs(args.input, 3)

        operation = args.input[1]
        user = args.input[2]
        object = args.input[3]

        canAccess(operation, user, object)

    else:
        print("Error: Invalid Command " + function)
    
if __name__ == "__main__":
    main()

