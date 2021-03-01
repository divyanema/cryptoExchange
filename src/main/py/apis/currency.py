from forex_python.converter import CurrencyRates

def RealTimeCurrencyExchangeRate(value) : 
 c = CurrencyRates()
 inrValue=value*c.get_rate('USD', 'INR')
 print(inrValue)
 return inrValue