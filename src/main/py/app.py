from flask import Flask
from apis.routes import routes
from apis.currency import RealTimeCurrencyExchangeRate
from database.data import getAllData
from database.config import config

app = Flask(__name__)
app.register_blueprint(routes)

if __name__ == '__main__':
    userData = getAllData('"CRYPTO_USER"')
    print(userData)
    app.run(debug=True)