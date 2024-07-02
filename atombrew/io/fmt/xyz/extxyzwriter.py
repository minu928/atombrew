from ..._writerinterface import WriterInterface


class EXTXYZWriter(WriterInterface):
    fmt = "extxyz"
    secondline_properties = ("energy", "stress")
    is_value_exist_dict = {
        "force": False,
    }

    def write(self, atoms, coords, *, box=None, force=None, **kwrgs):
        self.file.writelines(f"\t{len(atoms)}\n")
        self.file.writelines(self._make_secondline(box=box, **kwrgs))
        xyzlines = "\n".join(self._make_propertyline(atom=atoms, coord=coords, force=kwrgs.get("force", None)))
        self.file.writelines(xyzlines)
        self.file.writelines("\n")

    def _make_secondline(self, box, **kwrgs):
        propeties_words = " Properties=species:S:1:pos:R:3"
        assert box is not None, ValueError("box is None...")
        secondline = f'Lattice="' + " ".join(box.flatten().astype(str)) + '"'
        for key, val in kwrgs.items():
            if key in self.secondline_properties:
                secondline += f" {key}={val}"
            elif key in self.is_value_exist_dict:
                propeties_words += f"{key}:R:3"
                self.is_value_exist_dict[key] = True
        secondline += ' pbc="True True True"\n'
        return secondline

    def _make_propertyline(self, atom, coord, *, force=None):
        propertyline = [f"{iatom[0]:>4s}\t{ixyz[0]:>16f}\t{ixyz[1]:>16f}\t{ixyz[2]:>16f}" for iatom, ixyz in zip(atom, coord)]
        if force is not None:
            propertyline = [
                f"{p}\t{iforce[0]:>16s}\t{iforce[2]:>16s}\t{iforce[2]:>16s}" for p, iforce in zip(propertyline, force)
            ]
        return propertyline
