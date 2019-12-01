const Alexa = require('ask-sdk-core');
const Util = require('./util');
const Common = require('./common');

// The namespace of the custom directive to be sent by this skill
const NAMESPACE = 'Custom.Mindstorms.Gadget';

// The name of the custom directive to be sent this skill
const NAME_CONTROL = 'control';

const LaunchRequestHandler = {
    canHandle(handlerInput) {
        return Alexa.getRequestType(handlerInput.requestEnvelope) === 'LaunchRequest';
    },
    handle: async function(handlerInput) {

        let request = handlerInput.requestEnvelope;
        let { apiEndpoint, apiAccessToken } = request.context.System;
        let apiResponse = await Util.getConnectedEndpoints(apiEndpoint, apiAccessToken);
        if ((apiResponse.endpoints || []).length === 0) {
            return handlerInput.responseBuilder
            .speak(`I couldn't find an EV3 Brick connected to this Echo device. Please check to make sure your EV3 Brick is connected, and try again.`)
            .getResponse();
        }

        // Store the gadget endpointId to be used in this skill session
        let endpointId = apiResponse.endpoints[0].endpointId || [];
        Util.putSessionAttribute(handlerInput, 'endpointId', endpointId);

        return handlerInput.responseBuilder
            .speak("Welcome, you can start issuing move commands")
            .reprompt("Awaiting commands")
            .getResponse();
    }
};

// Add the speed value to the session attribute.
// This allows other intent handler to use the specified speed value
// without asking the user for input.


// Construct and send a custom directive to the connected gadget with
// data from the MoveIntent request.
const DrawIntentHandler = {
    canHandle(handlerInput) {
        return Alexa.getRequestType(handlerInput.requestEnvelope) === 'IntentRequest'
            && Alexa.getIntentName(handlerInput.requestEnvelope) === 'DrawIntent';
    },
    handle: function (handlerInput) {
        const request = handlerInput.requestEnvelope;
                
        let pattern = Alexa.getSlotValue(handlerInput.requestEnvelope, 'Pattern');
        
        const attributesManager = handlerInput.attributesManager;
        const endpointId = attributesManager.getSessionAttributes().endpointId || [];

        // Construct the directive with the payload containing the id for the pattern
        const directive = Util.build(endpointId, NAMESPACE, NAME_CONTROL,
            {
                type: 'draw',
                pattern: pattern
            });

        const speechOutput = (pattern === 0)
            ?  "Applying none"
            : `Drawing pattern ${pattern}`;

        return handlerInput.responseBuilder
            .speak(speechOutput)
            .reprompt("awaiting command")
            .addDirective(directive)
            .getResponse();
    }
};

// Construct and send a custom directive to the connected gadget with data from
// the SetCommandIntent request.

// The SkillBuilder acts as the entry point for your skill, routing all request and response
// payloads to the handlers above. Make sure any new handlers or interceptors you've
// defined are included below. The order matters - they're processed top to bottom.
exports.handler = Alexa.SkillBuilders.custom()
    .addRequestHandlers(
        LaunchRequestHandler,
        DrawIntentHandler,
        Common.HelpIntentHandler,
        Common.CancelAndStopIntentHandler,
        Common.SessionEndedRequestHandler,
        Common.IntentReflectorHandler, // make sure IntentReflectorHandler is last so it doesn't override your custom intent handlers
    )
    .addRequestInterceptors(Common.RequestInterceptor)
    .addErrorHandlers(
        Common.ErrorHandler,
    )
    .lambda();