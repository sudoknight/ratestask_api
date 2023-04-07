from datetime import date
from decimal import Decimal

from pydantic import BaseModel, Field


# this model is used for the response of get rates end point
class RatesSchema(BaseModel):
    day: date = Field(...)
    average_price: Decimal = Field(None)  # avg can be null in some cases
