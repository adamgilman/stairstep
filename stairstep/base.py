import simplejson as json

class State(object):
    prop_map = {
            'name'      : "Name",
            "comment"   : "Comment",
            "stype"     : "Type",
            "resource"  : "Resource",
            "next"      : "Next",
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