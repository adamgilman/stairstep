def validation_none_terminal_must_have_next(self):
    if (self.next is None) and (self.end is not True):
        raise AttributeError("All non-terminal states MUST have a Next field")

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

def validation_end_cannot_be_true(self):
    if self.end is True:
        raise AttributeError("End cannot be True for this State Type")

def validation_cannot_have_io_path_fields(self):
    if self.inputpath is not None:
        raise AttributeError("Fail State cannot have InputPath, OutputPath")
    
    if self.output is not None:
        raise AttributeError("Fail State cannot have InputPath, OutputPath")

def validation_must_contain_only_one_time_field(self):    
    fields = [self.seconds, self.secondspath, self.timestamp, self.timestamppath]

    fields_count = 0    
    for f in fields:
        if f is not None:
            fields_count = fields_count + 1
    
    if fields_count != 1:
        raise AttributeError("Wait state must contain exactly one of Seconds, SecondsPath, Timestamp, or TimestampPath")