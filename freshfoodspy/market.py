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

    def createOrder(self, user:User):

        order = Order(self, user)

        return order


class Order:

    itemID = ""
    buyerID = ""
    itemName = ""

    def __init__(self, item:MarketItem, user:User):
        
        self.itemID = item.itemID
        self.buyerID = user.userID
        self.itemName = item.itemName

class Market:

    @classmethod
    def placeOrder(self, new_order:Order):
        
        sequenceValue = self.getNextOrderID()

        FreshFoodsDBConnector('freshfoods','orders').insert({
            "_id": sequenceValue,
            "itemID": new_order.itemID,
            "buyerID": new_order.buyerID
        })

        print("[Market] : User {0} placed an order for item : {1}".format(new_order.buyerID, new_order.itemName))





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

        

    