from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from transformers.sdt.utils import VariableName


class DecafNameError(Exception):

    def __init__(self, var_name: "VariableName", *args):
        super(DecafNameError, self).__init__(*args)
        self.var_name = var_name

    def __str__(self):
        return f'name "{self.var_name.name}" not found!'


class DecafNotFoundInLocalError(DecafNameError):
    def __str__(self):
        return f"name \"{self.var_name.name}\" is not in Local. Look for it in Global Scope"
