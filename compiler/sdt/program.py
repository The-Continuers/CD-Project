from typing import *

from .declaration import Declaration


class Program:
    def __init__(self, declarations: List[Declaration]) -> None:
        self.declarations = declarations
