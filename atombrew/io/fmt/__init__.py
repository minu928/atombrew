from importlib import import_module
from pathlib import Path


HEAD = "atombrew.io.fmt"
for fmt_folder in Path(__file__).parent.glob("*"):
    for fmt_py in fmt_folder.glob("*.py"):
        if not "__" in fmt_folder.stem:
            import_module(f".{fmt_folder.stem}.{fmt_py.stem}", HEAD)
del import_module, Path
