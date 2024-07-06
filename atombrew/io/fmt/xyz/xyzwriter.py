from ..._trjwriterinterface import TRJWriterInterface


class XYZWriter(TRJWriterInterface):
    fmt = "xyz"

    def write(self, atoms, coords, *, box=None, forces=None, velocities=None, **kwrgs):
        natoms = len(atoms)
        self.file.writelines(f"\t{natoms}\n")
        self.file.writelines(f"\n")
        xyzlines = "\n".join(
            [f"{iatom[0]:>4s}\t{ixyz[0]:>16f}\t{ixyz[1]:>16f}\t{ixyz[2]:>16f}" for iatom, ixyz in zip(atoms, coords)]
        )
        self.file.writelines(xyzlines)
        self.file.writelines("\n")
