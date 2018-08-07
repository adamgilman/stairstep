import json, copy
from .validations import *

class SSBase(object):
    prop_map = {}
    base_validations = []

    def validate(self):
        all_validations = self.base_validations + self.validations
        for v in all_validations:
            v(self)
    
    def export(self):
        self.validate()
      
        ret = {}
        self_vars = copy.deepcopy( vars(self) )
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

class StateBase(SSBase):
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
            "end"       : "End",
            "seconds"   : "Seconds",
            "timestamp" : "Timestamp",
            "secondspath" : "SecondsPath",
            "timestamppath" : "TimestampPath"
        }
    base_validations = [
            validation_states_cant_have_both_end_and_next,
            validation_name_cannot_be_longer_than_128,
            validation_all_states_must_have_type
        ]

    def __init__(self,
        name = None,
        comment = None,
        stype = None,
        resource = None,
        snext = None,
        seconds = None,
        timestamp = None,
        timestamppath = None,
        secondspath = None,
        end = None
    ):
        #TODO - Refactor to unpack via **kwargs and map against prop_map
        self.name = name
        self.comment = comment
        self.stype = stype
        self.resource = resource
        self.next = snext
        self.seconds = seconds        
        self.end = end
        self.timestamppath = timestamppath
        self.secondspath = secondspath

        if timestamp is not None:
            self.timestamp = timestamp.isoformat() #compliant ISO-8601 export 
        else:
            self.timestamp = None

        self.validations = []
    

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