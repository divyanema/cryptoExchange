from forex_python.converter import CurrencyRates

def RealTimeCurrencyExchangeRate(usdvalue) : 
 c = CurrencyRates()
 inrValue=usdvalue*c.get_rate('USD', 'INR')
 print(inrValue)
 return inrValue


def RealTimeCurrencyExchangeRate1(inrvalue1) : 
 c1 = CurrencyRates()
 print(inrvalue1)
 print(c1.get_rate('INR', 'USD'))
 usdValue1=inrvalue1*c1.get_rate('INR', 'USD')
 print(usdValue1)
 return usdValue1