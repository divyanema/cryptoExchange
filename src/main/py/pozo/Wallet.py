class Wallet:

    def __init__(self, walletId,userId,type,balance,updatedTimestamp,status):
        self.walletId = id
        self.userId = userId
        self.type=type
        self.balance=balance
        self.updatedTimestamp=updatedTimestamp
        self.status=status


    def __repr__(self):  
        return "walletId:% s userId:% s type:% s balance:% s updatedTimestamp:% s status:% s" % (self.walletId, self.userId,self.type,self.balance,self.updatedTimestamp,self.status)  