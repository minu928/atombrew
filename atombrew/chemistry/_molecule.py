from scipy.constants import Avogadro
from .elements import parse_formula, calc_molecularweights
from typing import Dict, Union

# Constant for unit conversion (cubic angstrom to cubic cm)
ANGSTROM3_TO_CM3 = 1e-24


class Molecule:
    def __init__(self, formula: str) -> None:
        """
        Initialize a Molecule instance.

        Parameters
        ----------
        formula : str
            Chemical formula of the molecule.
        """
        self._formula = formula
        self._element_dict: Dict[str, int] = parse_formula(formula)
        self._mw: float = calc_molecularweights(element_count=self._element_dict)
        self._natoms: int = sum(self._element_dict.values())

    def __mul__(self, num: Union[int, float]) -> "Molecule":
        """
        Multiply the molecule by a number.

        Parameters
        ----------
        num : int or float
            Number to multiply the molecule by.

        Returns
        -------
        Molecule
            A new Molecule instance with multiplied formula.

        Raises
        ------
        TypeError
            If num is not a number.
        """
        if not isinstance(num, (int, float)):
            raise TypeError(f"Multiplication requires a number, got {type(num).__name__}")
        new_formula = "".join(f"{element}{count * num}" for element, count in self._element_dict.items())
        return Molecule(new_formula)

    def __add__(self, molecule: "Molecule") -> "Molecule":
        """
        Add two molecules together.

        Parameters
        ----------
        molecule : Molecule
            The molecule to add to this one.

        Returns
        -------
        Molecule
            A new Molecule instance representing the sum of the two molecules.

        Raises
        ------
        TypeError
            If the argument is not a Molecule instance.
        """
        if not isinstance(molecule, Molecule):
            raise TypeError(f"Addition requires an instance of Molecule, got {type(molecule).__name__}")
        return Molecule(self.formula + molecule.formula)

    def __repr__(self) -> str:
        """
        Return a string representation of the molecule.

        Returns
        -------
        str
            The chemical formula of the molecule.
        """
        return self.formula

    @property
    def mw(self) -> float:
        """
        Molecular weight of the molecule.

        Returns
        -------
        float
            Molecular weight in g/mol.
        """
        return self._mw

    @property
    def natoms(self) -> int:
        """
        Total number of atoms in the molecule.

        Returns
        -------
        int
            Number of atoms.
        """
        return self._natoms

    @property
    def formula(self) -> str:
        """
        Chemical formula of the molecule.

        Returns
        -------
        str
            The chemical formula.
        """
        return self._formula

    def calculate_volume(self, density: float) -> float:
        """
        Calculate volume of the molecule.

        Parameters
        ----------
        density : float
            Density in g/cm^3.

        Returns
        -------
        float
            Volume in Å^3.
        """
        return self.mw / (Avogadro * density * ANGSTROM3_TO_CM3)

    def calculate_density(self, volume: float) -> float:
        """
        Calculate density of the molecule.

        Parameters
        ----------
        volume : float
            Volume in Å^3.

        Returns
        -------
        float
            Density in g/cm^3.
        """
        return self.mw / (volume * Avogadro * ANGSTROM3_TO_CM3)

    def calculate_nmols(self, volume: float, density: float) -> float:
        """
        Calculate number of moles of the molecule.

        Parameters
        ----------
        volume : float
            Volume in Å^3.
        density : float
            Density in g/cm^3.

        Returns
        -------
        float
            Number of moles.
        """
        return density * volume * ANGSTROM3_TO_CM3 * Avogadro / self.mw
