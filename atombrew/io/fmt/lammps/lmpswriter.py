import numpy as np
from ..._writerinterface import WriterInterface


class LMPSWriter(WriterInterface):
    fmt = "lmps"

    def write(self, atoms, coords, *, box=None, force=None, **kwrgs):
        atoms = atoms.flatten()
        atomorder = kwrgs.get("atomorder", np.unique((atoms)))
        atomdict = {atom: i + 1 for i, atom in enumerate(atomorder)}
        file = self.file
        file.writelines(f"LMPS By AtomBrew\n\n")
        file.writelines(f"{len(atoms)} atoms\n")
        file.writelines(f"{len(atomdict)} atom types\n\n")
        for rb, a in zip(np.sum(box, axis=0), ["x", "y", "z"]):
            file.writelines(f"0 {rb:<16} {a}lo {a}hi\n")
        file.writelines("\n\nAtoms\n\n")
        if atoms[0].isalnum():
            atoms = [atomdict[atom] for atom in atoms]
        for i, (atom, coord) in enumerate(zip(atoms, coords)):
            file.writelines(f"{i+1} {atom} {coord[0]} {coord[1]} {coord[2]}\n")
