import simplejson as json

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


    def export(self):
        if (self.next is True):
            raise AttributeError("True is an invalid value for Next")
        
        if (self.stype not in ['Choice', 'Success', 'Fail']):
            if (self.next is not None) and (self.end is not None):
                raise AttributeError("State must have either an End or Next field")

        if (self.next is None) and (self.end is None):
            raise AttributeError("State must have either an End or Next field")

        if self.stype not in ['Succeed', 'Fail']:
            if self.next is None:
                raise AttributeError("All non-terminal states MUST have a “Next” field")
        
        if self.end is True:
            if self.stype in ['Choice', 'Succeed', 'Fail']:
                raise AttributeError("Choice, Succeed, Fail states may NOT have 'End' field")

        if self.stype is None:
            raise AttributeError("All states MUST have a “Type” field.")

        ret = {}
        self_vars = vars(self)
        self_vars.pop("prop_map", None)
        self_vars.pop("name", None)
        for prop_key in self_vars.keys():
            if self_vars[prop_key] is not None:
                key_map = self.prop_map[prop_key]
                ret[key_map] = self_vars[prop_key]
        return ret
                
class StatePass(StateBase):
    pass

class StateTask(StateBase):
    def __init__(self, **kwargs):
        kwargs['stype'] = "Task"
        super().__init__(**kwargs)

class StateSucceed(StateBase):
    def __init__(self, **kwargs):
        kwargs['stype'] = "Succeed"
        super().__init__(**kwargs)

class StateFail(StateBase):
    def __init__(self, **kwargs):
        kwargs['stype'] = "Fail"
        super().__init__(**kwargs)


class StateChoice(StateBase):
    def __init__(self, **kwargs):
        kwargs['stype'] = "Choice"
        super().__init__(**kwargs)


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