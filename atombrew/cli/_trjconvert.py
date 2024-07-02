from atombrew import Home
from ._main import subparsers

this_parser = subparsers.add_parser("trjconvert", help="Trajectory Convert")
this_parser.add_argument("-f", "--file", type=str, required=True, help="Token ID")
this_parser.add_argument("-o", "--out", type=str, required=True, help="Database ID")
this_parser.add_argument("-ofmt", type=str, default="auto", help="Open Format")
this_parser.add_argument("-wfmt", type=str, default="auto", help="Open Format")
this_parser.add_argument("-mode", type=str, default="w", help="Write Mode")
this_parser.add_argument("-start", type=int, default=0, help="Start Frame")
this_parser.add_argument("-end", type=int, default=None, help="End Frame")
this_parser.add_argument("-step", type=int, default=1, help="Frame Frequency")


def trjconvert(
    file,
    out,
    *,
    ofmt: str = "auto",
    wfmt: str = "auto",
    mode: str = "w",
    start=0,
    end=None,
    step=1,
    write_kwrgs: dict = None,
):

    home = Home(file, fmt=ofmt)
    home.write(out, fmt=wfmt, mode=mode, start=start, end=end, step=step, kwrgs=write_kwrgs)
