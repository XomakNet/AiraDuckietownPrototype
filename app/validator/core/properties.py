from validator.core.specification import LogSpecification
from validator.core.expression_builder import ExpressionBuilder
from validator.core.base_expression import *
from validator.core.program import *
from typing import List


class BasePropertyCompiler:
    def __init__(self, log: LogSpecification):
        self._log_specification = log

    def compile(self) -> ExpressionBuilder:
        raise NotImplementedError()


class StrongPropertyCompiler(BasePropertyCompiler):
    def compile(self) -> ExpressionBuilder:
        return self._process_states(self._log_specification.states)

    def _process_states(self, states: List) -> ExpressionBuilder:
        state = states[0]

        builder = None

        for i in range(0, len(state)):
            var_id = Identifier("{}{}".format(VAR_PREFIX, str(i + 1)))
            sub_builder = ExpressionBuilder(var_id)
            sub_builder.append_eq(Integer(state[i]))

            if builder is not None:
                builder.append_and(sub_builder.expression)
            else:
                builder = sub_builder

        if len(states) > 1:
            next_builder = self._process_states(states[1:])
            next_builder.wrap_tl_next()
            next_builder.wrap_tl_exist()

            builder.append_and(next_builder.expression)

        return builder


class WeakPropertyCompiler(BasePropertyCompiler):
    def compile(self) -> ExpressionBuilder:
        return self._process_states(self._log_specification.states)

    def _process_states(self, states: List) -> ExpressionBuilder:
        state = states[0]

        builder = None

        for i in range(0, len(state)):
            var_id = Identifier("{}{}".format(VAR_PREFIX, str(i + 1)))
            sub_builder = ExpressionBuilder(var_id)
            sub_builder.append_eq(Integer(state[i]))

            if builder is not None:
                builder.append_and(sub_builder.expression)
            else:
                builder = sub_builder

        if len(states) > 1:
            next_builder = self._process_states(states[1:])
            next_builder.wrap_tl_eventually()
            next_builder.wrap_tl_exist()

            builder.append_and(next_builder.expression)

        return builder
