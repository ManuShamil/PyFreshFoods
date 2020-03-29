import json
import bcrypt

from .db import FreshFoodsDBConnector
from .ff_jwt import ff_jwt

#Main Data Model
class User:
    userID = ""
    userEmail = ""
    userToken = ""

    def __init__(self,userID=None, email="", token=""):
        """Creates a user Object
        
        Arguments:
            email {str} -- Email of the user
        """

        self.userID = userID
        self.userEmail = email
        self.userToken = token

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

                return User(user.userID, user.userEmail, token) #return newly created user object with token included
                
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

        sequenceValue = self.updateAndGetNextSequence()
                    
        FreshFoodsDBConnector('freshfoods','user').insert({
                                "_id": sequenceValue,
                                "userEmail": self.userEmail,
                                "userPassword": hashedpassword
                            })

        #now try logging in to the account

        print("User Registration completed succesfully!")

        user = UserLogin(self.userEmail).loginEmail(self.userPassword)


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


    



        


            


