# -*- coding: utf-8 -*-

import os
import flask
from authentication import *
import google.oauth2.credentials
from email_endpoints import *
from helper import *
from flask import render_template
from flask_bootstrap import Bootstrap


app = flask.Flask(__name__)
# Note: A secret key is included in the sample so that it works.
# If you use this code in your application, replace this with a truly secret
# key. See http://flask.pocoo.org/docs/0.12/quickstart/#sessions.
app.secret_key = 'REPLACE ME - this value is here as a placeholder.'

bootstrap = Bootstrap(app)


# Index
@app.route('/')
def index():
    if 'credentials' not in flask.session:
        return flask.redirect('authorize')

    # Load credentials from the session.
    credentials = google.oauth2.credentials.Credentials(
        **flask.session['credentials'])

    # Save credentials back to session in case access token was refreshed.
    # ACTION ITEM: In a production app, you likely want to save these
    #              credentials in a persistent database instead.
    flask.session['credentials'] = credentials_to_dict(credentials)

    print(flask.session['credentials'])
    return render_template('index.html')


# Get the list of mails
@app.route('/emails')
def getMails():
    return apiRequestMails()


# Get list of threads and their messages
@app.route('/threads')
def getThreads():
    threads = apiRequestThreads()

    # ToDo: order the threads based on the date (desc mode)
    # or ordering the data after the request
    return render_template('threads.html', threads=threads.get_json())


# Get emails per thread
@app.route('/threads/<threadID>')
def getThreadMails(threadID):
    emailList = apiRequestThreadMails(threadID)

    if len(emailList.get_json()) <=1:
        summary = singleSummary(threadID, emailList.get_json())
    else:
        summary = threadSummary(emailList.get_json())

    return render_template('summary.html', summary=summary)


# Authorize the YAIA app to access google user info
@app.route('/authorize')
def authorization():
    return authorize()


# Reconnect the session
@app.route('/oauth2callback')
def oauth2callback():
    return oauth2Callback()


# Revoke access to YAIA app
@app.route('/revoke')
def revoke_permission():
    return revoke()


# Clear the flask session
@app.route('/clear')
def clear_session():
    return clear_credentials()


if __name__ == '__main__':
    # When running locally, disable OAuthlib's HTTPs verification.
    # ACTION ITEM for developers:
    #     When running in production *do not* leave this option enabled.
    os.environ['OAUTHLIB_INSECURE_TRANSPORT']=True

    # Specify a hostname and port that are set as a valid redirect URI
    # for your API project in the Google API Console.
    app.run('localhost', 8080, debug=True)
