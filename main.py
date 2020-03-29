from freshfoodspy import User, UserLogin, UserRegistration, Admin, AdminLogin, UserDetails, UserManagement

import json

class Main:
    def __init__(self):
        print("FreshFoods Back-End Logic")


        userDetails = UserDetails('reznov','kalishov','2000','us','ru')
        userDetails = UserDetails.parse(json.dumps(userDetails.__dict__))

        print(userDetails.__dict__)

"""
        #tests

        #token verify check
        myUser:User = UserLogin("user3@freshfoods.com").loginEmail("us2er123")
        print("Token Verification (True) : {0}".format(myUser.tokenVerify()))

        #token verify check
        myUser.userID = 0
        myUser.userEmail = "admin@freshfoods.com"
        print("Token Verification (False) : {0}".format(myUser.tokenVerify()))


        #admin login check
        myUser:User = UserLogin("user2@freshfoods.com").loginEmail("user123")
        print("User Login Verification (True) : {0}".format(myUser != None))
        myAdmin = AdminLogin(myUser).login()
        print("Admin Login Verification (True) : {0}".format(myAdmin != None))

        #admin login check
        myUser:User = UserLogin("user3@freshfoods.com").loginEmail("us2er123")
        myAdmin = AdminLogin(myUser).login()
        print("Admin Login Verification (False) : {0}".format(myAdmin != None))

        #user registration check
        myUser = UserRegistration("user3@freshfoods.com","us2er123").register()
        print("User Registration (False) : {0}".format(myUser != None))
"""

if __name__ == "__main__":
    main = Main()


