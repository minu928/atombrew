import re
from collections import defaultdict
from ._color import get_color
from ._mass import get_mass, calc_molecularweights


def parse_formula(formula: str, *, is_summation: bool = True) -> dict[str, int]:
    # 정규 표현식을 사용하여 원소와 개수를 추출
    pattern = r"([A-Z][a-z]?)(\d*)"
    elements = re.findall(pattern, formula)
    # 결과를 저장할 딕셔너리 초기화
    result = defaultdict(int)
    # 추출된 원소와 개수를 딕셔너리에 추가
    if is_summation:
        for element, count in elements:
            count = int(count) if count else 1
            result[element] += count
    return dict(result)


__all__ = ["parse_formula" "get_color", "get_mass", "calc_molecularweights"]

del _mass, _color
