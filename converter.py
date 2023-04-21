from fastapi import HTTPException
from num2words import CONVERTER_CLASSES, num2words


def check_key_in_dict(language: str):
    # check if lan in language list
    if language not in CONVERTER_CLASSES.keys():
        raise HTTPException(
            status_code=404,
            detail=f"{language} not in language list"
        )
    return language


def check_int_in_list(decimal: int = None):
    if decimal in {2, 3} or decimal is None:
        return decimal
    else:
        raise HTTPException(
            status_code=404,
            detail=f"decimal number must be in {[2, 3]}"
        )


def convert_to_currency(
        number: int | float,
        language: str,
        decimal: int = None,
        delete_from_sentence: str = None,
        currency: str = None,
        decimal_currency: str = None,
        separator: str = None):
    if isinstance(number, float):
        if decimal is not None:
            # number_str = f"%.{decimal}f" % number
            number_str = f"{number:.{decimal}f}"
        else:
            number_str = str(number)
        print(number_str)
        print(type(number_str))
        num_list = number_str.split(".")
        part1 = num2words(int(num_list[0]), lang=language)
        part2 = num2words(int(num_list[1]), lang=language)
        if delete_from_sentence is not None:
            part1_list = part1.split(" ")
            part1_list = [i for i in part1_list if i != delete_from_sentence]
            part1 = " ".join(part1_list)
            part2_list = part2.split(" ")
            part2_list = [i for i in part2_list if i != delete_from_sentence]
            part2 = " ".join(part2_list)
        if currency is not None and decimal_currency is not None:
            return (
                f"{part1} {currency} {separator} {part2} {decimal_currency}".replace(
                    ',', ''
                )
                if separator is not None
                else f"{part1} {currency} {part2} {decimal_currency}".replace(
                    ',', ''
                )
            )
        if separator is not None:
            return f"{part1} {separator} {part2}".replace(',', '')
        else:
            return f"{part1} {part2}".replace(',', '')
    elif isinstance(number, int):
        result = num2words(number=number, lang=language)
        if delete_from_sentence is not None:
            result_list = result.split(" ")
            result_list = [i for i in result_list if i != delete_from_sentence]
            result = " ".join(result_list)
        if currency is not None:
            return f"{result} {currency}".replace(',', '')
        else:
            return f"{result}".replace(',', '')