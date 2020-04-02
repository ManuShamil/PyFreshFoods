import json
import bcrypt

from .db import FreshFoodsDBConnector
from .ff_jwt import ff_jwt
from .market import Market, MarketItem

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

        new_order = item.createOrder(self, qty)

        Market.placeOrder(new_order)


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


    



        


            


