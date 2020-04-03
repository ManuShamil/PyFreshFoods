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
    totalPrice = -1

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
        self.totalPrice = qty * item.itemPrice

class Market:

    @staticmethod
    def placeOrder(new_order:Order):

        if (Market.checkQuantity(new_order)):
        
            sequenceValue = Market.getNextOrderID()


            FreshFoodsDBConnector('freshfoods','orders').insert({
                "_id": sequenceValue,
                "itemID": new_order.itemID,
                "buyerID": new_order.buyerID,
                "itemQuantity": new_order.itemQuantity,
                "totalPrice": new_order.totalPrice
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

        else:
            
            print("[Market] : Failed! placing an order for item : {1} by User {0} : Quantity: {2}(Insufficient Quantity)".format(new_order.buyerID, new_order.itemName, new_order.itemQuantity))



    @staticmethod
    def checkQuantity(order:Order):

        quantity = FreshFoodsDBConnector('freshfoods', 'market').findOne({
            "_id": order.itemID
        })['itemQuantity']

        if (order.itemQuantity <= quantity):
            return True
        else:
            return False



    @staticmethod
    def addMarketItem(user, item:MarketItem):

        sequenceValue = Market.getNextItemID()

        FreshFoodsDBConnector('freshfoods','market').insert({
            "_id": sequenceValue,
            "sellerID": item.sellerID,
            "itemName": item.itemName,
            "itemPrice": item.itemPrice,
            "itemQuantity": item.itemQuantity
        })

    @staticmethod
    def getNextItemID():
    
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

    @staticmethod
    def getNextOrderID():
    
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

    @staticmethod
    def getAllItems():

        market_items = FreshFoodsDBConnector('freshfoods','market').findAll({})

        allItems = []

        for x in market_items:
            item = MarketItem()
            item.itemID = x['_id']
            item.sellerID = x['sellerID']
            item.itemName = x['itemName']
            item.itemPrice = x['itemPrice']
            item.itemQuantity = x['itemQuantity']

            allItems.append(item)

        return allItems

    @staticmethod
    def getItem(item_id):

        item = FreshFoodsDBConnector('freshfoods','market').findOne({
            "_id": item_id
        })

        my_item = MarketItem()
        my_item.itemID = item['_id']
        my_item.sellerID = item['sellerID']
        my_item.itemName = item['itemName']
        my_item.itemPrice = item['itemPrice']
        my_item.itemQuantity = item['itemQuantity']

        return my_item

        

    