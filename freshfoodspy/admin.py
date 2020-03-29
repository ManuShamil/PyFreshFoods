from .db import FreshFoodsDBConnector
from .user import User, UserLogin

from .ff_jwt import ff_jwt


class Admin:

    userID = ""
    userEmail = ""
    adminLevel = ""

    def __init__(self, userID, userEmail, level=""):
        self.userID = userID
        self.userEmail = userEmail
        self.adminLevel = level

class AdminLogin:

    user = None

    def __init__(self, user:User):

        if(user == None):
            
            print("User undefined")
            return

        #verify if token belongs to the user
        if (user.tokenVerify() == False):
            
            print("Could not verify Token!")
            return

        user_token = user.userToken

        payload:User = ff_jwt.decode(user_token)

        self.user = user



    def login(self):

        if self.user == None:

            print("empty username field")

            return None

        if not self.user.isAuthorized():
            
            print("admin is not logged in!")

            return None

        admin = FreshFoodsDBConnector('freshfoods','admin').findOne({"userID": self.user.userID})

        if admin is not None:

            print("{0} succesfully logged in as admin".format(self.user.userEmail))

            return Admin(self.user.userID, self.user.userEmail, admin['adminLevel'])
        
        else:

            print("{0} cannot be logged in as admin!".format(self.user.userEmail))

            return None


        

        

