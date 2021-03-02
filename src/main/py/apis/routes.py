from flask import Flask, jsonify,Blueprint,request
import shrimpy
from apis.currency import RealTimeCurrencyExchangeRate
from database.data import getSpecificData
from database.data import insertUserData
from database.config import config
from pozo.User import User
import json
from types import SimpleNamespace

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
    create_trade_response = client.create_trade(userId,"87272",data["fromSymbol"],data["toSymbol"],data["amount"])
    return jsonify({'id': create_trade_response["id"]})      

@routes.route('/trade/user/<userId>/trade/<tradeID>', methods=['GET'])
def getTrade(userId,tradeID):
    get_trade_response = client.get_trade_status(userId,"87272",tradeID)
    trade = get_trade_response["trade"]
    trade["amount"] =  RealTimeCurrencyExchangeRate(float(trade["amount"]))
    return get_trade_response["trade"]   

@routes.route('/trade/user/<userId>/open', methods=['GET'])
def getOpenTrade(userId):
    get_trade_response = client.list_active_trades(userId,"87272")
    return jsonify({'trades': get_trade_response})     

@routes.route('/trade/user/<userId>/all', methods=['GET'])
def getAllTrade(userId):
    get_trade_response = client.get_trade_status(userId,"87272","2fc7db03-60a6-48a1-b281-100ca0cd7b06")
    return jsonify({'trades': get_trade_response["trade"]})  

@routes.route('/limitOrder/user/<userId>', methods=['POST'])
def createlimitOrder(userId):
    data=request.get_json()
    create_trade_response = client.place_limit_order(userId,"87272",data["baseSymbol"],data["quoteSymbol"],
    data["quantity"],data["price"],data["side"],data["timeInForce"])
    return jsonify({'id': create_trade_response["id"]})  

@routes.route('/limitOrder/user/<userId>/trade/<tradeID>', methods=['GET'])
def getlimitOrder(userId,tradeID):
    get_trade_response = client.get_limit_order_status(userId,"87272",tradeID)
    return get_trade_response["order"]   

@routes.route('/limitOrder/user/<userId>/open', methods=['GET'])
def getlimitOrderOpen(userId):
    get_trade_response = client.list_open_orders(userId,"87272")
    return jsonify({'orders': get_trade_response})     

@routes.route('/limitOrder/user/<userId>/all', methods=['GET'])
def getlimitOrderAll(userId):
    get_trade_response = client.get_limit_order_status(userId,"87272","38b66928-46c3-4d65-b2f5-b0b847f6d896")
    return jsonify({'orders': get_trade_response["order"]}) 

@routes.route('/limitOrder/user/<userId>/trade/<tradeID>/cancel', methods=['DELETE'])
def getlimitOrderCancel(userId,tradeID):
    get_trade_response = client.cancel_limit_order(userId,"87272","38b66928-46c3-4d65-b2f5-b0b847f6d896")
    return get_trade_response            

@routes.route('/balance/user/<userId>', methods=['GET'])
def getBalance(userId):
    get_trade_response = client.get_balance(userId,"87272")
    return get_trade_response  

@routes.route('/marketData/from/<from_symbol>/to/<to_symbol>', methods=['GET'])
def getmarketData(from_symbol,to_symbol):
    get_trade_response = client.get_candles(exchange,from_symbol,from_symbol,"1d")
    return jsonify({'volume': get_trade_response})                    