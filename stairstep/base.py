import simplejson as json
from .validations import *

class StateBase(object):
    prop_map = {
            'name'      : "Name",
            "comment"   : "Comment",
            "stype"     : "Type",
            "resource"  : "Resource",
            "next"      : "Next",
            "inputpath" : "InputPath",
            "outputpath": "OutputPath",
            "retry"     : "Retry",
            "catch"     : "Catch",
            "end"       : "End"
        }
    def __init__(self,
        name = None,
        comment = None,
        stype = None,
        resource = None,
        snext = None,
        end = None
    ):
        self.name = name
        self.comment = comment
        self.stype = stype
        self.resource = resource
        self.next = snext
        self.end = end

        self.base_validations = [
            validation_states_cant_have_both_end_and_next,
            validation_name_cannot_be_longer_than_128
        ]
        self.validations = []

    def validate(self):
        all_validations = self.base_validations + self.validations
        for v in all_validations:
            v(self)
        
    def export(self):
        self.validate()

        if self.stype is None:
            raise AttributeError("All states MUST have a “Type” field.")

        if (self.next is True):
            raise AttributeError("True is an invalid value for Next")
                
        if self.end is True:
            if self.stype in ['Choice', 'Succeed', 'Fail']:
                raise AttributeError("Choice, Succeed, Fail states may NOT have 'End' field")

        ret = {}
        self_vars = vars(self)
        exclude_fields = [
                            'prop_map',
                            'name',
                            'validations',
                            'base_validations'
                         ]
        for key in exclude_fields:
            self_vars.pop(key, None)
        
        for prop_key in self_vars.keys():
            if self_vars[prop_key] is not None:
                key_map = self.prop_map[prop_key]
                ret[key_map] = self_vars[prop_key]
        return ret

#TODO: make validation methods an abstract base class onto subclasses
# parent StateBase calls validation method of lower class
# howto? call mixin validations?
# mixins have an ABC as well they have to implement?

#o, end=T, N=N
#


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
            validation_states_must_have_next_or_end
        ]
        


class StateSucceed(StateBase):
    def __init__(self, **kwargs):
        kwargs['stype'] = "Succeed"
        super().__init__(**kwargs)

        self.validations += []
        

class StateFail(StateBase):
    def __init__(self, **kwargs):
        kwargs['stype'] = "Fail"
        super().__init__(**kwargs)

        self.validations += []
        

class StairStep(object):
    def __init__(self, 
        comment = None,
        startAt = None
    ):
        self.states = {}
        self.comment = comment
        self.startAt = startAt

    def addState(self, state):
        self.states[state.name] = state

    def export(self):
        states = {}
        for k in self.states.keys():
            states[k] = self.states[k].export()
        if self.comment is not None:
            ret = {
                "Comment" : self.comment,
                "StartAt" : self.startAt,
                "States" : states
            }
        else:
            ret = {
                "StartAt" : self.startAt,
                "States" : states
            }
        return ret

    def json(self):
        return json.dumps( self.export() )