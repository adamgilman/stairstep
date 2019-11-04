from .base import StateBase
from .validations import *

class StatePass(StateBase):
    def __init__(self, **kwargs):
        kwargs['stype'] = "Pass"
        super().__init__(**kwargs)

        self.validations += [
            validation_none_terminal_must_have_next,
            validation_states_must_have_next_or_end
        ]

class StateTask(StateBase):
    def __init__(self, **kwargs):
        kwargs['stype'] = "Task"
        super().__init__(**kwargs)

        self.validations += [
            validation_states_must_have_next_or_end
        ]

class StateWait(StateBase):
    def __init__(self, **kwargs):
        kwargs['stype'] = "Wait"
        super().__init__(**kwargs)

        self.validations += [
            validation_must_contain_only_one_time_field,
        ]

class StateSucceed(StateBase):
    def __init__(self, **kwargs):
        kwargs['stype'] = "Succeed"
        super().__init__(**kwargs)

        self.validations += [
            validation_end_cannot_be_true,
            validation_cannot_have_next
        ]


class StateFail(StateBase):
    def __init__(self, **kwargs):
        kwargs['stype'] = "Fail"
        super().__init__(**kwargs)

        self.validations += [
            validation_end_cannot_be_true,
            validation_cannot_have_next,
            validation_cannot_have_io_path_fields
        ]


class StateParallel(StateBase):
    def __init__(self, **kwargs):
        kwargs['stype'] = "Parallel"
        accepted_kwargs = {
            k: v for k, v in kwargs.items()
            if k in (*StateBase.prop_map.keys(), 'snext')
        }
        super().__init__(**accepted_kwargs)
        self.branches = kwargs['branches']
        self.validations += [
            validation_states_must_have_next_or_end,
            validation_branch_must_be_state_machines,
        ]

    def export(self):
        ret = super().export()
        exported_branches = [
            ss.export()
            for ss in self.branches
        ]
        ret['Branches'] = exported_branches
        return ret
