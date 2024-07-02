import numpy as np
from ..._writerinterface import WriterInterface


class POSCARWriter(WriterInterface):
    fmt = "poscar"

    def write(self, atoms, coords, *, box=None, force=None, **kwrgs):
        kind, numb = np.unique(atoms, return_counts=True)
        kind_line = "  ".join(kind) + "\n"
        numb_line = "  ".join(numb.astype(str)) + "\n"
        self.file.writelines(kind_line)
        scale = kwrgs.get("scale", 1.0)
        self.file.writelines(f" {scale:.16f}\n")
        box = box.astype(str)
        for r_box in box:
            self.file.writelines("  " + "  ".join(r_box) + "\n")
        self.file.writelines(" " + kind_line)
        self.file.writelines(" " + numb_line)
        self.file.writelines("Cartesian\n")
        for coord in coords:
            self.file.writelines(f"{coord[0]:16f} {coord[1]:16f} {coord[2]:16f}\n")
