from ._main import parser
from ._trjconvert import trjconvert

func_dict = {"trjconvert": trjconvert}


def parsing():
    args = parser.parse_args().__dict__
    command = args.pop("command")
    return func_dict[command](**args)
