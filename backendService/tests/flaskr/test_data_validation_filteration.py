from flaskr.data_validation_filteration import validate_data_to_proceed, filter_data_by_rsvp, _check_rsvp_status_

class TestCheckRsvpStatus:
    
    def test_what_if_status_true(self):
        data = {'response': True}
        assert _check_rsvp_status_(data) == True

    def test_what_if_status_false(self):
        data = {'response': False}
        assert _check_rsvp_status_(data) == False

class TestFilterDataByRsvp:
    
    d_is_none = None
    d_is_empty_dict = {}
    d_is_response_true = {'response': True}
    d_is_response_false = {'response': False}
    
    def test_what_if_d_is_none(self):
        d = self.d_is_none
        assert filter_data_by_rsvp(d) == False

    def test_what_if_d_is_empty_dict(self):
        d = self.d_is_empty_dict
        assert filter_data_by_rsvp(d) == False

    def test_what_if_d_is_response_true(self):
        d = self.d_is_response_true
        assert filter_data_by_rsvp(d) == True

    def test_what_if_d_is_response_false(self):
        d = self.d_is_response_false
        assert filter_data_by_rsvp(d) == False

class TestValidateDataToProceed:
    
    d_is_none = None
    d_is_empty_dict = {}
    d_is_response_true = {'response': True}
    d_is_response_false = {'response': False}
    