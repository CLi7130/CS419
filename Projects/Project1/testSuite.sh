#!/bin/sh
echo Deleting existing database...
rm -rf tables

# Testing for AddUser
    echo "[AddUser] Testing valid AddUser Commands...."
    echo
    #should return success for each
    i=1
    while [ "$i" -le 10 ]; do
        echo "python3 auth.py AddUser user"$i "password"$i
        python3 auth.py AddUser user$i password$i
        i=$(( i + 1 ))
    done

    echo "-------"
    echo "[AddUser] Testing Adding Users already in system..."
    echo
    #should return errors, as users are already in database
    i=1
    while [ "$i" -le 10 ]; do
        echo "python3 auth.py AddUser user"$i "password"$i
        python3 auth.py AddUser user$i password$i
        i=$(( i + 1 ))
    done

    echo "-------"
    echo "[AddUser] Testing Invalid Commands..."
    echo

    # wrong command
    echo "python3 auth.py addUser user21 password21"
    python3 auth.py addUser user21 password21

    # too few params (missing username and password)
    echo "python3 auth.py AddUser \"\" \"\""
    python3 auth.py AddUser "" ""

    # too many params
    echo "python3 auth.py AddUser user50 password50 password2"
    python3 auth.py AddUser user50 password50 password2

    echo "-------"
    echo "[AddUser] Testing Blank Username"
    echo
    # blank username
    echo "python3 auth.py AddUser \"\" password"
    python3 auth.py AddUser "" password

    echo "-------"
    echo "[AddUser] Testing Blank Password"
    echo
    # blank password (this should work)
    echo "python3 auth.py AddUser user100 \"\""
    python3 auth.py AddUser user100 ""

    echo "-------"
    echo "[AddUser] Testing Users/Passwords with spaces"
    echo
    echo "python3 auth.py AddUser \"user name\" password"
    python3 auth.py AddUser "user name" password

    echo "python3 auth.py AddUser paul monkey\ brains"
    python3 auth.py AddUser paul monkey\ brains

    echo "python3 auth.py AddUser paul2 \"monkey brains\""
    python3 auth.py AddUser paul2 "monkey brains"

    echo "---------------------------"

# Testing for Authenticate
    echo "[Authenticate] Testing Valid Credentials..."
    echo
    #should return success for each
    i=1
    while [ "$i" -le 10 ]; do
        echo "python3 auth.py Authenticate user"$i "password"$i
        python3 auth.py Authenticate user$i password$i
        i=$(( i + 1 ))
    done

    echo "-------"
    echo "[Authenticate] Testing Invalid Credentials..."
    echo
    i=1
    while [ "$i" -le 10 ]; do
        echo "python3 auth.py Authenticate user"$i "badpassword"$i
        python3 auth.py Authenticate user$i badpassword$i
        i=$(( i + 1 ))
    done

    echo "-------"
    echo "[Authenticate] Testing Users not in database..."
    echo
    i=20
    while [ "$i" -le 30 ]; do
        echo "python3 auth.py Authenticate user"$i "password"$i
        python3 auth.py Authenticate user$i password$i
        i=$(( i + 1 ))
    done

    echo "-------"
    echo "[Authenticate] Testing Invalid Input..."
    echo

    #blank username
    echo "python3 auth.py Authenticate \"\" password"
    python3 auth.py Authenticate "" password

    #missing input
    echo "python3 auth.py Authenticate password"
    python3 auth.py Authenticate password

    echo "python3 auth.py Authenticate user1 password1 password2"
    python3 auth.py Authenticate user1 password1 password2

# Testing for SetDomain
    echo "------------------------------"
    echo "[SetDomain] Add user to a domain that doesn't exist..."
    echo
    echo "---New Domain: end_user---"
    #this should return nothing, as the domain doesn't exist.
    echo "python3 auth.py DomainInfo end_users"
    python3 auth.py DomainInfo end_users

    #should create domain
    i=1
    while [ "$i" -le 5 ]; do
        echo "python3 auth.py SetDomain user"$i "end_users"
        python3 auth.py SetDomain user$i end_users
        i=$(( i + 1 ))
    done

    #this should show additions to the new domain (users 1-3)
    echo "python3 auth.py DomainInfo end_users"
    python3 auth.py DomainInfo end_users

    echo "---New Domain: admin---"
    #this should return nothing, as the domain doesn't exist.
    echo "python3 auth.py DomainInfo admin"
    python3 auth.py DomainInfo admin

    #should create domain
    i=6
    while [ "$i" -le 8 ]; do
        echo "python3 auth.py SetDomain user"$i "admin"
        python3 auth.py SetDomain user$i admin
        i=$(( i + 1 ))
    done

    #this should show additions to the new domain (users 4-6)
    echo "python3 auth.py DomainInfo admin"
    python3 auth.py DomainInfo admin

    echo "---New Domain: assistant---"
    #this should return nothing, as the domain doesn't exist.
    echo "python3 auth.py DomainInfo assistant"
    python3 auth.py DomainInfo assistant

    #should create domain
    i=9
    while [ "$i" -le 10 ]; do
        echo "python3 auth.py SetDomain user"$i "assistant"
        python3 auth.py SetDomain user$i assistant
        i=$(( i + 1 ))
    done

    #this should show additions to the new domain (users 4-6)
    echo "python3 auth.py DomainInfo assistant"
    python3 auth.py DomainInfo assistant

    echo "-------"
    echo "[SetDomain] Test for Missing Domain...."
    echo
    echo "python3 auth.py SetDomain user10 \"\""
    python3 auth.py SetDomain user10 ""

    echo "-------"
    echo "[SetDomain] Test for Nonexistant User...."
    echo
    echo "python3 auth.py SetDomain \"\" admin"
    python3 auth.py SetDomain "" admin

    echo "python3 auth.py SetDomain user999 admin"
    python3 auth.py SetDomain user999 admin

# Tests for DomainInfo
    echo "====================="
    echo "[DomainInfo] Test for missing Domain"
    echo
    echo "python3 auth.py DomainInfo \"\""
    python3 auth.py DomainInfo ""

    echo "-------"
    echo "[DomainInfo] Test printing valid Domain"
    echo
    echo "python3 auth.py DomainInfo end_users"
    python3 auth.py DomainInfo end_users

    echo "-------"
    echo "[DomainInfo] Test printing Nonexistant Domain"
    echo
    echo "python3 auth.py DomainInfo maintenance"  
    python3 auth.py DomainInfo maintenance

    echo "-------"
    echo "[DomainInfo] Test printing Empty Domain"
    echo "Create empty domain via AddAccess"
    echo
    
    echo "python3 auth.py AddAccess edit_codebase IT iLab_Computers"
    python3 auth.py AddAccess edit_codebase IT iLab_Computers

    #This should return nothing, domain is empty
    echo "python3 auth.py DomainInfo IT"  
    python3 auth.py DomainInfo IT

# Testing for SetType
    echo "====================="
    echo "[SetType] Test for missing Parameters"

    echo "python3 auth.py SetType \"\" personal_info"
    python3 auth.py SetType  "" personal_info

    echo "python3 auth.py SetType name \"\""
    python3 auth.py SetType name ""

    echo "python3 auth.py TypeInfo personal_info"
    python3 auth.py TypeInfo personal_info

    echo "----"
    echo "[SetType] Set valid Type"
    echo
    echo "python3 auth.py SetType name personal_info"
    python3 auth.py SetType name personal_info
    echo "python3 auth.py SetType DOB personal_info"
    python3 auth.py SetType DOB personal_info
    echo "python3 auth.py SetType SSN personal_info"
    python3 auth.py SetType SSN personal_info
    echo "python3 auth.py SetType height personal_info"
    python3 auth.py SetType height personal_info
    echo "python3 auth.py SetType weight personal_info"
    python3 auth.py SetType weight personal_info

    echo "python3 auth.py TypeInfo personal_info"
    python3 auth.py TypeInfo personal_info
    
    echo "----"
    echo "[SetType] Add duplicates (should return success, but not add to type)"
    echo
    echo "python3 auth.py SetType name personal_info"
    python3 auth.py SetType name personal_info
    echo "python3 auth.py SetType DOB personal_info"
    python3 auth.py SetType DOB personal_info

    echo "python3 auth.py TypeInfo personal_info"
    python3 auth.py TypeInfo personal_info

# Testing for TypeInfo
    echo "====================="
    echo "[TypeInfo] Test for valid input"
    echo
    echo "python3 auth.py TypeInfo \"\""
    python3 auth.py TypeInfo ""

    echo "-----"
    echo "[TypeInfo] Test for types that do not exist"
    echo "python3 auth.py TypeInfo sandwiches"
    python3 auth.py TypeInfo sandwiches

    echo "-----"
    echo "[TypeInfo] Test for types that are empty\n"
    echo "python3 auth.py TypeInfo iLab_Computers"
    python3 auth.py TypeInfo iLab_Computers

    echo "-----"
    echo "[TypeInfo] Test for types that do exist\n"
    echo "python3 auth.py TypeInfo personal_info"
    python3 auth.py TypeInfo personal_info 

# Testing for AddAccess
    echo "====================="
    echo "[AddAccess] Test for valid input"
    echo 
    #These should all fail
    echo "python3 auth.py AddAccess \"\" end_users personal_info"
    python3 auth.py AddAccess "" end_users personal_info
    
    echo "python3 auth.py AddAccess edit_codebase \"\" personal_info"
    python3 auth.py AddAccess edit_codebase "" personal_info

    echo "python3 auth.py AddAccess edit_codebase end_users \"\""
    python3 auth.py AddAccess edit_codebase end_users ""

    # Test Creation of domain and type
    echo "----"
    echo "[AddAccess] Test creation of domain, type and operation"
    echo "Create empty Domain and Type"

    echo "python3 auth.py DomainInfo students"
    python3 auth.py DomainInfo students

    echo "python3 auth.py TypeInfo books"
    python3 auth.py TypeInfo books

    echo "python3 auth.py AddAccess read students books"
    python3 auth.py AddAccess read students books

    echo "----"
    echo "[AddAccess] Test duplicate entries of operation, domain, type\n"
    echo "python3 auth.py AddAccess read students books"
    python3 auth.py AddAccess read students books

    echo "----"
    echo "[AddAccess] Add valid operations to domain/type pairs\n"
    echo "python3 auth.py AddAccess ordering IT supplies"
    python3 auth.py AddAccess ordering IT supplies

    echo "python3 auth.py AddAccess email assistant iLab_Computers"
    python3 auth.py AddAccess email assistant iLab_Computers

    echo "python3 auth.py AddAccess payroll admin iLab_Computers"
    python3 auth.py AddAccess payroll admin iLab_Computers

    echo "python3 auth.py AddAccess access assistant iLab_Computers"
    python3 auth.py AddAccess access assistant iLab_Computers

    echo "python3 auth.py AddAccess access end_users iLab_Computers"
    python3 auth.py AddAccess access end_users iLab_Computers

    echo "python3 auth.py AddAccess view end_users personal_info"
    python3 auth.py AddAccess view end_users personal_info


# Testing for CanAccess
    echo "====================="
    echo "[CanAccess] Test for valid input"
    echo 
    #These should all fail
    echo "python3 auth.py CanAccess \"\" end_users personal_info"
    python3 auth.py CanAccess "" end_users personal_info
    
    echo "python3 auth.py CanAccess edit_codebase \"\" personal_info"
    python3 auth.py CanAccess edit_codebase "" personal_info

    echo "python3 auth.py CanAccess edit_codebase end_users \"\""
    python3 auth.py CanAccess edit_codebase end_users ""
   
    echo "----"
    echo "[CanAccess] Test for nonexistant operations\n"
    echo "python3 auth.py CanAccess notpayroll admin iLab_Computers"
    python3 auth.py CanAccess notpayroll admin iLab_Computers

    echo "----"
    echo "[CanAccess] Test Permissions\n"

    echo "Populating types for testing.."
    python3 auth.py SetType ilab1 iLab_Computers
    python3 auth.py SetType ilab2 iLab_Computers
    python3 auth.py SetType rm iLab_Computers
    python3 auth.py SetType textbooks books
    python3 auth.py SetType planners books
    python3 auth.py SetType spreadsheets iLab_Computers
    python3 auth.py SetType screwdriver supplies
    python3 auth.py SetType cables supplies

    python3 auth.py AddUser PK monkeybrains
    python3 auth.py SetDomain PK IT

    echo "---------"

    # success
    echo "[CanAccess] Testing Valid Access Rights"
    echo "python3 auth.py CanAccess payroll user6 rm"
    python3 auth.py CanAccess payroll user6 rm

    echo "python3 auth.py CanAccess payroll user6 spreadsheets"
    python3 auth.py CanAccess payroll user6 spreadsheets

    echo "python3 auth.py CanAccess access user1 ilab2"
    python3 auth.py CanAccess access user1 ilab2  

    echo "python3 auth.py CanAccess ordering PK cables"
    python3 auth.py CanAccess ordering PK cables 

    #failure
    echo "\n[CanAccess] Testing Invalid Access Rights"
    echo "python3 auth.py CanAccess ordering user5 screwdriver"
    python3 auth.py CanAccess ordering user2 screwdriver

    echo "python3 auth.py CanAccess read user7 textbooks"
    python3 auth.py CanAccess read admin textbooks
    
    #operation doesn't exist, failure
    echo "python3 auth.py CanAccess write user2 personal_info"
    python3 auth.py CanAccess write user2 personal_info


