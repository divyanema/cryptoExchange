from flask import Flask, jsonify,Blueprint,request
import shrimpy
from apis.currency import RealTimeCurrencyExchangeRate

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
    return jsonify({'user_id': user_id, 'account_id' :account_id}) 

@routes.route('/login/email/<emailID>', methods=['GET'])
def login(emailID): 
    return jsonify({'user_id': "16a00060-71b7-4007-9f3e-f5e2aab82989"})           

@routes.route('/trade/user/<userId>/account/<exchangeaccountId>', methods=['POST'])
def createTrade(userId,exchangeaccountId):
    data=request.get_json()
    create_trade_response = client.create_trade(userId,exchangeaccountId,data["fromSymbol"],data["toSymbol"],data["amount"])
    return jsonify({'id': create_trade_response["id"]})      

@routes.route('/trade/user/<userId>/account/<exchangeaccountId>/trade/<tradeID>', methods=['GET'])
def getTrade(userId,exchangeaccountId,tradeID):
    get_trade_response = client.get_trade_status(userId,exchangeaccountId,tradeID)
    trade = get_trade_response["trade"]
    trade["amount"] =  RealTimeCurrencyExchangeRate(float(trade["amount"]))
    return get_trade_response["trade"]   

@routes.route('/trade/user/<userId>/account/<exchangeaccountId>/open', methods=['GET'])
def getOpenTrade(userId,exchangeaccountId):
    get_trade_response = client.list_active_trades(userId,exchangeaccountId)
    return jsonify({'trades': get_trade_response})     

@routes.route('/trade/user/<userId>/account/<exchangeaccountId>/all', methods=['GET'])
def getAllTrade(userId,exchangeaccountId):
    get_trade_response = client.get_trade_status(userId,exchangeaccountId,"2fc7db03-60a6-48a1-b281-100ca0cd7b06")
    return jsonify({'trades': get_trade_response["trade"]})  

@routes.route('/limitOrder/user/<userId>/account/<exchangeaccountId>', methods=['POST'])
def createlimitOrder(userId,exchangeaccountId):
    data=request.get_json()
    create_trade_response = client.place_limit_order(userId,exchangeaccountId,data["baseSymbol"],data["quoteSymbol"],
    data["quantity"],data["price"],data["side"],data["timeInForce"])
    return jsonify({'id': create_trade_response["id"]})  

@routes.route('/limitOrder/user/<userId>/account/<exchangeaccountId>/trade/<tradeID>', methods=['GET'])
def getlimitOrder(userId,exchangeaccountId,tradeID):
    get_trade_response = client.get_limit_order_status(userId,exchangeaccountId,tradeID)
    return get_trade_response["order"]   

@routes.route('/limitOrder/user/<userId>/account/<exchangeaccountId>/open', methods=['GET'])
def getlimitOrderOpen(userId,exchangeaccountId):
    get_trade_response = client.list_open_orders(userId,exchangeaccountId)
    return jsonify({'orders': get_trade_response})     

@routes.route('/limitOrder/user/<userId>/account/<exchangeaccountId>/all', methods=['GET'])
def getlimitOrderAll(userId,exchangeaccountId):
    get_trade_response = client.get_limit_order_status(userId,exchangeaccountId,"38b66928-46c3-4d65-b2f5-b0b847f6d896")
    return jsonify({'orders': get_trade_response["order"]}) 

@routes.route('/limitOrder/user/<userId>/account/<exchangeaccountId>/trade/<tradeID>/cancel', methods=['DELETE'])
def getlimitOrderCancel(userId,exchangeaccountId,tradeID):
    get_trade_response = client.cancel_limit_order(userId,exchangeaccountId,"38b66928-46c3-4d65-b2f5-b0b847f6d896")
    return get_trade_response            

@routes.route('/balance/user/<userId>/account/<exchangeaccountId>', methods=['GET'])
def getBalance(userId,exchangeaccountId):
    get_trade_response = client.get_balance(userId,exchangeaccountId)
    return get_trade_response               