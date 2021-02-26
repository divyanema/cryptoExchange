from flask import Flask, jsonify,Blueprint
import shrimpy

routes= Blueprint('routes',__name__)

@routes.route('/', methods=['GET'])
def healthcheck():
    return jsonify({'healthcheck' : 'ok'})

@routes.route('/dashboard', methods=['GET'])
def dashboard():
    public_key = '2ee5af94090913c6e6929660132a9c396fe10aed49489f5450a8f1cbdc458f3'
    secret_key = '1e48238aac15d73891475c402f42f83d96c857cca64e81f3e8b0bc0019d421e69fc168dd7d24be72d9d66ed281ec052eb132faba413bb5833bfd36384ad8f3b3'
    client = shrimpy.ShrimpyApiClient(public_key, secret_key)
    ticker = client.get_ticker('bittrex')
    return jsonify({'ticker': ticker})    