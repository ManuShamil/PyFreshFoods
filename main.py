from freshfoodspy import User, UserLogin, UserRegistration, Admin, AdminLogin, UserDetails, UserManagement, UserDetails, UserListing, Market, MarketItem, Order

import json
import threading
import time
import random

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

        def foo():
            
            #time.sleep(random.randint(0, 5))

            item = Market.getItem(5)

            #time.sleep(random.randint(0, 5))

            myUser:User = UserLogin('user8@gmail.com').loginEmail('user123')

            chicken = Market.getItem(5)

            myUser.placeOrder(chicken, 10)

            #time.sleep(random.randint(0, 5)) 

            myrOders = myUser.getMyOrders()

            myUser.cancelOrder(myrOders[0])




            messages = myUser.getMessages()

            random_user = UserListing.getUserbyID(13)

            myUser.sendMessage(random_user,'Hi, User 2!')

            for x in messages:
                print(x.__dict__)


            myUser = UserLogin('user2@freshfoods.com').loginEmail('user123')

            messages = myUser.getMessages()

            random_user = UserListing.getUserbyID(16)

            myUser.sendMessage(random_user,'Hi, User8!')


            myUser.readMessage(messages[0])


            for x in messages:
                print(x.__dict__)



        for y in range(0, 1):

            mythread = threading.Thread(target=foo,)
            mythread.start()


        #myUser.placeOrder(item, 8)
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


