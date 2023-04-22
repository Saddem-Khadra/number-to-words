from fastapi import FastAPI, Depends
from converter import convert_to_currency, Item, validate_input_data

app = FastAPI()


@app.post("/api/converter/")
async def converter(item: Item = Depends(validate_input_data)):
    return {"message": convert_to_currency(item=item)}
