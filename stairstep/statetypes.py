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

class StateChoice(StateBase):
    def __init__(self, **kwargs):
        kwargs['stype'] = "Choice"
        super().__init__(**kwargs)

        self.validations += [
            validation_states_must_have_next_or_end,
            validation_end_cannot_be_true
        ]
        
class StateSucceed(StateBase):
    def __init__(self, **kwargs):
        kwargs['stype'] = "Succeed"
        super().__init__(**kwargs)

        self.validations += [
            validation_end_cannot_be_true
        ]
        

class StateFail(StateBase):
    def __init__(self, **kwargs):
        kwargs['stype'] = "Fail"
        super().__init__(**kwargs)

        self.validations += [
            validation_end_cannot_be_true,
            validation_cannot_have_io_path_fields
        ]