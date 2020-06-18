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
                            'base_validations',
                            'branches',
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
            'name'          : "Name",
            "comment"       : "Comment",
            "stype"         : "Type",
            "resource"      : "Resource",
            "next"          : "Next",
            "inputpath"     : "InputPath",
            "resultpath"    : "ResultPath",
            "outputpath"    : "OutputPath",
            "retry"         : "Retry",
            "catch"         : "Catch",
            "end"           : "End",
            "seconds"       : "Seconds",
            "timestamp"     : "Timestamp",
            "secondspath"   : "SecondsPath",
            "timestamppath" : "TimestampPath",
            "parameters"    : "Parameters"
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
        end = None,
        parameters = None,
        inputpath = None,
        outputpath = None,
        resultpath = None
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
        self.parameters = parameters
        self.inputpath = inputpath
        self.outputpath = outputpath
        self.resultpath = resultpath

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

    def validate_state_flow(self):
        state_names = [
            state_name for state_name in self.states.keys()
            if state_name != self.startAt
        ]
        state_targets = [
            state.next for state in self.states.values()
            if getattr(state, 'next', None) is not None
        ]
        for state_name in state_names:
            if state_name not in state_targets:
                raise ValueError(
                    'State unreachable: ' + state_name
                    + "(you can ignore this warning if there is a StateChoice"
                    + " pointing to this state)."
                )
        for target in state_targets:
            if target not in state_names:
                raise ValueError('Target state not found: ' + target)

    def export(self):
        # The error raised is changed to a warning. This is a
        # workaround due to lack of implementation around StateChoice.
        try:
            self.validate_state_flow()
        except Exception as e:
            print(f"WARNING - validation error:" + str(e))

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
