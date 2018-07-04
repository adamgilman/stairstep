from stairstep import State

class FieldValidationTests(object):
    def test_required_fields(self):
        fields = self.state_fields['required_fields']
        for f in fields:
            test_state = self.original_state
            #set value to field and make sure exception is not raised
            setattr(test_state, f, None)
            with self.assertRaises(AttributeError):
                test_state.export()

    def test_notallowed_fields(self):
        fields = self.state_fields['not_allowed']
        for f in fields:
            test_state = self.original_state
            #set value to field and make sure exception is raised
            setattr(test_state, f, "SomeValue")
            try:
                test_state.export()
            except AttributeError:
                print(vars(test_state))
                self.fail("AttributeError raised for a field that is allowed")

    def test_required_fields(self):
        fields = self.state_fields['required_fields']
        for f in fields:
            test_state = self.original_state
            #remove required field and make sure exception is raised
            setattr(test_state, f, None)
            with self.assertRaises(AttributeError):
                test_state.export() 

    def test_have_next_or_end(self):
        #if true must have next or catch and it is true
        '''
        if true
            if field has next, 
            if field has end
                add end and make sure it errors
                remove it make sure it errors
                set it to false and make sure it errors
        if false
            cannot have either next or end
        '''
        if self.next_or_end:
            if hasattr(self.original_state, 'next'):
                test_state = self.original_state
                test_state.end = True
                with self.assertRaises(AttributeError):
                    test_state.export() 

                test_state = self.original_state
                test_state.next = None
                with self.assertRaises(AttributeError):
                    test_state.export() 
                
                test_state = self.original_state
                test_state.next = False
                with self.assertRaises(AttributeError):
                    test_state.export() 
            
            if hasattr(self.original_state, 'end'):
                test_state = self.original_state
                test_state.next = "nextResource"
                with self.assertRaises(AttributeError):
                    test_state.export() 

                test_state = self.original_state
                test_state.end = None
                test_state.next = None
                with self.assertRaises(AttributeError):
                    print(vars(test_state))
                    test_state.export() 
                
                test_state = self.original_state
                test_state.end = False
                with self.assertRaises(AttributeError):
                    test_state.export()
        
        if not self.next_or_end: 
            test_state = self.original_state
            #cannot have either next or end
            if hasattr(self.original_state, 'next'):
                with self.assertRaises(AttributeError):
                    test_state.export()

            if hasattr(self.original_state, 'end'):
                with self.assertRaises(AttributeError):
                    test_state.export()
            