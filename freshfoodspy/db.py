from pymongo import MongoClient

class FreshFoodsDBConnector:
    host = ""
    port = ""

    databaseName = ""
    collectionName = ""

    client = None


    def __init__(self, db_name, collection_name):
        self.host = "localhost"
        self.port = "27017"
        
        self.databaseName = db_name
        self.collectionName = collection_name

        self.connect()

    def connect(self):
        try:
            self.client = MongoClient('mongodb://{0}:{1}/'.format(self.host, self.port))
            self.isConnected = True

            return True
        except:
            self.isConnected = False

            return False


    def insert(self, document):
        if self.isConnected != True:
            return False    #if connection didn't succeed, do not proceed.

        return self.client[self.databaseName][self.collectionName].insert_one(document)

    def findAll(self, query, projection = {}):
        if self.isConnected != True:
            return False    #if connection didn't succeed, do not proceed.

        return self.client[self.databaseName][self.collectionName].find(query)

    def findOne(self, query, projection = {}):
        if self.isConnected != True:
            return False

        return self.client[self.databaseName][self.collectionName].find_one(query)

    def findOneAndUpdate(self, query, update, projection = {}):
        if self.isConnected != True:
            return False

        return self.client[self.databaseName][self.collectionName].find_one_and_update(query,update,projection)

    def update(self, query, data):
        if self.isConnected != True:
            return False

        return self.client[self.databaseName][self.collectionName].update_one(query, data)




