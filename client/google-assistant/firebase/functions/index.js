'use strict';

const config = require('./config/config')
const functions = require('firebase-functions'); // Cloud Functions for Firebase library
const DialogflowApp = require('actions-on-google').DialogflowApp; // Google Assistant helper library
const requestAPI = require('request-promise')
var admin = require("firebase-admin");
const baseURL = 'https://catalog.fullerton.edu'

exports.dialogflowFirebaseFulfillment = functions.https.onRequest((request, response) => {
  console.log('Dialogflow Request headers: ' + JSON.stringify(request.headers));
  console.log('Dialogflow Request body: ' + JSON.stringify(request.body));
  if (request.body.result) {
    processV1Request(request, response);
  } else if (request.body.queryResult) {
    processV2Request(request, response);
  } else {
    console.log('Invalid Request');
    return response.status(400).end('Invalid Webhook Request (expecting v1 or v2 webhook request)');
  }
});

/*
* Function to handle v1 webhook requests from Dialogflow
*/
function processV1Request (request, response) {
  let action = request.body.result.action; // https://dialogflow.com/docs/actions-and-parameters
  let parameters = request.body.result.parameters; // https://dialogflow.com/docs/actions-and-parameters
  let inputContexts = request.body.result.contexts; // https://dialogflow.com/docs/contexts
  let requestSource = (request.body.originalRequest) ? request.body.originalRequest.source : undefined;
  const googleAssistantRequest = 'google'; // Constant to identify Google Assistant requests
  const app = new DialogflowApp({request: request, response: response});


  if ( app.data.collegeData === undefined ){
    app.data.collegeData = [];
  }

  if ( app.data.collegeCount === undefined ){
    app.data.collegeCount = 0;
  }

  if ( app.data.courseData === undefined ){
    app.data.courseData = [];
  }

  // Create handlers for Dialogflow actions as well as a 'default' handler
  const actionHandlers = {
    // The default welcome intent has been matched, welcome the user (https://dialogflow.com/docs/events#default_welcome_intent)
    'input.welcome': () => {
      // Use the Actions on Google lib to respond to Google requests; for other requests use JSON
      if (requestSource === googleAssistantRequest) {
        sendGoogleResponse('Hello'); // Send simple response to user
      }
    },

    'input.hascollege':() =>{
      // check if a csuf has a given college or not
      let college = app.getArgument('college_name')
      console.log('input.hascollege => College Name = '+college)
      isCollegeExist(college, config.collegeEndpoint);
    },

    'hascollege.hascollege-yes':() =>{
      console.log('Inside hascollege.hascollege-yes')
      let college = app.getContextArgument('hascollege-followup', 'college_name').value;//.getContextArgument().getArgument('hascollege-followup.college_name')
      console.log('hascollege.hascollege-yes => College Name = '+college)
      collegeDescription(college, config.collegeEndpoint);
    },

    'input.prerequisite':() =>{
      let course = app.getArgument('course_prereq')
      console.log('input.prerequisite => Course Name = '+course)
      showPrerequisite(course, config.courseEndpoint);
    },

    'input.showcolleges':() =>{
      // show all colleges
      showColleges(config.collegeEndpoint);
    },

    // The default fallback intent has been matched, try to recover (https://dialogflow.com/docs/intents#fallback_intents)
    'input.unknown': () => {
      // Use the Actions on Google lib to respond to Google requests; for other requests use JSON
      if (requestSource === googleAssistantRequest) {
        sendGoogleResponse('I\'m having trouble, can you try that again?'); // Send simple response to user
      } else {
        sendResponse('I\'m having trouble, can you try that again?'); // Send simple response to user
      }
    },
    // Default handler for unknown or undefined actions
    'default': () => {
      // Use the Actions on Google lib to respond to Google requests; for other requests use JSON
      if (requestSource === googleAssistantRequest) {
        let responseToUser = {
          googleRichResponse: googleRichResponse, // Optional, uncomment to enable
          googleOutputContexts: ['weather', 2, { ['city']: 'rome' }], // Optional, uncomment to enable
          speech: 'This message is from Dialogflow\'s Cloud Functions for Firebase editor!', // spoken response
          text: 'This is from Dialogflow\'s Cloud Functions for Firebase editor! :-)' // displayed response
        };
        sendGoogleResponse(responseToUser);
      } else {
        let responseToUser = {
          data: richResponsesV1, // Optional, uncomment to enable
          outputContexts: [{'name': 'weather', 'lifespan': 2, 'parameters': {'city': 'Rome'}}], // Optional, uncomment to enable
          speech: 'This message is from Dialogflow\'s Cloud Functions for Firebase editor!', // spoken response
          text: 'This is from Dialogflow\'s Cloud Functions for Firebase editor! :-)' // displayed response
        };
        sendResponse(responseToUser);
      }
    }
  };

  // If undefined or unknown action use the default handler
  if (!actionHandlers[action]) {
    action = 'default';
  }

  // Run the proper handler function to handle the request from Dialogflow
  actionHandlers[action]();

  function isCollegeExist(collegeName, endpoint){
    if (app.data.collegeData.length === 0){
      // Call the service and display colleges
      getCollegeData(endpoint).then(() => checkCollegeExist(collegeName))
        .catch(function (err){
          console.log('isCollegeExist:: No college data: '+ err)
        });
    }
    else{
      // display colleges
      checkCollegeExist(collegeName);
    }
  }

  function checkCollegeExist(cname){
    let responseToUser, text;
    let collegeLength = Object.keys(app.data.collegeData.college).length;
    console.log('checkCollegeExist => Length is -> '+ collegeLength);

    if ( collegeLength === 0 ){
      responseToUser = 'No colleges available at this time';
      text = 'No colleges available at this time';
    }

    if (cname === null && cname === undefined){
      text = 'I am not sure how to help with that';
      responseToUser = 'I am not sure how to help with that';
    }

    else{
      for ( let i = 0; i < collegeLength; i++)
      {
        let college = app.data.collegeData.college[i]
        let paramCollegeName = cname.toString().toLowerCase()
        let collegeName = college['name'].toString().toLowerCase()
        console.log('Param College Name: '+paramCollegeName+ '\nCollege Name: '+collegeName)
        if(collegeName === paramCollegeName){
          text = '<speak> Yes! CSUF has '+collegeName+ '. <break time="1s"/> Would you like to know more? </speak>';
          responseToUser = '<speak> Yes! CSUF has '+collegeName+ '. <break time="1s"/> Would you like to know more? </speak>';
          break;
        }
        else if (collegeName.includes(paramCollegeName)){
          text = '<speak> Yes! CSUF has '+collegeName+ '. <break time="1s"/> Would you like to know more? </speak>';
          responseToUser = '<speak> Yes! CSUF has '+collegeName+ '. <break time="1s"/> Would you like to know more? </speak>';
          break;
        }
        else{
          responseToUser = 'CSUF does not teach ' +paramCollegeName+' currently';
          text = 'CSUF does not teach ' +paramCollegeName+' currently';
        }
      }
    }
    if (requestSource === googleAssistantRequest) {
      sendGoogleResponse(responseToUser);
    } else {
      sendResponse(text);
    }
  }


  function collegeDescription(collegeName, endpoint){
    if (app.data.collegeData.length === 0){
      // Call the service and display colleges
      getCollegeData(endpoint).then(() => findCollegeDescription(collegeName))
        .catch(function (err){
          console.log('collegeDescription:: No college data: '+ err)
        });
    }
    else{
      // display colleges
      findCollegeDescription(collegeName);
    }
  }

  function findCollegeDescription(cname){
    let responseToUser, text;
    let collegeLength = Object.keys(app.data.collegeData.college).length;
    console.log('findCollegeDescription => Length is -> '+ collegeLength);

    if ( collegeLength === 0 ){
      responseToUser = 'No colleges available at this time';
      text = 'No colleges available at this time';
    }
    else{
      for ( let i = 0; i < collegeLength; i++)
      {
        let college = app.data.collegeData.college[i]
        let paramCollegeName = cname.trim().toString().toLowerCase()
        let collegeName = college.name.trim().toString().toLowerCase()
        console.log('findCollegeDescription:: Param College Name: '+paramCollegeName+ '\nCollege Name: '+collegeName)
        if(collegeName === paramCollegeName){

          text = '<speak> Okay. <break time="1s"/> According to the catalog - <break time="1s"/>'+ college.description +'</speak>';

          let googleRichResponse = app.buildRichResponse()
            .addSimpleResponse(text)
            .addBasicCard(app.buildBasicCard(college.description)
              .setTitle(collegeName)
              .addButton('Read More: ', baseURL+college.url)
            );
          responseToUser = {
            googleRichResponse: googleRichResponse,
            speech: text,
            displayText: text
          }

          break;
        }
        else if (collegeName.includes(paramCollegeName)){
          text = '<speak> Okay. <break time="1s"/> According to the catalog - <break time="1s"/>'+ college.description +'</speak>';

          let googleRichResponse = app.buildRichResponse()
            .addSimpleResponse(text)
            .addBasicCard(app.buildBasicCard(college.description)
              .setTitle(collegeName)
              .addButton('Read More: ', baseURL+college.url)
            );
          responseToUser = {
            googleRichResponse: googleRichResponse,
            speech: text,
            displayText: text
          }

          break;
        }
        else{
          responseToUser = 'Sorry! I am unable to find the information for ' +paramCollegeName;
          text = 'Sorry! I am unable to find the information for ' +paramCollegeName;
        }
      }
    }
    if (requestSource === googleAssistantRequest) {
      sendGoogleResponse(responseToUser);
    } else {
      sendResponse(text);
    }
  }


  function showPrerequisite(courseName, endpoint){
    if (app.data.courseData.length === 0){
      getCourseData(endpoint).then(() => checkCoursePrerequisite(courseName))
        .catch(function (err){
          console.log('showPrerequisite:: No course data '+err)
        });
    }
    else{
      checkCoursePrerequisite(courseName);
    }
  }

  function checkCoursePrerequisite(courseParam){

    // TODO - CPSC 120 Prereq is not correct and needs to be fixed

    let responseToUser, text;
    console.log('Inside Course Prerequisite')
    console.log('Courses are:: '+app.data.courseData)
    console.log('Specific Courses are:: '+app.data.courseData['specific courses'])
    let courseLength = app.data.courseData['specific courses'].length;
    console.log('checkCoursePrerequisite => Length is -> '+ courseLength);
    let courses = app.data.courseData['specific courses']
    if ( courseLength === 0 ){
      //responseToUser = 'No courses available at this time';
      text = 'No courses available at this time';
    }
    else{
      for ( let i = 0; i < courseLength; i++)
      {
        let course = courses[i]
        console.log("checkCoursePrerequisite:: Course is :: "+course.toString())
        let paramCourseName = courseParam.trim().toString().toLowerCase()
        let courseName = course['name'].trim().toString().toLowerCase()
        let courseNumber = course['short_name'].trim().toString().toLowerCase()

        console.log('Param course Name: '+paramCourseName+ '\nCourse Name: '+courseName)
        if(courseName === paramCourseName || courseNumber === paramCourseName){

          let type = course['type']
          let prerequisite = course['prerequisite'];
          console.log("Prerequisite is:: "+prerequisite)
          console.log("Prerequisite 1 is:: "+course.prerequisite)
          if(prerequisite.length > 0){
            text = 'The ' +type+ ' for ' + paramCourseName + ' is ' + prerequisite;
          }
          else {
            text = 'There is no prerequisite for '+paramCourseName;
          }
          let googleRichResponse = app.buildRichResponse()
            .addSimpleResponse(text)
            .addBasicCard(app.buildBasicCard(course['description'])
              .setTitle(courseName)
              .addButton('Read More', course['url'])
            );
          responseToUser = {
            googleRichResponse: googleRichResponse,
            speech: text,
            displayText: text
          }

          break;
        }
        else if (courseName.includes(paramCourseName) || courseNumber.includes(paramCourseName)){

          let type = course['type']
          let prerequisite = course['prerequisite'];

          if(prerequisite.length > 0){
            text = 'The ' +type+' for ' + paramCourseName + ' is ' + prerequisite;
          }
          else {
            text = 'There is no prerequisite for '+paramCourseName;
          }

          let googleRichResponse = app.buildRichResponse()
            .addSimpleResponse(text)
            .addBasicCard(app.buildBasicCard(course['description'])
              .setTitle(courseName)
              .addButton('Read More', course['url'])
            );
          responseToUser = {
            googleRichResponse: googleRichResponse,
            speech: text,
            displayText: text
          }

          break;
        }
        else{
          responseToUser = 'Sorry I am unable to find prerequsite for ' +paramCourseName;
          text = 'Sorry I am unable to find prerequsite for ' +paramCourseName;
        }
      }
    }
    if (requestSource === googleAssistantRequest) {
      sendGoogleResponse(responseToUser);
    } else {
      sendResponse(text);
    }
  }

  function showColleges(endpoint){
    if (app.data.collegeData.college.length === 0){
      getCollegeData(endpoint).then(() => buildSingleCollegeResponse())
        .catch(function (err){
          console.log('showColleges:: No college data '+err)
        });
    }
    else{
      buildSingleCollegeResponse();
    }
  }

  function buildSingleCollegeResponse(collegeName){
    let responseToUser, text;
    let collegeLength = Object.keys(app.data.collegeData.college).length;
    if ( collegeLength === 0){
      responseToUser = 'No colleges available at this time';
      text = 'No colleges available at this time';
    }
    else if ( app.data.collegeCount < collegeLength ){
      //display card or text
      let college = app.data.collegeData.college[app.data.collegeCount];
      text = 'College number ' + (app.data.collegeCount + 1) + '';
      text += college.name;
      let googleRichResponse = app.buildRichResponse()
        .addSimpleResponse(text)
        .addBasicCard(app.buildBasicCard('This is a basic card')
          .setTitle(college.name)
          .addButton('Read More', baseURL+college.url)
        );
      responseToUser = {
        googleRichResponse: googleRichResponse,
        speech: text,
        displayText: text
      }
    }
    else{
      responseToUser = 'No more colleges';
    }
    if (requestSource === googleAssistantRequest) {
      sendGoogleResponse(responseToUser);
    } else {
      sendResponse(text);
    }
  }


  // Call the service to get data
  function getCourseData(endpoint){
    return requestAPI(config.serviceURL + endpoint)
      .then(function (data) {
        let courses = JSON.parse(data)
        if (courses.hasOwnProperty('specific courses')){
          saveCourseData(courses)
        }
        return null;
      })
      .catch(function (err) {
        console.log('getCourseData::' +endpoint+ ' No course data'+ err)
      });
  }

  function saveCourseData(data){
    app.data.courseData = data;
    console.log('saveCourseData:: Saving Course Data: '+app.data.courseData)
  }


  // Call the service to get data
  function getCollegeData(endpoint){
    return requestAPI(config.serviceURL + endpoint)
      .then(function (data) {
        let colleges = JSON.parse(data)
        if (colleges.hasOwnProperty('college')){
          saveCollegeData(colleges)
        }
        return null;
      })
      .catch(function (err) {
        console.log('getCollegeData::' +endpoint+ ' No college data'+ err)
      });
  }

  function saveCollegeData(data){
    app.data.collegeData = data;
    console.log(app.data.collegeData)
  }


  // Function to send correctly formatted Google Assistant responses to Dialogflow which are then sent to the user
  function sendGoogleResponse (responseToUser, endConversation = false) {
    if (typeof responseToUser === 'string') {
      app.ask(responseToUser); // Google Assistant response
    } else {
      // If speech or displayText is defined use it to respond
      let googleResponse = app.buildRichResponse().addSimpleResponse({
        speech: responseToUser.speech || responseToUser.displayText,
        displayText: responseToUser.displayText || responseToUser.speech
      });
      // Optional: Overwrite previous response with rich response
      if (responseToUser.googleRichResponse) {
        googleResponse = responseToUser.googleRichResponse;
      }
      // Optional: add contexts (https://dialogflow.com/docs/contexts)
      if (responseToUser.googleOutputContexts) {
        app.setContext(...responseToUser.googleOutputContexts);
      }
      if (endConversation){
        app.tell(googleResponse)
      } else{
        app.ask(googleResponse)
      }
      console.log('Response to Dialogflow (AoG): ' + JSON.stringify(googleResponse));
      app.ask(googleResponse); // Send response to Dialogflow and Google Assistant
    }
  }
  // Function to send correctly formatted responses to Dialogflow which are then sent to the user
  function sendResponse (responseToUser) {
    // if the response is a string send it as a response to the user
    if (typeof responseToUser === 'string') {
      let responseJson = {};
      responseJson.speech = responseToUser; // spoken response
      responseJson.displayText = responseToUser; // displayed response
      response.json(responseJson); // Send response to Dialogflow
    } else {
      // If the response to the user includes rich responses or contexts send them to Dialogflow
      let responseJson = {};
      // If speech or displayText is defined, use it to respond (if one isn't defined use the other's value)
      responseJson.speech = responseToUser.speech || responseToUser.displayText;
      responseJson.displayText = responseToUser.displayText || responseToUser.speech;
      // Optional: add rich messages for integrations (https://dialogflow.com/docs/rich-messages)
      responseJson.data = responseToUser.data;
      // Optional: add contexts (https://dialogflow.com/docs/contexts)
      responseJson.contextOut = responseToUser.outputContexts;
      console.log('Response to Dialogflow: ' + JSON.stringify(responseJson));
      response.json(responseJson); // Send response to Dialogflow
    }
  }
}
// Construct rich response for Google Assistant (v1 requests only)
const app = new DialogflowApp();
const googleRichResponse = app.buildRichResponse()
  .addSimpleResponse('This is the first simple response for Google Assistant')
  .addSuggestions(
    ['Suggestion Chip', 'Another Suggestion Chip'])
  // Create a basic card and add it to the rich response
  .addBasicCard(app.buildBasicCard(`This is a basic card.  Text in a
 basic card can include "quotes" and most other unicode characters
 including emoji 📱.  Basic cards also support some markdown
 formatting like *emphasis* or _italics_, **strong** or __bold__,
 and ***bold itallic*** or ___strong emphasis___ as well as other things
 like line  \nbreaks`) // Note the two spaces before '\n' required for a
  // line break to be rendered in the card
    .setSubtitle('This is a subtitle')
    .setTitle('Title: this is a title')
    .addButton('This is a button', 'https://assistant.google.com/')
    .setImage('https://developers.google.com/actions/images/badges/XPM_BADGING_GoogleAssistant_VER.png',
      'Image alternate text'))
  .addSimpleResponse({ speech: 'This is another simple response',
    displayText: 'This is the another simple response 💁' });
// Rich responses for Slack and Facebook for v1 webhook requests
const richResponsesV1 = {
  'slack': {
    'text': 'This is a text response for Slack.',
    'attachments': [
      {
        'title': 'Title: this is a title',
        'title_link': 'https://assistant.google.com/',
        'text': 'This is an attachment.  Text in attachments can include \'quotes\' and most other unicode characters including emoji 📱.  Attachments also upport line\nbreaks.',
        'image_url': 'https://developers.google.com/actions/images/badges/XPM_BADGING_GoogleAssistant_VER.png',
        'fallback': 'This is a fallback.'
      }
    ]
  },
  'facebook': {
    'attachment': {
      'type': 'template',
      'payload': {
        'template_type': 'generic',
        'elements': [
          {
            'title': 'Title: this is a title',
            'image_url': 'https://developers.google.com/actions/images/badges/XPM_BADGING_GoogleAssistant_VER.png',
            'subtitle': 'This is a subtitle',
            'default_action': {
              'type': 'web_url',
              'url': 'https://assistant.google.com/'
            },
            'buttons': [
              {
                'type': 'web_url',
                'url': 'https://assistant.google.com/',
                'title': 'This is a button'
              }
            ]
          }
        ]
      }
    }
  }
};
/*
* Function to handle v2 webhook requests from Dialogflow
*/
function processV2Request (request, response) {
  // An action is a string used to identify what needs to be done in fulfillment
  let action = (request.body.queryResult.action) ? request.body.queryResult.action : 'default';
  // Parameters are any entites that Dialogflow has extracted from the request.
  let parameters = request.body.queryResult.parameters || {}; // https://dialogflow.com/docs/actions-and-parameters
  // Contexts are objects used to track and store conversation state
  let inputContexts = request.body.queryResult.contexts; // https://dialogflow.com/docs/contexts
  // Get the request source (Google Assistant, Slack, API, etc)
  let requestSource = (request.body.originalDetectIntentRequest) ? request.body.originalDetectIntentRequest.source : undefined;
  // Get the session ID to differentiate calls from different users
  let session = (request.body.session) ? request.body.session : undefined;
  // Create handlers for Dialogflow actions as well as a 'default' handler
  const actionHandlers = {
    // The default welcome intent has been matched, welcome the user (https://dialogflow.com/docs/events#default_welcome_intent)
    'input.welcome': () => {
      sendResponse('Hello, Welcome to my Dialogflow agent!'); // Send simple response to user
    },

    'input.mvoting': () =>{
      sendResponse('Voting');
    },
    // The default fallback intent has been matched, try to recover (https://dialogflow.com/docs/intents#fallback_intents)
    'input.unknown': () => {
      // Use the Actions on Google lib to respond to Google requests; for other requests use JSON
      sendResponse('I\'m having trouble, can you try that again?'); // Send simple response to user
    },
    // Default handler for unknown or undefined actions
    'default': () => {
      let responseToUser = {
        //fulfillmentMessages: richResponsesV2, // Optional, uncomment to enable
        //outputContexts: [{ 'name': `${session}/contexts/weather`, 'lifespanCount': 2, 'parameters': {'city': 'Rome'} }], // Optional, uncomment to enable
        fulfillmentText: 'This is from Dialogflow\'s Cloud Functions for Firebase editor! :-)' // displayed response
      };
      sendResponse(responseToUser);
    }
  };
  // If undefined or unknown action use the default handler
  if (!actionHandlers[action]) {
    action = 'default';
  }
  // Run the proper handler function to handle the request from Dialogflow
  actionHandlers[action]();
  // Function to send correctly formatted responses to Dialogflow which are then sent to the user
  function sendResponse (responseToUser) {
    // if the response is a string send it as a response to the user
    if (typeof responseToUser === 'string') {
      let responseJson = {fulfillmentText: responseToUser}; // displayed response
      response.json(responseJson); // Send response to Dialogflow
    } else {
      // If the response to the user includes rich responses or contexts send them to Dialogflow
      let responseJson = {};
      // Define the text response
      responseJson.fulfillmentText = responseToUser.fulfillmentText;
      // Optional: add rich messages for integrations (https://dialogflow.com/docs/rich-messages)
      if (responseToUser.fulfillmentMessages) {
        responseJson.fulfillmentMessages = responseToUser.fulfillmentMessages;
      }
      // Optional: add contexts (https://dialogflow.com/docs/contexts)
      if (responseToUser.outputContexts) {
        responseJson.outputContexts = responseToUser.outputContexts;
      }
      // Send the response to Dialogflow
      console.log('Response to Dialogflow: ' + JSON.stringify(responseJson));
      response.json(responseJson);
    }
  }
}
const richResponseV2Card = {
  'title': 'Title: this is a title',
  'subtitle': 'This is an subtitle.  Text can include unicode characters including emoji 📱.',
  'imageUri': 'https://developers.google.com/actions/images/badges/XPM_BADGING_GoogleAssistant_VER.png',
  'buttons': [
    {
      'text': 'This is a button',
      'postback': 'https://assistant.google.com/'
    }
  ]
};
const richResponsesV2 = [
  {
    'platform': 'ACTIONS_ON_GOOGLE',
    'simple_responses': {
      'simple_responses': [
        {
          'text_to_speech': 'Spoken simple response',
          'display_text': 'Displayed simple response'
        }
      ]
    }
  },
  {
    'platform': 'ACTIONS_ON_GOOGLE',
    'basic_card': {
      'title': 'Title: this is a title',
      'subtitle': 'This is an subtitle.',
      'formatted_text': 'Body text can include unicode characters including emoji 📱.',
      'image': {
        'image_uri': 'https://developers.google.com/actions/images/badges/XPM_BADGING_GoogleAssistant_VER.png'
      },
      'buttons': [
        {
          'title': 'This is a button',
          'open_uri_action': {
            'uri': 'https://assistant.google.com/'
          }
        }
      ]
    }
  },
  {
    'platform': 'FACEBOOK',
    'card': richResponseV2Card
  },
  {
    'platform': 'SLACK',
    'card': richResponseV2Card
  }
];