from .db import FreshFoodsDBConnector
import json
from freshfoodspy import user

class MarketItem:

    itemID = -1
    itemName = ""
    itemPrice = 0
    itemQuantity = 0

    itemSeller = None

    def __init__(self, itemID=-1, seller=None, itemName="", itemPrice=0, itemQuantity=0):
        self.itemID = itemID
        self.itemSeller = seller
        self.itemName = itemName
        self.itemPrice = itemPrice
        self.itemQuantity = itemQuantity

    def createOrder(self, user, qty:int):

        order = Order().buildOrder(self, user, qty)

        return order

    @classmethod
    def buildObject(cls, user, itemName="", itemPrice=0, itemQuantity=0):
        """Used to construct the Item for adding to database exculsively
        
        Arguments:
            user {User} -- The user adding the item to the market
        """

        cls.itemSeller = user
        cls.itemName = itemName
        cls.itemPrice = itemPrice
        cls.itemQuantity = itemQuantity

        return cls

class Order:
    orderID = -1
    itemID = -1
    itemBuyer = None
    itemName = ""
    itemQuantity = -1
    totalPrice = -1

    def __init__(self, orderID = -1, itemID= -1, itemBuyer = None, itemName="", itemQuantity=-1, totalPrice=-1):
        self.orderID = orderID
        self.itemID = itemID
        self.itemBuyer = itemBuyer
        self.itemName = itemName
        self.itemQuantity = itemQuantity
        self.totalPrice = totalPrice

    @classmethod
    def buildOrder(cls, item:MarketItem, user, qty:int):
        """Creates an Order Object (required by MarketItem class to place Orders)
        
        Arguments:
            item {MarketItem} -- MarketItem Object
            user {User} -- User Object
        """
        
        cls.itemID = item.itemID
        cls.itemBuyer = user
        cls.itemName = item.itemName
        cls.itemQuantity = qty
        cls.totalPrice = qty * item.itemPrice

        return cls

class Market:

    @staticmethod
    def cancelOrder(order:Order):
        
        #reset the quantity of the market listing

        FreshFoodsDBConnector('freshfoods','market').update({
            "_id": order.itemID
        },{
            "$inc": {
                "itemQuantity": order.itemQuantity
            }
        })

        #delete the order from users order
        FreshFoodsDBConnector('freshfoods','orders').remove({
            "_id": order.orderID
        })

        print("[Market] : OrderID : {0} cancelled by user: {1}".format(order.orderID, order.itemBuyer.userID))


    @staticmethod
    def placeOrder(new_order:Order):

        if (Market.checkQuantity(new_order)):
        
            sequenceValue = Market.getNextOrderID()


            new_order.orderID = sequenceValue #set order id of the Order

            FreshFoodsDBConnector('freshfoods','orders').insert({
                "_id": sequenceValue,
                "itemID": new_order.itemID,
                "buyerID": new_order.buyer.userID,
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


            print("[Market] : OrderID : {3} User {0} placed an order for item : {1} : Quantity : {2}".format(new_order.buyer.userID, new_order.itemName, new_order.itemQuantity, new_order.orderID))

        else:
            
            print("[Market] : Failed! placing an order for item : {1} by User {0} : Quantity: {2}(Insufficient Quantity)".format(new_order.buyer.userID, new_order.itemName, new_order.itemQuantity))



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
            "sellerID": item.itemSeller.userID,
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
            item.itemSeller = user.UserListing.getUserbyID(x['sellerID'])
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
        my_item.itemSeller = user.UserListing.getUserbyID(item['sellerID'])
        my_item.itemName = item['itemName']
        my_item.itemPrice = item['itemPrice']
        my_item.itemQuantity = item['itemQuantity']

        return my_item

    @staticmethod
    def getOrdersbyUser(user):
        my_orders = FreshFoodsDBConnector('freshfoods','orders').findAll({
           "buyerID": user.userID
        })

        myOrders = []

        for order in my_orders:

            my_order = Order()
            my_order.orderID = order['_id']
            my_order.itemBuyer = user
            my_order.itemName = Market.getItem(int(order['itemID'])).itemName
            my_order.itemID = order['itemID']
            my_order.totalPrice = order['totalPrice']
            my_order.itemQuantity = order['itemQuantity']

            myOrders.append(my_order)

        return myOrders


    