# YAIA Email Summarizer


> "**Y**et **A**nother **I**ntelligent **A**pproach"

#### Overview

Email is playing an important role on most almost everybody’s lives. It is an easy and a common form of communication nowadays. However, people is constantly receiving a significant amount of emails that takes also significant amount of time to read.
The technological advances have brought a lot of changes in people’s life style. With the arrival of the IoT, for example, several wearables and devices send feedback, alerts, and notifications to users through emails.
In addition, people rely on their email account for communication and information. A wide variety of services, require email authentication to send the user a status/report of subscriptions or programmed tasks. Entertainment or news, are found in newsletters and magazines, which provide a variety of articles and product releases.
All this, is causing an email overload that will continue increasing. Email summarization could significantly help in this matter. 

##### Users / users case

|_User_|_User case_|
|------|---------|
|Curious person that is open to increase their productivity by using technological tools.|<ul><li>A person who wants to avoid reading the new emails, simples or in a thread. A nice summary of them let her/him know what is going on and make decisions faster.</li></ul>|
|Busy person that want to increase its performance at work.|<ul><li>A busy person that have several priorities rather than read emails. A concise email summary of the new inbox messages let her/him make decisions that can change her/his current workflow.</li><li>A busy person that is pretty new at work and need a catch up of an ongoing conversation. A summary of an email thread let her/him know what is happening there.</li></ul>|
|Tech people (open source developers mainly) that always try something new, give feedback and contribute to improve functionality.|<ul><li>A person who is always exploring new paths that converge in the AI development. The first release of this work is the starting point for her/him to contribute to the intelligent systems that will make our lives easier.</li></ul>|


##### Problem

Email overload: people is constantly receiving a significant amount of emails that take also significant amount of time to read.

#### Installation

##### Requirements
   - Python 3
   - Conda 4.4.10 or later
   - pip 10.0.1
   
##### Download or clone YAIA
```
git clone https://github.com/teresita-guerrero/DSR-Journey.git
```

##### The virtual environment

Open a terminal and go to the YAIA directory:
```
cd DSR-Journey/Portfolio/YAIA
```

- Create a virtual environment:
```
conda env create -f yaia.yml
```
- Activate the virtual environment: 
```
source activate yaia
```
- Set the environment variables. This is for development purposes 
(as the app stills in development this step is required):
```
. ./setup.sh
```

##### Running the application

- Go to the app directory:
```
cd portfolio/YAIA/app
```
- Run the API:
```
FLASK_APP=api.py FLASK_DEBUG=1 python -m flask run --port=8080
```
- Go to the browser and type:
```
http://localhost:8080
```

#### The ML Script

The machine learning process was added to this repo. You can play with it by 
changing the features, parameters and so on.

 _Follow the directions: [here](/ml/)_


