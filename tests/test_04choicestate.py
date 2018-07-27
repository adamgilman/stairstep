import unittest
from stairstep import StairStep
from stairstep import StateChoice, ChoiceRule, ChoiceExpression

#each element of a choice is a choice rule
#containing a comparasion and a next

class TestChoiceStateRule(unittest.TestCase):
    def setUp(self):
        self.ss = StairStep(
            comment = "Example Choice State",
            startAt = "ChoiceStateX",
        )
        self.state = StateChoice(
            name            = "HelloWorld",
            choices = StateChoice(name="ChoiceStateX", choices=
                [
                    ChoiceRule(operator="Not", next="Public", conditions=[
                        ChoiceExpression(operator="StringEquals", variable="$.type", value="Private"),
                    ]),

                    ChoiceRule(operator="And", next="ValueInTwenties", conditions=[
                        ChoiceExpression(operator="NumericGreaterThanEquals", variable="$.value", value="20"),
                        ChoiceExpression(operator="NumericLessThan", variable="$.value", value="30")
                    ]),

                    ChoiceRule(operator="Default", next="DefaultState")
                ]
            )    
        )
        self.ss.addState(self.state)
    
    def test_choice_state(self):
        output = '''
            {
                "Comment": "Example Choice State",
                "StartAt": "ChoiceStateX",
                "States": {
                    "ChoiceStateX": {
                        "Type" : "Choice",
                        "Choices": [
                            {
                                "Not": {
                                "Variable": "$.type",
                                "StringEquals": "Private"
                                },
                                "Next": "Public"
                            },
                            {
                            "And": [
                                {
                                "Variable": "$.value",
                                "NumericGreaterThanEquals": 20
                                },
                                {
                                "Variable": "$.value",
                                "NumericLessThan": 30
                                }
                            ],
                            "Next": "ValueInTwenties"
                            }
                        ],
                        "Default": "DefaultState"
                        },

                }
            }
        '''     
        output = json.loads(output)
        result = json.loads( self.ss.json() )
        self.assertDictEqual(output, result)
