from transformers.sdt import Function, Variable
from transformers.sdt.stmts import StatementBlock
from transformers.sdt.utils import VariableName
from transformers.types import DecafInt, DecafArray

allocation_function = Function(identifier=VariableName(name="alloc"),
                               params=[Variable(v_type=DecafInt, v_id=VariableName(name="allocation_num"))],
                               return_type=None, stmts=StatementBlock(sts=[]))
