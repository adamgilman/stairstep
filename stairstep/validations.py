def validation_none_terminal_must_have_next(self):
    if self.next is None:
        raise AttributeError("All non-terminal states MUST have a “Next” field")

def validation_states_must_have_next_or_end(self):
    if (self.next is None) and (self.end is None):
        raise AttributeError("State must have either an End or Next field")

def validation_states_cant_have_both_end_and_next(self):
    if (self.next is not None) and (self.end is not None):
        raise AttributeError("State cannot have both an End and Next field")

def validation_name_cannot_be_longer_than_128(self):
    if len(self.name) > 128:
        raise AttributeError("State name cannot be longer than 128 charecters")

def validation_all_states_must_have_type(self):
    if self.stype is None:
        raise AttributeError("State must have Type")
