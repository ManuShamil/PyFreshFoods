import json
import bcrypt
from datetime import datetime

from .db import FreshFoodsDBConnector
from .ff_jwt import ff_jwt
from .market import Market, MarketItem

class Message:
    messageID = -1
    messageFrom = None
    messageTo = None
    messageRead = False

    Message = ""

    messageTimeStamp = ""
    

class UserDetails:
    firstName = ""
    lastName = ""
    DOB = ""
    Address = ""
    altAaddress = ""

    def __init__(self, firstName="", lastName="", DOB="", Address="",altAaddress=""):
        self.firstName = firstName
        self.lastName = lastName
        self.DOB = DOB
        self.Address = Address
        self.altAaddress = altAaddress

    @classmethod
    def parse(cls, user_details=""):
            
        if(type(user_details) == str):
            user_details:UserDetails = json.loads(user_details)

        userDetails = UserDetails()
        userDetails.firstName = user_details['firstName']
        userDetails.lastName = user_details['lastName']
        userDetails.DOB = user_details['DOB']
        userDetails.Address = user_details['Address']
        userDetails.altAaddress = user_details['altAaddress']

        return userDetails

    @classmethod
    def buildPublicUserDetailsObject(cls, first_name, last_name):
        
        cls.firstName = first_name
        cls.lastName = last_name
        
#Main Data Model
class User:
    userID = ""
    userEmail = ""
    userToken = ""
    userDetails = None

    def __init__(self,userID=None, email="", token=""):
        """Creates a user Object
        
        Arguments:
            email {str} -- Email of the user
        """

        self.userID = userID
        self.userEmail = email
        self.userToken = token

    def setUserDetails(self, user_details:UserDetails):
        self.userDetails = user_details
        
    def isAuthorized(self):
        if ff_jwt.verify(self.userToken):
            return True
        else:
            return False

    def tokenVerify(self):

        payload:User = ff_jwt.decode(self.userToken)

        del(payload['userToken']) #no need to check for token

        for x in payload:
            if self.__dict__[x] != payload[x]:
                return False

        return True

    def placeOrder(self, item:MarketItem, qty:int):

        UserMarketManagement(self).placeOrder(item, qty)

    def cancelOrder(self, order):
        
        UserMarketManagement(self).cancelOrder(order)

    def getMyOrders(self):

        return UserMarketManagement(self).getMyOrders()

    def sendMessage(self, to, message:str):

        UserManagement(self).sendMessage(to, message)

    def getMessages(self):
        
        return UserManagement(self).getMessages()

    def readMessage(self, message:Message):

        UserManagement(self).readMessage(message)

    @classmethod
    def buildPublicUserObject(cls, user_id:int, user_details:UserDetails):
        cls.userID = user_id
        cls.userDetails = user_details

        return cls
        



class UserMarketManagement:
    myUser = None

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

        self.myUser = user

    def placeOrder(self, item:MarketItem, qty:int):

        new_order = item.createOrder(self.myUser, qty)

        Market.placeOrder(new_order)

    def cancelOrder(self, order):

        Market.cancelOrder(order)

    def getMyOrders(self):

        return Market.getOrdersbyUser(self.myUser)



class UserManagement:

    myUser = None

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

        self.myUser = user

    def updateUserDetails(self, user_details:UserDetails):

        FreshFoodsDBConnector('freshfoods','userdetails').update({
            "_id": self.myUser.userID
        },{
            '$set': user_details.__dict__  
        },True
        )
        
        pass


    @classmethod
    def insertUserDetails(cls, userID):

        user_details=UserDetails()

        """ Only to be called from UserRegistration.register() """
        FreshFoodsDBConnector('freshfoods','userdetails').update({
            "_id": userID
        },{
            '$set': user_details.__dict__  
        },
        insert_new=True
        )
        
        pass

    def getUserDetails(self):

        user_details = FreshFoodsDBConnector('freshfoods','userdetails').findOne({
            "_id": self.myUser.userID
        })

        if (user_details != None):

            return UserDetails.parse(user_details)

    
    def getMessages(self):
        
        my_messages = FreshFoodsDBConnector('freshfoods','usermessages').findAll({
            "messageTo": self.myUser.userID 
        })

        myMessages = []

        for x in my_messages:

            message = Message()
            message.messageID = x['_id']
            message.messageTo = self.myUser
            message.messageFrom = UserListing.getUserbyID(x['messageFrom'])
            message.Message = x['Message']
            message.messageRead = x['messageRead']
            message.messageTimeStamp = x['messageTimeStamp']

            myMessages.append(message)

        return myMessages
    
    def sendMessage(self, to:User, message:str):

        sequenceValue = FreshFoodsDBConnector('freshfoods','counter').findOneAndUpdate({
                            "$and": [
                                {
                                    "collectionName": 'usermessages'
                                },{
                                    "columnName": '_id'
                                }
                        ]},
                        {
                            "$inc": {"sequenceValue": 1}
                        })['sequenceValue']

        FreshFoodsDBConnector('freshfoods','usermessages').insert({
            "_id": sequenceValue + 1,
            "messageFrom": self.myUser.userID,
            "messageTo": to.userID,
            "Message": message,
            "messageRead": False,
            "messageTimeStamp": datetime.now().isoformat()
        })
    
    def readMessage(self, message:Message):

        FreshFoodsDBConnector('freshfoods', 'usermessages').update({
            "_id": message.messageID,
        },{
            "$set": {
                "messageRead": True
            }
        })



#TODO Add Erros incase of UserLogin Failure 
class UserLogin:

    email = ""

    def __init__(self, email:str):
        """UserLogin Class - contains methods to return User Object

        - loginEmail()

        Arguments:
            email {str} -- Email of the user.
        """

        self.email = email
        

    def loginEmail(self, password:str):
        """Logs In user using Email
        
        Arguments:
            password {str} -- password of the user

        Returns:
            User -- If user succesfully logs in
            None -- If user fails to log in
        """

        print("UserLogin using Email: {0}".format(self.email))

        if(self.email != "" and password !=""):

            myUser = FreshFoodsDBConnector("freshfoods","user").findOne({"userEmail": self.email})

            if myUser == None:

                print("{0} does not exist in Database!".format(self.email))
                return None

            if bcrypt.checkpw( password.encode('utf-8'), myUser['userPassword']):

                email = myUser['userEmail']
                userid = myUser['_id']



                user = User(userid, email) #create new user object without token
                token = ff_jwt.encode(user.__dict__) #convert user object to token

                loggedUser = User(user.userID, user.userEmail, token) #return newly created user object with token included


                loggedUser.setUserDetails(UserManagement(loggedUser).getUserDetails()) #set User Information
                return loggedUser
                
            else:
                print("password is incorrect!")
                return None
        else:
            return None

#TODO Add Erros incase of UserRegistration Failure 
class UserRegistration:
    userEmail = ""
    userPassword = ""

    required = ["userEmail", "userPassword"]
    missingParams = []
    Proceed = True

    def __init__(self, email="", password=""):
        self.userEmail = email
        self.userPassword = password

    def register(self):

        for x in self.required:
            if (self.__dict__[x] == ""):

                print("{0} cannot be empty!".format(x))

                self.missingParams.append(x)

                self.Proceed = False

        if self.Proceed is not True:
            print("could not complete registration of {0}".format(self.userEmail))
            return self.missingParams

        if self.isDuplicate():
            print("Email Already Exists")
            return None

        # All requirements filled
        # Now register the user to database

        hashedpassword = bcrypt.hashpw(self.userPassword.encode('utf-8'), bcrypt.gensalt())

        sequenceValue = self.updateAndGetNextSequence() #this will be the next userID (Auto Increment)
                    
        #add user to user database
        FreshFoodsDBConnector('freshfoods','user').insert({
                                "_id": sequenceValue,
                                "userEmail": self.userEmail,
                                "userPassword": hashedpassword
                            })

        #add user details to user database
        UserManagement.insertUserDetails(sequenceValue)

        #now try logging in to the account

        print("User Registration completed succesfully!")

        user = UserLogin(self.userEmail).loginEmail(self.userPassword)

        return user


    def updateAndGetNextSequence(self):
        
        sequenceValue = FreshFoodsDBConnector('freshfoods','counter').findOneAndUpdate({
                            "$and": [
                                {
                                    "collectionName": 'user'
                                },{
                                    "columnName": '_id'
                                }
                        ]},
                        {
                            "$inc": {"sequenceValue": 1}
                        })['sequenceValue']

        sequenceValue += 1

        return sequenceValue
    
    def isDuplicate(self):

        userEmailCheck = FreshFoodsDBConnector('freshfoods','user').findOne({
                    "userEmail": self.userEmail
                })

        if userEmailCheck is not None:
            return True

        return False


class UserListing:

    myUser:User = None

    def __init__(self, user:User):
        self.myUser = user

    @staticmethod
    def getUserbyID(user_id):

        my_user = FreshFoodsDBConnector('freshfoods','user').findOne({
            "_id": user_id
        })

        my_user_details = FreshFoodsDBConnector('freshfoods','userdetails').findOne({
            "_id": user_id
        })

        myUserDetails = UserDetails().buildPublicUserDetailsObject(my_user_details['firstName'], my_user_details['lastName'])
        
        myUser:User = User().buildPublicUserObject(my_user['_id'], myUserDetails)


        return myUser


    



        


            


