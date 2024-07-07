from ..._trjwriterinterface import TRJWriterInterface


class EXTXYZWriter(TRJWriterInterface):
    fmt = "extxyz"
    is_value_exist_dict = {
        "force": False,
    }

    def write(self, atoms, coords, forces, velocities, *, box=None, **kwrgs):
        file = self.file
        file.writelines(f"\t{len(atoms)}\n")
        file.writelines(self._make_infoline(box=box, isinforces=forces.size, isinvelocities=velocities.size))
        file.writelines(self._make_xyzline(atoms=atoms, coords=coords, forces=forces, velocities=velocities))

    def _make_infoline(self, box, isinforces: bool, isinvelocities: bool):
        assert box is not None, ValueError("box is None...")
        infoline = f'Lattice="' + " ".join(box.flatten().astype(str)) + '"'
        infoline += " Properties=species:S:1:pos:R:3"
        if isinforces:
            infoline += ":forces:R:3"
        if isinvelocities:
            infoline += ":velocities:R:3"
        infoline += ' pbc="True True True"\n'
        return infoline

    def _make_xyzline(self, atoms, coords, forces, velocities):
        xyzline = ""
        iterables = [atoms, coords]
        if forces.size:
            iterables.append(forces)
        if velocities.size:
            iterables.append(velocities)
        for atom, *properties in zip(*iterables):
            xyzline += f"{atom[0]:>4s}"
            for property in properties:
                xyzline += f" {property[0]:>16f} {property[1]:>16f} {property[2]:>16f}"
            xyzline += "\n"
        return xyzline
