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
    def placeOrder(cls, new_order:Order):
        
        sequenceValue = cls.getNextOrderID()

        FreshFoodsDBConnector('freshfoods','orders').insert({
            "_id": sequenceValue,
            "itemID": new_order.itemID,
            "buyerID": new_order.buyerID
        })

        print("[Market] : User {0} placed an order for item : {1}".format(new_order.buyerID, new_order.itemName))


    @classmethod
    def addMarketItem(cls, user:User, item:MarketItem):

        sequenceValue = cls.getNextItemID()

        FreshFoodsDBConnector('freshfoods','market').insert({
            "_id": sequenceValue,
            "sellerID": item.sellerID,
            "itemName": item.itemName,
            "itemPrice": item.itemPrice
        })

    @classmethod
    def getNextItemID(cls):
    
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
    def getNextOrderID(cls):
    
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

    @classmethod
    def getAllItems(cls):

        market_items = FreshFoodsDBConnector('freshfoods','market').findAll({})

        allItems = []

        for x in market_items:
            item = MarketItem()
            item.itemID = x['_id']
            item.sellerID = x['sellerID']
            item.itemName = x['itemName']
            item.itemPrice = x['itemPrice']

            allItems.append(item)

        return allItems

        

    