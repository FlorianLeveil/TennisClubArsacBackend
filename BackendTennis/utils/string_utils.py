from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from typing import List


def string_list_to_camel_case(strings_to_convert: List[str]) -> str:
    final_string = ''
    counter = 0
    for _str in strings_to_convert:
        if counter == 0:
            final_string += _str.lower()
        else:
            final_string += _str.capitalize()
        counter += 1
    return final_string
