## Voice Conversational Chatbot for California State University - Fullerton

### Purpose
Build a domain-specific voice conversational app using google assistant to assist students to find answers to their most frequently asked questions at California State University, Fullerton. Some of such questions are, but not limited to, course perquisites, faculty office hours, course information. 

### This project is divided into two parts: 
## Part 1
Part 1 scrapes the data from California State University - Fullerton catalog, insert the data in postgreSQL on google cloud and create endpoints to have the data access over HTTP.

### Steps to setup
In order to have the local development envirnoment set-up, Following steps needs to be performed:

#### 1. Prerequsites:
The project scrapes data from the California State University catalog [1] and insert it on google cloud postgreSQL.    Therefore, this project requires you to have a google cloud project with PostgreSQL services enable. Refer google cloud documentation [2] to know the steps.

#### 2. Clone the repositroy:
Once you have google cloud project, clone this reposiroty into your local development envirnoment. 
  
#### 3. Set classpath:
Set the following variable in your classpath:
> export SQLALCHEMY_DATABASE_URI=postgresql+psycopg2://[USER_NAME]:[PASSWORD]@127.0.0.1:5432/[DATABASE_NAME]

#### 4. Virtual Enviournment setup:
Create a virtual envirnoment and install all the dependecies given in requirements.txt in the project. Refer [3] to know how to setup and install dependecies in a virtual envirnoment. 

#### 5. Create schema and insert data to google cloud:
Execute _python scraperdboperations.py_ from the project directory. This will create the schema and insert all data into the database on google cloud. 
  
#### 6. OpenAPI.yaml changes:
Replace the value of __host:__ variable with your google cloud project URL.

#### 7. Deploy services on google cloud:
Execute __gcloud endpoints services deploy openapi-appengine.yaml__ command from project home directory. This will deploy your endpoints on google cloud. Please make sure you have google cloud SDK installed and configured on your local machine. Refer to google cloud documentation [4]. Execution of this command will generate the project name and configuration id. Please note them as you will them in the next step.
  
#### 8. Now you are ready to deploy the project on google cloud: 
In order to deploy, you need to change the endpoint api services configuration in __api.yaml__ file. Open the api.yaml file and change the following with the project name and configuration id you got in step 7. 

> endpoints_api_service: <br /> 
>   &nbsp; &nbsp; name: [Name]<br />
>   &nbsp; &nbsp; config_id: [CONFIG_ID]

#### 9. After the successful deployment hit following endpoints, and you should be able to see the college data:

https://[Project URL]/colleges <br />
https://[Project URL]/departments <br />
https://[Project URL]/programs <br />
https://[Project URL]/courses <br />
https://[Project URL]/specificcolleges <br />
https://[Project URL]/generalcolleges <br />


## Part 2

Part 2 uses the endpoints created in part 1. These endpoints can be called anywhere as httprequest. However, I am using dialogflow and cloud functions for firebase in this project. Part 2 expect you to have a agent created on dialogflow. Refer [5] to create an agent on dialogflow and then refer the following steps to setup part 2 in your local development enviournment.

#### 1. Upload intents on your dialogflow agent:
First you will need to upload intents to your dialogflow agent. Click on upload intents on your dialog flow console and upload all the intent present under *<PROJECT-HOME-DIR>\client\google-assistant\intents*.

#### 1. Deploy firebase functions on dialogflow: 
Before you upload firebase functions, make sure you have webhook enabled for your dialogflow agent. Once you have that, do the following:

1.  Open *<PROJECT-HOME-DIR>/client/google-assistant/firebase/functions/config/config.js* and change the *config.serviceURL* to your google cloud project URL. 

2. Open terminal and navigate to *<PROJECT-HOME-DIR>/client/google-assistant/firebase/functions*. Run the following command to deploy the firebase function: 
__firebase deploy --only functions__

That's it. Now you can test the app by asking questions like: 

"does csuf has business course"
"what is the prerequisite for CPSC 481" etc...

Please refer to firebase documentation [6] on how to deploy firebase functions. 

##### References

[1] - http://catalog.fullerton.edu <br />
[2] - https://cloud.google.com/appengine/docs/flexible/python/using-cloud-sql-postgres <br />
[3] - https://packaging.python.org/guides/installing-using-pip-and-virtualenv/ <br />
[4] - https://cloud.google.com/appengine/downloads <br />
[5] - https://dialogflow.com/docs/agents <br />
[6] - https://firebase.google.com/docs/cli/


Developer - Puneet Jain punitjain@csu.fullerton.edu <br /> 
Advisor - Dr. Michael Shafae <br />
Reviewer - Dr. Anand Panangadan
