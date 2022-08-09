from typing import TYPE_CHECKING, List, Dict, Union

from code_generation.exceptions import DecafNameError
from code_generation.scope import Symbol, ScopeLoopInterface
from exceptions import CompilerPanic
from utils import Stack
from todos import Todo

from transformers.types import DecafDouble, DecafBool, DecafString, DecafInt

if TYPE_CHECKING:
    from transformers.sdt import Function, Variable
    from transformers.sdt.utils import VariableName
    from transformers.types import DecafType
    from transformers.sdt.stmts import ForStatement, WhileStatement


class Scope:

    def __init__(self, name: str = None, parent_scope: "Scope" = None):
        self.stack_size = 0
        self.name = name
        self.parent_scope = parent_scope
        self.functions_env: Dict[str, "Function"] = {}
        self.symbols_env: Dict[str, "Symbol"] = {}
        self.loop_stack = Stack()

    def loop(self, loop: Union["ForStatement", "WhileStatement"]):
        return ScopeLoopInterface(self, loop)

    def extend_function(self, function: "Function"):
        self.functions_env[function.identifier.name] = function

    def extend_symbol(self, variable: "Variable"):
        self.stack_size += variable.type.size
        self.symbols_env[variable.id.name] = Symbol(variable, self.stack_size)

    def apply_function(self, function_name: "VariableName") -> "Function":
        try:
            scope_ans: "Function" = self.functions_env.get(function_name.name)
            if scope_ans is None:
                scope_ans = self.parent_scope.apply_function(function_name)
            return scope_ans
        except AttributeError as e:
            if "'NoneType' object has no attribute 'get'" in str(e):
                raise DecafNameError(var_name=function_name)
            raise CompilerPanic(caused_by=e)

    def apply_symbol(self, variable_name: "VariableName") -> "Variable":
        try:
            scope_ans: "Symbol" = self.symbols_env.get(variable_name.name)
            if scope_ans is None:
                return self.parent_scope.apply_symbol(variable_name)
            return scope_ans.variable
        except AttributeError as e:
            if "'NoneType' object has no attribute 'get'" in str(e):
                raise DecafNameError(var_name=variable_name)
            raise CompilerPanic(caused_by=e)

    def apply_symbol_stack_pointer_offset(self, variable_name: "VariableName", base_offset: int = 0) -> int:
        try:
            scope_ans: "Symbol" = self.symbols_env.get(variable_name.name)
            if scope_ans is None:
                return self.parent_scope.apply_symbol_stack_pointer_offset(
                    variable_name, base_offset=self.stack_size + base_offset
                )
            return self.stack_size - scope_ans.relative_stack_address + base_offset
        except AttributeError as e:
            if "'NoneType' object has no attribute 'get'" in str(e):
                raise DecafNameError(var_name=variable_name)
            raise CompilerPanic(caused_by=e)

    def path_to_root(self) -> List["Scope"]:
        path = [self]
        if self.parent_scope is None:
            return path
        return [*self.parent_scope.path_to_root(), *path]

    @property
    def scope_prefix(self):
        return '_'.join([scope.name for scope in self.path_to_root() if scope.name is not None])

    def push_to_stack(self, temp_t: "DecafType") -> List[str]:
        self.stack_size += temp_t.size
        code = [
            f"subu $sp, $sp, {temp_t.size}	# Decrement sp to make space for temp."]
        if temp_t in [DecafInt, DecafString, DecafBool]:
            code += [f"sw $t0, 0($sp) # put temp to stack"]
        elif temp_t == DecafDouble:
            code += ["s.d $f0, 0($sp) # put temp to stack"]
        else:
            code += [str(Todo())]
        return code

    def pop_from_stack(self, temp_t: "DecafType") -> List:
        self.stack_size -= temp_t.size
        code = []
        if temp_t in [DecafInt, DecafString, DecafBool]:
            code += [f"lw $t0, 0($sp) # put temp from stack to $t0"]
        elif temp_t == DecafDouble:
            code += ["l.d $f0, 0($sp) # put temp from stack to $f0"]
        else:
            code += [str(Todo())]
        code += [f"addi $sp, $sp, {temp_t.size}	# move stack up to pop the temp"]
        return code


GLOBAL_SCOPE = Scope(name='global')

if __name__ == '__main__':
    a = Scope('a', GLOBAL_SCOPE)
