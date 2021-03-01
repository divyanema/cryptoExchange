from flask import Flask
from apis.routes import routes
from apis.currency import RealTimeCurrencyExchangeRate

app = Flask(__name__)
app.register_blueprint(routes)

if __name__ == '__main__':
   
    app.run(debug=True)