from .db import FreshFoodsDBConnector

class MarketItem:

    itemID = -1
    sellerID = -1
    itemName = ""
    itemPrice = 0
    itemQuantity = 0

    def __init__(self, itemID=-1, sellerID=-1, itemName="", itemPrice=0, itemQuantity=0):
        self.itemID = itemID
        self.sellerID = sellerID
        self.itemName = itemName
        self.itemPrice = itemPrice
        self.itemQuantity = itemQuantity

    def createOrder(self, user, qty:int):

        order = Order(self, user, qty)

        return order

    @classmethod
    def buildObject(cls, user, itemName="", itemPrice=0, itemQuantity=0):
        """Used to construct the Item for adding to database exculsively
        
        Arguments:
            user {User} -- The user adding the item to the market
        """

        cls.sellerID = user.userID
        cls.itemName = itemName
        cls.itemPrice = itemPrice
        cls.itemQuantity = itemQuantity

        return cls

class Order:

    itemID = -1
    buyerID = -1
    itemName = ""
    itemQuantity = -1

    def __init__(self, item:MarketItem, user, qty:int):
        """Creates an Order Object (required by MarketItem class to place Orders)
        
        Arguments:
            item {MarketItem} -- MarketItem Object
            user {User} -- User Object
        """
        
        self.itemID = item.itemID
        self.buyerID = user.userID
        self.itemName = item.itemName
        self.itemQuantity = qty

class Market:

    @classmethod
    def placeOrder(cls, new_order:Order):
        
        sequenceValue = cls.getNextOrderID()

        print(new_order.itemID)

        FreshFoodsDBConnector('freshfoods','orders').insert({
            "_id": sequenceValue,
            "itemID": new_order.itemID,
            "buyerID": new_order.buyerID,
            "itemQuantity": new_order.itemQuantity
        })

        #decrement the quantity in new Market Listing

        FreshFoodsDBConnector('freshfoods', 'market').update({
            "_id": new_order.itemID
        },
        {
            "$inc": {
                "itemQuantity": -new_order.itemQuantity
            }
        },
        insert_new=False)



        print("[Market] : User {0} placed an order for item : {1} : Quantity : {2}".format(new_order.buyerID, new_order.itemName, new_order.itemQuantity))


    @classmethod
    def addMarketItem(cls, user, item:MarketItem):

        sequenceValue = cls.getNextItemID()

        FreshFoodsDBConnector('freshfoods','market').insert({
            "_id": sequenceValue,
            "sellerID": item.sellerID,
            "itemName": item.itemName,
            "itemPrice": item.itemPrice,
            "itemQuantity": item.itemQuantity
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

        

    