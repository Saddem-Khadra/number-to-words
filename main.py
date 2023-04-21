from fastapi import FastAPI, Depends

from converter import convert_to_currency, check_key_in_dict, check_int_in_list

app = FastAPI()


@app.post("/api/converter/")
async def converter(number: int | float,
                    delete_from_sentence: str = None,
                    currency: str = None,
                    decimal_currency: str = None,
                    separator: str = None,
                    decimal: int = Depends(check_int_in_list),
                    language: str = Depends(check_key_in_dict)):
    return {"message": convert_to_currency(
        number=number,
        language=language,
        decimal=decimal,
        delete_from_sentence=delete_from_sentence,
        currency=currency,
        decimal_currency=decimal_currency,
        separator=separator
    )}
