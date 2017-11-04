"""
This sample demonstrates a simple skill built with the Amazon Alexa Skills Kit.
The Intent Schema, Custom Slots, and Sample Utterances for this skill, as well
as testing instructions are located at http://amzn.to/1LzFrj6

For additional samples, visit the Alexa Skills Kit Getting Started guide at
http://amzn.to/1LGWsLG
"""

from __future__ import print_function
from datetime import date

# --------------- Helpers that build all of the responses ----------------------

def build_speechlet_response(title, output, reprompt_text, should_end_session):
    return {
        'outputSpeech': {
            'type': 'PlainText',
            'text': output
        },
        'card': {
            'type': 'Simple',
            'title': "SessionSpeechlet - " + title,
            'content': "SessionSpeechlet - " + output
        },
        'reprompt': {
            'outputSpeech': {
                'type': 'PlainText',
                'text': reprompt_text
            }
        },
        'shouldEndSession': should_end_session
    }


def build_response(session_attributes, speechlet_response):
    return {
        'version': '1.0',
        'sessionAttributes': session_attributes,
        'response': speechlet_response
    }


# --------------- Functions that control the skill's behavior ------------------

def get_welcome_response():
    """ If we wanted to initialize the session to have some attributes we could
    add those here
    """

    session_attributes = {}
    card_title = "Welcome"
    speech_output = "Welcome to the Alexa Anti Boredom kit. " \
                    "What are your plans for tonight?"
    # If the user either does not reply to the welcome message or says something
    # that is not understood, they will be prompted again with this text.
    reprompt_text = "What are your plans for tonight?"
    should_end_session = False
    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))


def handle_session_end_request():
    card_title = "Session Ended"
    speech_output = "Thank you for fighting boredom with Alexa. " \
                    "Have fun! "
    # Setting this to true ends the session and exits the skill.
    should_end_session = True
    return build_response({}, build_speechlet_response(
        card_title, speech_output, None, should_end_session))


def create_event_attributes(evname, evprice):
    return {"event_name": evname, "event_price": evprice}

class FunEvent: 
    def __init__(self, name, date, price):
        self.name = name
        self.date = date
        self.price = price

    def __str__(self):
        return self.name + " on " + str(self.date) + ", tickets cost " + str(self.price) + " pounds"

def get_list_events(intent, session):
    session_attributes = {}
    reprompt_text = None

    events = [
        FunEvent("Rubber duck race", date.today(), 10),
        FunEvent("Arch Enemy concert", date.today(), 25)
    ]
    
    if len(events) == 0:
        speech_output = "Sorry, looks like nothing's going on."
        should_end_session = True
    else:
        speech_output = "Here's what's happening: " + ", ".join(events)
        should_end_session = False
    
    return build_response(session_attributes, build_speechlet_response(
        intent['name'], speech_output, reprompt_text, should_end_session))

def select_event(intent, session):
    # "request": {
    # "type": "IntentRequest",
    # "requestId": "EdwRequestId.ac909ff5-e943-4a4b-b288-e9e68b077eb5",
    # "intent": {
    #   "name": "SelectEventIntent",
    #   "slots": {
    #     "event": {
    #       "name": "event",
    #       "value": "rubber duck race"
    #     }
    #   }
    # },
    # "locale": "en-US",
    # "timestamp": "2017-11-04T12:26:05Z"
    # }
    card_title = intent['name']
    session_attributes = {}
    should_end_session = False

    if 'event' in intent['slots']:
        evname = intent['slots']['event']['value']
        session_attributes = create_event_attributes(evname)
        speech_output = "You want to attend " + \
                        evname + \
                        ". You can ask me to purchase tickets by saying " \
                        "Pay with FunPay"
        reprompt_text = "You can ask me to purchase tickets by saying " \
                        "Pay with FunPay"
    else:
        speech_output = "I'm not sure what event you picked. " \
                        "Please try again."
        reprompt_text = "I'm not sure what event you picked. " \
                        "You can tell me your favorite color by saying, " \
                        "Get tickets for event."
    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))

def pay_for_event_in_session(intent, session):
    session_attributes = {}
    reprompt_text = None

    if session.get('attributes', {}) and "event_name" in session.get('attributes', {}) and "event_price" in session.get('attributes', {}):
        evname = session['attributes']['event_name']
        evprice = session['attributes']['event_price']
        speech_output = "You want to purchase tickets for " + evname + \
                        ". You will be charged " + str(evprice) + "."

        # PAY HERE

        should_end_session = True
    else:
        speech_output = "I'm not sure what event you picked."
        should_end_session = False

    # Setting reprompt_text to None signifies that we do not want to reprompt
    # the user. If the user does not respond or says something that is not
    # understood, the session will end.
    return build_response(session_attributes, build_speechlet_response(
        intent['name'], speech_output, reprompt_text, should_end_session))


# --------------- Events ------------------

def on_session_started(session_started_request, session):
    """ Called when the session starts """

    print("on_session_started requestId=" + session_started_request['requestId']
          + ", sessionId=" + session['sessionId'])


def on_launch(launch_request, session):
    """ Called when the user launches the skill without specifying what they
    want
    """

    print("on_launch requestId=" + launch_request['requestId'] +
          ", sessionId=" + session['sessionId'])
    # Dispatch to your skill's launch
    return get_welcome_response()


def on_intent(intent_request, session):
    """ Called when the user specifies an intent for this skill """

    print("on_intent requestId=" + intent_request['requestId'] +
          ", sessionId=" + session['sessionId'])

    intent = intent_request['intent']
    intent_name = intent_request['intent']['name']

    # Dispatch to your skill's intent handlers
    if intent_name == "AskListEventIntent":
        return get_list_events(intent, session)
    elif intent_name == "SelectEventIntent":
        return select_event(intent, session)
    elif intent_name == "PayForEventIntent":
        return pay_for_event_in_session(intent, session)
    elif intent_name == "AMAZON.HelpIntent":
        return get_welcome_response()
    elif intent_name == "AMAZON.CancelIntent" or intent_name == "AMAZON.StopIntent":
        return handle_session_end_request()
    else:
        raise ValueError("Invalid intent")


def on_session_ended(session_ended_request, session):
    """ Called when the user ends the session.

    Is not called when the skill returns should_end_session=true
    """
    print("on_session_ended requestId=" + session_ended_request['requestId'] +
          ", sessionId=" + session['sessionId'])
    # add cleanup logic here


# --------------- Main handler ------------------

def lambda_handler(event, context):
    """ Route the incoming request based on type (LaunchRequest, IntentRequest,
    etc.) The JSON body of the request is provided in the event parameter.
    """
    print("event.session.application.applicationId=" +
          event['session']['application']['applicationId'])

    """
    Uncomment this if statement and populate with your skill's application ID to
    prevent someone else from configuring a skill that sends requests to this
    function.
    """
    # if (event['session']['application']['applicationId'] !=
    #         "amzn1.echo-sdk-ams.app.[unique-value-here]"):
    #     raise ValueError("Invalid Application ID")

    if event['session']['new']:
        on_session_started({'requestId': event['request']['requestId']},
                           event['session'])

    if event['request']['type'] == "LaunchRequest":
        return on_launch(event['request'], event['session'])
    elif event['request']['type'] == "IntentRequest":
        return on_intent(event['request'], event['session'])
    elif event['request']['type'] == "SessionEndedRequest":
        return on_session_ended(event['request'], event['session'])
