import simplejson as json

class State(object):
    def __init__(self,
        name = None,
        stype = None,
        resource = None,
        end = None
    ):
        self.name = name
        self.stype = stype
        self.resource = resource
        self.end = end

    def export(self): 
        return {
                    'Type' : self.stype,
                    'Resource' : self.resource,
                    "End" : self.end
                }
                

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
        ret = {
            "Comment" : self.comment,
            "StartAt" : self.startAt,
            "States" : states
        }
        return ret

    def json(self):
        return json.dumps( self.export() )