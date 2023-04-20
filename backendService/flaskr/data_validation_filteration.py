"""
MODULE: data_validation_filteration
Provide services and utilities for connecting with kafka
"""
import json

def data_validate_venue(d):
    """
    FUNCTION: data_validate_venue(), Validates and filters venue 
    @returns: Validated and Filtered Venue or None
    @arguments Venue data 
    """
    # print('from data_validate_venue: ', d)
    venue_name = d['venue_name'] if 'venue_name' in d else None
    venue_id = d['venue_id'] if 'venue_id' in d else None
    lon = d['lon'] if 'lon' in d else None
    lat = d['lat'] if 'lat' in d else None

    if lon is not None and lat is not None:
        return {'venue_name': venue_name, 'venue_id': venue_id, 'lon': lon, 'lat':lat}
    return None

def data_validate_response(d):
    """
    FUNCTION: data_validate_response(), Covert string Rsvp to Bool
    @returns: Bool ( True/False )
    @arguments Rsvp Status String
    """
    return True if d == 'yes' else False

def data_validate_and_filter_rsvp(d):
    """
    FUNCTION: data_validate_and_filter_rsvp(), Validates Complete Response (Meetup Rsvp: http://meetup.github.io/stream/rsvpTicker/)
    Loads data in JSON, and then make calls to sub - functions
    @returns Filtered and Validated Data or None - Scope reduced to three 
    1. Venue Details
    2. Response (Rsvp)
    3. Rsvp_Id
    @arguments a record from Kafka Event Pipeline (Consumer)
    """
    # print('From data_validate_and_filter_rsvp: ', d)
    venue = data_validate_venue(d['venue']) if 'venue' in d else None
    response = data_validate_response(d['response']) if 'response' in d else None
    rsvp_id = d['rsvp_id'] if 'rsvp_id' in d else None

    if venue is not None and response is not None:
        return {'venue': venue, 'response': response, 'rsvp_id': rsvp_id}
    return None
    
def validate_data_to_proceed(d): 
    """
    FUNCTION: validate_data_to_proceed(), Validates Complete Response (Meetup Rsvp: http://meetup.github.io/stream/rsvpTicker/)
    Loads data in JSON, and then make calls to sub - functions
    @returns Filtered and Validated Data or None
    @arguments a record from Kafka Event Pipeline (Consumer)
    """
    # print('From validate_data_to_proceed: ', d)
    if 'rsvp' in d and d['rsvp'] is not None:
        return data_validate_and_filter_rsvp(json.loads(d['rsvp']))
    return None

def _check_rsvp_status_(data):
    """
    FUNCTION: _check_rsvp_status_(), Filter data where Rsvp is True
    @returns True/False, 
    @arguments Rsvp Status
    """
    return data is not None and data['response'] == True

def filter_data_by_rsvp(d):
    """
    FUNCTION: filter_data_by_rsvp(), Filter data where Rsvp is True
    @returns True/False, If the given record (dict)
    @arguments a record (dict) for the Rsvp event from outgoing pipline
    """
    if d is not None and 'response' in d:
        return _check_rsvp_status_(d)
    return False