from flask import Flask, jsonify,Blueprint,request,Response
import shrimpy
from apis.currency import RealTimeCurrencyExchangeRate,RealTimeCurrencyExchangeRate1
from database.data import getSpecificData, getSpecificDataList,insertUserData,insertWalletHistory,insertTrade,insertWallet,deleteWallet,updateWallet
from database.config import config
from pozo.User import User
from pozo.Wallet import Wallet
import uuid
from datetime import datetime, timezone
import json


routes= Blueprint('routes',__name__)

public_key = '2ee5af94090a913c6e6929660132a9c396fe10aed49489f5450a8f1cbdc458f3'
secret_key = '1e48238aac15d73891475c402f42f83d96c857cca64e81f3e8b0bc0019d421e69fc168dd7d24be72d9d66ed281ec052eb132faba413bb5833bfd36384ad8f3b3'
client = shrimpy.ShrimpyApiClient(public_key, secret_key)
exchange= "bittrex"
exchange_public_key="e2830f3f7b45491fa24c1a2996c47ebd"
exchange_secret_key="0b25006c0bf64302b4334c1db2b19d5e"

@routes.route('/', methods=['GET'])
def healthcheck():
    return jsonify({'healthcheck' : 'ok'})

@routes.route('/dashboard', methods=['GET'])
def dashboard(): 
    ticker = client.get_ticker('bittrex')
    for t in ticker: 
        t["priceUsd"]=RealTimeCurrencyExchangeRate(float(t["priceUsd"]))
    return jsonify({'ticker': ticker})  

@routes.route('/register', methods=['POST'])
def register(): 
    create_user_response = client.create_user("")
    user_id = create_user_response['id']  
    link_account_response = client.link_account(user_id,exchange,exchange_public_key,
    exchange_secret_key)                                                        
    account_id = link_account_response["id"]
    data=request.get_json()
    print(data)
    insertUserData(user_id,data["firstName"],data["lastName"],data["email"],data["panNo"],data["dob"],data["mobileNo"],account_id,"ACTIVE")
    walletId=uuid.uuid1()
    print (walletId)
    currentTimeStamp = datetime.now(timezone.utc)
    print(currentTimeStamp)
    insertWallet(walletId,user_id,0,currentTimeStamp,"ACTIVE")
    return jsonify({'userId': user_id, 'accountId' :account_id}) 

@routes.route('/login/email/<emailID>', methods=['GET'])
def login(emailID): 
    result= getSpecificData("crypto_user","email",emailID)
    return jsonify({'userId': result[0]})      

@routes.route('/getUserProfile/user/<userId>', methods=['GET'])
def getUserProfile(userId): 
    result= getSpecificData("crypto_user","user_id",userId)
    user=User(result[0],result[1],result[2],result[3],result[4],result[5],result[6],result[7],result[8])
    print(user)
    return jsonify({'userId': user.id, 'accountId' :user.exchangeAccountId,"firstName":user.firstName,"lastNme":user.lastName,"email":user.email,"panNo":user.panNo,"dob":user.dob,"mobileNo":user.mobileNo,"status":user.status})

@routes.route('/trade/user/<userId>', methods=['POST'])
def createTrade(userId):
    data=request.get_json()
    result= getSpecificData("crypto_user","user_id",userId)
    data["amount"]= RealTimeCurrencyExchangeRate1(float(data["amount"]))
    print(round(data["amount"],2))
    create_trade_response = client.create_trade(userId,result[7],data["fromSymbol"],data["toSymbol"],round(data["amount"],2))
    print(create_trade_response)
    if 'id' not in create_trade_response:
        return jsonify({'exception': create_trade_response["error"]})  
    insertTrade(userId,create_trade_response["id"])   
    return jsonify({'id': create_trade_response["id"]})      

@routes.route('/trade/user/<userId>/trade/<tradeID>', methods=['GET'])
def getTrade(userId,tradeID):
    result= getSpecificData("crypto_user","user_id",userId)
    get_trade_response = client.get_trade_status(userId,result[7],tradeID)
    if 'trade' not in get_trade_response:
        return jsonify({'exception': get_trade_response["error"]}) 
    trade = get_trade_response["trade"]
    trade["amount"] =  RealTimeCurrencyExchangeRate(float(trade["amount"]))
    if trade["fromSymbol"]=="INR":
        updateWalletusers(userId,"SELL",trade["amount"])
    if trade["toSymbol"]=="INR":
        updateWalletusers(userId,"BUY",trade["amount"])
    return get_trade_response["trade"]   

@routes.route('/trade/user/<userId>/open', methods=['GET'])
def getOpenTrade(userId):
    result= getSpecificData("crypto_user","user_id",userId)
    get_trade_response = client.list_active_trades(userId,result[7])
    if 'trade' not in get_trade_response:
        return jsonify({'exception': get_trade_response["error"]}) 
    for trade in get_trade_response: 
        trade1=trade["trade"]
        trade1["amount"]= RealTimeCurrencyExchangeRate(float(trade1["amount"]))
    return jsonify({'trades': get_trade_response})     

@routes.route('/trade/user/<userId>/all', methods=['GET'])
def getAllTrade(userId):
    result= getSpecificData("crypto_user","user_id",userId)
    trades= getSpecificDataList("crypto_trade","user_id",userId)
    print(trades)
    thislist =[]
    for trade in trades:    
        get_trade_response = client.get_trade_status(userId,result[7],trade[1])
        if 'trade' not in get_trade_response:
            return jsonify({'exception': get_trade_response["error"]}) 
        print(get_trade_response)
        trade1=get_trade_response["trade"]
        trade1["amount"]= RealTimeCurrencyExchangeRate(float(trade1["amount"]))
        thislist.append(get_trade_response["trade"])
    print (thislist)   
    return jsonify({'trades': thislist})  

@routes.route('/limitOrder/user/<userId>', methods=['POST'])
def createlimitOrder(userId):
    data=request.get_json()
    result= getSpecificData("crypto_user","user_id",userId)
    data["price"]= RealTimeCurrencyExchangeRate1(float(data["price"]))
    create_trade_response = client.place_limit_order(userId,result[7],data["baseSymbol"],data["quoteSymbol"],
    data["quantity"],round(data["price"],2),data["side"],data["timeInForce"])
    if 'id' not in create_trade_response:
        return jsonify({'exception': create_trade_response["error"]}) 
    insertTrade(userId,create_trade_response["id"])
    return jsonify({'id': create_trade_response["id"]})  

@routes.route('/limitOrder/user/<userId>/trade/<tradeID>', methods=['GET'])
def getlimitOrder(userId,tradeID):
    result= getSpecificData("crypto_user","user_id",userId)
    get_trade_response = client.get_limit_order_status(userId,result[7],tradeID)
    if 'order' not in get_trade_response:
        return jsonify({'exception': get_trade_response["error"]}) 
    trade = get_trade_response["order"]
    trade["amount"] =  RealTimeCurrencyExchangeRate(float(trade["amount"]))
    if trade["fromSymbol"]=="INR":
        updateWalletusers(userId,"SELL",trade["amount"])
    if trade["toSymbol"]=="INR":
        updateWalletusers(userId,"BUY",trade["amount"])
    return get_trade_response["order"]   

@routes.route('/limitOrder/user/<userId>/open', methods=['GET'])
def getlimitOrderOpen(userId):
    result= getSpecificData("crypto_user","user_id",userId)
    get_trade_response = client.list_open_orders(userId,result[7])
    if 'order' not in get_trade_response:
        return jsonify({'exception': get_trade_response["error"]}) 
    for trade in get_trade_response: 
        trade1=trade["order"]
        trade1["amount"]= RealTimeCurrencyExchangeRate(float(trade1["amount"]))
    return jsonify({'orders': get_trade_response})     

@routes.route('/limitOrder/user/<userId>/all', methods=['GET'])
def getlimitOrderAll(userId):
    result= getSpecificData("crypto_user","user_id",userId)
    trades= getSpecificDataList("crypto_trade","user_id",userId)
    print(trades)
    thislist =[]
    for trade in trades:    
        get_trade_response = client.get_limit_order_status(userId,result[7],trade[1])
        if 'order' not in get_trade_response:
            return jsonify({'exception': get_trade_response["error"]}) 
        print(get_trade_response)
        trade1=get_trade_response["order"]
        trade1["amount"]= RealTimeCurrencyExchangeRate(float(trade1["amount"]))
        thislist.append(get_trade_response["order"])
    print (thislist)   
    return jsonify({'orders': thislist}) 

@routes.route('/limitOrder/user/<userId>/trade/<tradeID>/cancel', methods=['DELETE'])
def getlimitOrderCancel(userId,tradeID):
    result= getSpecificData("crypto_user","user_id",userId)
    get_trade_response = client.cancel_limit_order(userId,result[7],tradeID)
    return get_trade_response            

@routes.route('/balance/user/<userId>', methods=['GET'])
def getBalance(userId):
    result= getSpecificData("crypto_user","user_id",userId)
    get_trade_response = client.get_balance(userId,result[7])
    if 'balances' not in get_trade_response:
        return jsonify({'exception': get_trade_response["balances"]}) 
    balances=get_trade_response["balances"]
    print(balances)
    if balances  :
        balances["usdValue"]=RealTimeCurrencyExchangeRate(float(balances["usdValue"]))
    return get_trade_response  

@routes.route('/marketData/from/<from_symbol>/to/<to_symbol>', methods=['GET'])
def getmarketData(from_symbol,to_symbol):
    get_trade_response = client.get_candles(exchange,from_symbol,from_symbol,"1d")
    return jsonify({'volume': get_trade_response})

@routes.route('/wallet/updateBalance/<userId>', methods=['PUT'])
def updateWalletuser(userId):
    data=request.get_json()
    print(data)
    updateWalletusers(userId,data["type"],data["balance"])
    return jsonify({'status' : 'ok'})

def updateWalletusers(userId,type,balance):
    currentTimeStamp = datetime.now(timezone.utc)
    print(currentTimeStamp)
    result= getSpecificData("crypto_wallet","user_id",userId)
    if (type=='ADD') or (type=='SELL'):
        print(result[2])
        new_balance=float(result[2])+float(balance)
        print(new_balance)
    if (type=='WITHDRAW') or (type=='BUY'):
        new_balance=float(result[2])- float(balance) 
        print(new_balance)
    print(new_balance)       
    updateWallet(result[0],userId,new_balance,currentTimeStamp)
    insertWalletHistory(result[0],userId,type,balance,currentTimeStamp,"ACTIVE")
    return jsonify({'status' : 'ok'})    

@routes.route('/wallet/getBalance/<userId>', methods=['GET'])
def getWalletBalance(userId):
    result= getSpecificData("crypto_wallet","user_id",userId)
    balance=float(result[2])
    print("else case",balance)
    return jsonify({'userId': userId, 'balance' :balance})

@routes.route('/wallet/getBalanceHistory/<userId>', methods=['GET'])
def getWalletBalanceHIstory(userId):
    print(userId)
    walletHistoryDetails = getSpecificDataList("crypto_wallet_history","user_id",userId)
    print(walletHistoryDetails)
    thislist =[]
    for row in walletHistoryDetails:
        print(row[0])
        walletHistory={"walletId":row[0],"userId":row[1],"type":row[2],"balance":float(row[3]),"updatedTimestamp":str(row[4]),"status":row[5]}
        thislist.append(walletHistory)
    print("List:",thislist)
    return jsonify(thislist)
    
@routes.route('/wallet/delete/<userId>', methods=['GET'])
def deleteBalance(userId):
    print(userId)
    currentTimeStamp = datetime.now(timezone.utc)
    print(currentTimeStamp)
    deleteWallet(currentTimeStamp,"INACTIVE","user_id",userId)
    return jsonify({'status' : 'ok'})



    