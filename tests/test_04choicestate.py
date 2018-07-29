import unittest, json
from stairstep import StairStep
from stairstep import StateChoice, ChoiceRule, ChoiceExpression

#each element of a choice is a choice rule
#containing a comparasion and a next

class TestChoiceStateRule(unittest.TestCase):
    def setUp(self):
        self.maxDiff = None
        self.ss = StairStep(
            comment = "Example Choice State",
            startAt = "ChoiceStateX"
        )
        typeNotPrivate = ChoiceRule(operator="Not", snext="Public", conditions=
                            ChoiceExpression(operator="StringEquals", variable="$.type", value="Private")
                         )

        valueInTwenties = ChoiceRule(operator="And", snext="ValueInTwenties", conditions=[
                            ChoiceExpression(operator="NumericGreaterThanEquals", variable="$.value", value=20),
                            ChoiceExpression(operator="NumericLessThan", variable="$.value", value=30)]
                        )
    
        self.state = StateChoice(
            name    = "ChoiceStateX",
            choices = [typeNotPrivate, valueInTwenties],
            default = "DefaultState"
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
                        }

                }
            }
        '''     
        output = json.loads(output)
        result = json.loads( self.ss.json() )
        self.assertDictEqual(output, result)

class TestChoiceExpressionSubset(unittest.TestCase):
    def setUp(self):
        self.choice_expression = ChoiceExpression(operator="StringEquals", variable="$.type", value="Private")

    def test_choice_expression_output(self):
        output = '''
            {
                "Variable": "$.type",
                "StringEquals": "Private"
            }
        '''
        output = json.loads(output)
        result = json.loads( self.choice_expression.json() )
        self.assertDictEqual(output, result)

class TestChoiceRuleSubset(unittest.TestCase):
    def setUp(self):
        pass

    def test_choice_rule_output_single(self):
        choice_rule = ChoiceRule(operator="Not", snext="Public", conditions=
                               ChoiceExpression(operator="StringEquals", variable="$.type", value="Private")
                           )
        output = '''
        {
            "Not": {
            "Variable": "$.type",
            "StringEquals": "Private"
            },
            "Next": "Public"
        }'''
        output = json.loads(output)
        result = json.loads( choice_rule.json() )
        self.assertDictEqual(output, result)

    def test_choice_rule_output_multiple_conditions(self):
        choice_rule = ChoiceRule(operator="And", snext="ValueInTwenties", conditions=[
                            ChoiceExpression(operator="NumericGreaterThanEquals", variable="$.value", value=20),
                            ChoiceExpression(operator="NumericLessThan", variable="$.value", value=30)
                            ]
                      )

        output = '''
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
        }'''
        output = json.loads(output)
        result = json.loads( choice_rule.json() )
        self.assertDictEqual(output, result)