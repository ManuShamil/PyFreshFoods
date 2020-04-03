from freshfoodspy import User, UserLogin, UserRegistration, Admin, AdminLogin, UserDetails, UserManagement, UserDetails, Market, MarketItem, Order

import json

class Main:
    def __init__(self):
        print("FreshFoods Back-End Logic")

        #myUser:User = UserLogin("user8@gmail.com").loginEmail('user123')
        #print(myUser.__dict__)
        #print(myUser.userDetails.__dict__)

        #Market.placeOrder(Order(MarketItem(0,13,"sunflower oil","200"),myUser))

        #myUser:User = UserLogin('user7@gmail.com').loginEmail('user123')
        
        #myItem:MarketItem = MarketItem.buildObject(myUser, "Frozen Chicken 1000g", 200, 451)

        #Market.addMarketItem(myUser, myItem)

        item = Market.getItem(5)

        myUser:User = UserLogin('user8@gmail.com').loginEmail('user123')

        myUser.placeOrder(item, 8)
        myUser.placeOrder(item, 8)
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


