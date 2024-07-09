from collections import defaultdict
from ._color import get_color
from ._mass import get_mass, calc_molecularweights


def count_elements(elements: str) -> dict[str, int]:
    element_dict = defaultdict(int)
    tmp_element = ""
    for char in elements:
        if char.isupper():
            if tmp_element:
                element_dict[tmp_element] += 1
                tmp_element = ""
        elif char.isnumeric():
            element_dict[tmp_element] += int(char)
            tmp_element = ""
            continue
        tmp_element += char
    if tmp_element:
        element_dict[tmp_element] += 1
    return element_dict


__all__ = ["count_elements" "get_color", "get_mass", "calc_molecularweights"]

del defaultdict, _mass, _color
