from typing import Union
from fastapi import HTTPException
from num2words import num2words, CONVERTER_CLASSES
from pydantic import BaseModel


class Item(BaseModel):
    number: int | float
    delete_from_sentence: str | None = None
    currency: str | None = None
    decimal_currency: str | None = None
    separator: str | None = None
    decimal: int | None = None
    language: str

    class Config:
        smart_union = True


def validate_input_data(item: Item):
    # check if lan in language list
    if item.language not in CONVERTER_CLASSES.keys():
        raise HTTPException(
            status_code=404,
            detail=f"{item.language} not in language list"
        )
    if item.decimal not in {2, 3} and item.decimal is not None:
        raise HTTPException(
            status_code=404,
            detail=f"decimal number must be in {[2, 3]}"
        )
    return item


def convert_to_currency(item: Item) -> str:
    if isinstance(item.number, float):
        return when_number_is_float(item=item)
    elif isinstance(item.number, int):
        return when_number_is_int(item=item)


def when_number_is_int(item: Item) -> str:
    result = num2words(number=item.number, lang=item.language)
    if item.delete_from_sentence is not None:
        result_list = result.split(" ")
        result_list = [i for i in result_list if i != item.delete_from_sentence]
        result = " ".join(result_list)
    if item.currency is not None:
        return f"{result} {item.currency}".replace(',', '')
    else:
        return f"{result}".replace(',', '')


def when_number_is_float(item: Item) -> str:
    number_str = f"{item.number:.{item.decimal}f}" if item.decimal is not None else str(item.number)
    num_list = number_str.split(".")
    part1 = num2words(int(num_list[0]), lang=item.language)
    part2 = num2words(int(num_list[1]), lang=item.language)
    if item.delete_from_sentence is not None:
        part1_list = part1.split(" ")
        part1_list = [i for i in part1_list if i != item.delete_from_sentence]
        part1 = " ".join(part1_list)
        part2_list = part2.split(" ")
        part2_list = [i for i in part2_list if i != item.delete_from_sentence]
        part2 = " ".join(part2_list)
    if item.currency is not None and item.decimal_currency is not None:
        return (
            f"{part1} {item.currency} {item.separator} {part2} {item.decimal_currency}".replace(
                ',', ''
            )
            if item.separator is not None
            else f"{part1} {item.currency} {part2} {item.decimal_currency}".replace(
                ',', ''
            )
        )
    if item.separator is not None:
        return f"{part1} {item.separator} {part2}".replace(',', '')
    else:
        return f"{part1} {part2}".replace(',', '')
