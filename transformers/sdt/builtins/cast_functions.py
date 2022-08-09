from dataclasses import dataclass
from typing import TYPE_CHECKING, Dict, List

from transformers.sdt import Function, Variable
from transformers.sdt.stmts import StatementBlock
from transformers.sdt.utils import VariableName

from transformers.types import DecafInt, DecafDouble, DecafBool

if TYPE_CHECKING:
    from transformers.types import DecafType


@dataclass
class CastFunction:
    parameter_type: "DecafType"
    return_type: "DecafType"


cast_func_mapping: Dict[str, "CastFunction"] = {
    'dtoi': CastFunction(parameter_type=DecafDouble, return_type=DecafInt),
    'itod': CastFunction(parameter_type=DecafInt, return_type=DecafDouble),
    'btoi': CastFunction(parameter_type=DecafBool, return_type=DecafInt),
    'itob': CastFunction(parameter_type=DecafInt, return_type=DecafBool),
}

cast_functions: List[Function] = [
    Function(identifier=VariableName(name=cf_name),
             params=[Variable(v_type=cf.parameter_type, v_id=VariableName(name=cf.parameter_type.enum))],
             return_type=cf.return_type, stmts=StatementBlock(sts=[])) for cf_name, cf in cast_func_mapping.items()
]
