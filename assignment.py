import json
from datetime import date, datetime
from decimal import Decimal
from marshmallow import Schema, fields, post_load

class StockSchema(Schema):
    _type = fields.Str()
    symbol = fields.Str()
    date = fields.Date()
    open = fields.Decimal()
    high = fields.Decimal()
    low = fields.Decimal()
    close = fields.Decimal()
    volume = fields.Int()

    @post_load
    def make_stock(self, data, **kwargs):
        if "_type" in data and data["_type"] == "Stock":
            return Stock(
                symbol=data["symbol"],
                date=data["date"],
                open_=data["open"],
                high=data["high"],
                low=data["low"],
                close=data["close"],
                volume=data["volume"]
            )
        return data

class TradeSchema(Schema):
    _type = fields.Str()
    symbol = fields.Str()
    timestamp = fields.DateTime()
    order = fields.Str()
    price = fields.Decimal()
    volume = fields.Int()
    commission = fields.Decimal()

    @post_load
    def make_trade(self, data, **kwargs):
        if "_type" in data and data["_type"] == "Trade":
            return Trade(
                symbol=data["symbol"],
                timestamp=data["timestamp"],
                order=data["order"],
                price=data["price"],
                volume=data["volume"],
                commission=data["commission"]
            )
        return data

class Stock:
    def __init__(self, symbol, date, open_, high, low, close, volume):
        self.symbol = symbol
        self.date = date
        self.open = open_
        self.high = high
        self.low = low
        self.close = close
        self.volume = volume
        
class Trade:
    def __init__(self, symbol, timestamp, order, price, volume, commission):
        self.symbol = symbol
        self.timestamp = timestamp
        self.order = order
        self.price = price
        self.commission = commission
        self.volume = volume



class CustomEncoder(json.JSONEncoder):
       # Your implementation here
    def default(self, obj):
        if isinstance(obj, Stock):
            return {
                "_type": "Stock",
                "symbol": obj.symbol,
                "date": obj.date.isoformat() if isinstance(obj.date, (date, datetime)) else obj.date,
                "open": str(obj.open) if isinstance(obj.open, Decimal) else obj.open,
                "high": str(obj.high) if isinstance(obj.high, Decimal) else obj.high,
                "low": str(obj.low) if isinstance(obj.low, Decimal) else obj.low,
                "close": str(obj.close) if isinstance(obj.close, Decimal) else obj.close,
                "volume": obj.volume
            }
        elif isinstance(obj, Trade):
            return {
                "_type": "Trade",
                "symbol": obj.symbol,
                "timestamp": obj.timestamp.isoformat() if isinstance(obj.timestamp, (date, datetime)) else obj.timestamp,
                "order": obj.order,
                "price": str(obj.price) if isinstance(obj.price, Decimal) else obj.price,
                "volume": obj.volume,
                "commission": str(obj.commission) if isinstance(obj.commission, Decimal) else obj.commission
            }
        elif isinstance(obj, Decimal):
            return str(obj)
        elif isinstance(obj, (date, datetime)):
            return obj.isoformat()
            
        return json.JSONEncoder.default(self, obj)



def custom_decoder(obj_dict):
    """Custom decoder for JSON deserialization of Stock and Trade objects"""
    
    # Check if this is a typed object we need to convert
    if "_type" not in obj_dict:
        return obj_dict
        
    obj_type = obj_dict["_type"]
    
    if obj_type == "Stock":
        return Stock(
            symbol=obj_dict["symbol"],
            date=datetime.fromisoformat(obj_dict["date"]).date(),
            open_=Decimal(obj_dict["open"]),
            high=Decimal(obj_dict["high"]),
            low=Decimal(obj_dict["low"]),
            close=Decimal(obj_dict["close"]),
            volume=obj_dict["volume"]
        )
        
    elif obj_type == "Trade":
        return Trade(
            symbol=obj_dict["symbol"],
            timestamp=datetime.fromisoformat(obj_dict["timestamp"]),
            order=obj_dict["order"],
            price=Decimal(obj_dict["price"]),
            volume=obj_dict["volume"],
            commission=Decimal(obj_dict["commission"])
        )
        
    return obj_dict 

def serialize_with_marshmallow(obj):
    if isinstance(obj, Stock):
        return StockSchema().dumps({**obj.__dict__, "_type": "Stock"}, cls=CustomEncoder)
    elif isinstance(obj, Trade):
        return TradeSchema().dumps({**obj.__dict__, "_type": "Trade"}, cls=CustomEncoder)
    return None

def deserialize_with_marshmallow(obj, schema):
    """Deserialize JSON to Stock or Trade objects using Marshmallow."""
    return schema.loads(obj)

# activity = {
#     "quotes": [
#         Stock('TSLA', date(2018, 11, 22), 
#               Decimal('338.19'), Decimal('338.64'), Decimal('337.60'), Decimal('338.19'), 365_607),
#         Stock('AAPL', date(2018, 11, 22), 
#               Decimal('176.66'), Decimal('177.25'), Decimal('176.64'), Decimal('176.78'), 3_699_184),
#         Stock('MSFT', date(2018, 11, 22), 
#               Decimal('103.25'), Decimal('103.48'), Decimal('103.07'), Decimal('103.11'), 4_493_689)
#     ],
    
#     "trades": [
#         Trade('TSLA', datetime(2018, 11, 22, 10, 5, 12), 'buy', Decimal('338.25'), 100, Decimal('9.99')),
#         Trade('AAPL', datetime(2018, 11, 22, 10, 30, 5), 'sell', Decimal('177.01'), 20, Decimal('9.99'))
#     ]
# }