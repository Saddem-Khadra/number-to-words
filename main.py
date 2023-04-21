from fastapi import FastAPI, Depends, HTTPException
from num2words import CONVERTER_CLASSES
from pydantic import BaseModel
from converter import convert_to_currency, Item, validate_input_data

app = FastAPI()






@app.post("/api/converter/")
async def converter(item: Item = Depends(validate_input_data)):
    return {"message": convert_to_currency(
        number=item.number,
        language=item.language,
        decimal=item.decimal,
        delete_from_sentence=item.delete_from_sentence,
        currency=item.currency,
        decimal_currency=item.decimal_currency,
        separator=item.separator
    )}
