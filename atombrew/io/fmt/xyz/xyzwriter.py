from ..._writerinterface import WriterInterface


class XYZWriter(WriterInterface):
    fmt = "xyz"

    def write(self, atoms, coords, *, frame=None, box=None, force=None, **kwrgs):
        natoms = len(atoms)
        self.file.writelines(f"\t{natoms}\n")
        self.file.writelines(f"\n")
        xyzlines = "\n".join(
            [f"{iatom:>4s}\t{ixyz[0]:>16s}\t{ixyz[1]:>16s}\t{ixyz[2]:>16s}" for iatom, ixyz in zip(atoms, coords)]
        )
        self.file.writelines(xyzlines)
        self.file.writelines("\n")
