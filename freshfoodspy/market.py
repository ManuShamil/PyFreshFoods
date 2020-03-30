from .user import User
from .db import FreshFoodsDBConnector

class MarketItem:

    itemID = ""
    sellerID = ""
    itemName = ""
    itemPrice = ""

    def __init__(self, itemID="", sellerID="", itemName="", itemPrice=""):
        self.itemID = itemID
        self.sellerID = sellerID
        self.itemName = itemName
        self.itemPrice = itemPrice

class Order:

    itemID = ""
    buyerID = ""

    def __init__(self):
        pass

class Market:

    @classmethod
    def placeOrder():
        
        sequenceValue = self.getNextOrderID()

        FreshFoodsDBConnector('freshfoods','orders').insert({
            "_id": sequenceValue,
            "sellerID": item.sellerID,
            "itemName": item.itemName,
            "itemPrice": item.itemPrice
        })



    @classmethod
    def addMarketItem(self, user:User, item:MarketItem):

        sequenceValue = self.getNextItemID()

        FreshFoodsDBConnector('freshfoods','market').insert({
            "_id": sequenceValue,
            "sellerID": item.sellerID,
            "itemName": item.itemName,
            "itemPrice": item.itemPrice
        })

    @classmethod
    def getNextItemID(self):
    
        sequenceValue = FreshFoodsDBConnector('freshfoods','counter').findOneAndUpdate({
                            "$and": [
                                {
                                    "collectionName": 'market'
                                },{
                                    "columnName": '_id'
                                }
                        ]},
                        {
                            "$inc": {"sequenceValue": 1}
                        })['sequenceValue']

        sequenceValue += 1

        return sequenceValue

        @classmethod
    def getNextOrderID(self):
    
        sequenceValue = FreshFoodsDBConnector('freshfoods','counter').findOneAndUpdate({
                            "$and": [
                                {
                                    "collectionName": 'orders'
                                },{
                                    "columnName": '_id'
                                }
                        ]},
                        {
                            "$inc": {"sequenceValue": 1}
                        })['sequenceValue']

        sequenceValue += 1

        return sequenceValue

        

    