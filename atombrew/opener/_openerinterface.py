from typing import TextIO


class OpenerInterface(object):
    def extract_snapshot(self, file: TextIO):
        pass
