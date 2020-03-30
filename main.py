from freshfoodspy import User, UserLogin, UserRegistration, Admin, AdminLogin, UserDetails, UserManagement

import json

class Main:
    def __init__(self):
        print("FreshFoods Back-End Logic")

        myUser:User = UserRegistration('user1@gmail.com','user123').register()
        new_details = myUser.userDetails
        new_details.lastName = "Modified User"
        UserManagement(myUser).updateUserDetails(
            new_details
        )

        print(myUser.__dict__)
        print(myUser.userDetails.__dict__)

        #userDetails = UserDetails('FreshFoods','User 2','2000','Kerala, India')

        #manageUser = UserManagement(myUser, userDetails)
        #manageUser.updateUserDetails()

        #print(userDetails.__dict__)

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


