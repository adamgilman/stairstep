import json
from .base import StateBase
from .validations import *

class StateChoice(StateBase):
    def __init__(self, **kwargs):
        kwargs['stype'] = "Choice"
        
        self.choices = kwargs.pop("choices", None)
        self.default = kwargs.pop("default", None)

        super().__init__(**kwargs)
        self.validations += [
            validation_end_cannot_be_true
        ]
    
    def export(self):
        #generate choices export
        return {
            'Type' : "Choice",
            'Default' : self.default,
            'Choices' : [c.export() for c in self.choices]
        }

class ChoiceRule:
    def __init__(self, operator=None, snext=None, conditions=None):
        self.operator = operator
        self.snext = snext
        self.conditions = conditions

    def export(self):
        if type(self.conditions) is not list:
            return {
                'Next' : self.snext,
                self.operator : self.conditions.export()
            }
        else:
            multiple_conditions = []
            for c in self.conditions:
                multiple_conditions.append( c.export() )
            return {
                'Next' : self.snext,
                self.operator : multiple_conditions
            }

    def json(self):
        return json.dumps( self.export() )

class ChoiceExpression:
    def __init__(self, operator=None, variable=None, value=None):
        self.operator = operator
        self.variable = variable
        self.value = value
    
    def export(self):
        return {
                "Variable" : self.variable,
                self.operator : self.value
        }

    def json(self):
        return json.dumps( self.export() )