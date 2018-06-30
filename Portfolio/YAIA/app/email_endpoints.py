import flask
import google.oauth2.credentials
import googleapiclient.discovery
import base64

from authentication import *


# This variable specifies the name of a file that contains the OAuth 2.0
# information for this application, including its client_id and client_secret.
CLIENT_SECRETS_FILE = "client_secret.json"
c = config.emailConfiguration()
# This OAuth 2.0 access scope allows for full read/write access to the
# authenticated user's account and requires requests to use an SSL connection.
SCOPES = c["service_scopes"]
API_SERVICE_NAME = c["service_name"]
API_VERSION = c["service_version"]


def apiRequestMails():
    if 'credentials' not in flask.session:
        return flask.redirect('authorize')

    # Load credentials from the session.
    credentials = google.oauth2.credentials.Credentials(
        **flask.session['credentials'])

    service = googleapiclient.discovery.build(
        API_SERVICE_NAME, API_VERSION, credentials=credentials)

    # Call the gmail API
    query = "in:inbox is:unread -category:(promotions OR social)"
    messages = service.users().messages().list(userId='me', q=query).execute().\
        get('messages', [])

    msgs = dict()
    for message in messages:
        m = service.users().messages().get(userId='me',
                                               id=message['id']).execute()

        mDate = ''
        mFrom = ''
        mTo = ''
        mSubject = ''
        for header in m['payload']["headers"]:
            if header['name'] == "Date":
                mDate = header['value']
            if header['name'] == "From":
                mFrom = header['value']
            if header['name'] == "To":
                mTo = header['value']
            if header['name'] == "Subject":
                mSubject= header['value']

        message_data = m['payload']["parts"][0]["body"]["data"]
        decoded_message = base64.urlsafe_b64decode(message_data)

        msgs[message['id']] = {
            'thread_num': m['threadId'],
            'id': m['id'],
            'received': mDate,
            'from': mFrom,
            'to': mTo,
            'subject': mSubject,
            'message_content': str(decoded_message, 'utf-8')
        }

    # Save credentials back to session in case access token was refreshed.
    # ACTION ITEM: In a production app, you likely want to save these
    #              credentials in a persistent database instead.
    flask.session['credentials'] = credentials_to_dict(credentials)

    return flask.jsonify(**msgs)


def apiRequestMailByID(messageID):
    if 'credentials' not in flask.session:
        return flask.redirect('authorize')

    # Load credentials from the session.
    credentials = google.oauth2.credentials.Credentials(
        **flask.session['credentials'])

    service = googleapiclient.discovery.build(
        API_SERVICE_NAME, API_VERSION, credentials=credentials)

    # Call the Gmail API
    m = service.users().messages().get(userId='me',id=messageID).execute()

    msg = dict()
    mDate = ''
    mFrom = ''
    mTo = ''
    mSubject = ''
    for header in m['payload']["headers"]:
        if header['name'] == "Date":
            mDate = header['value']
        if header['name'] == "From":
            mFrom = header['value']
        if header['name'] == "To":
            mTo = header['value']
        if header['name'] == "Subject":
            mSubject= header['value']

    message_data = m['payload']["parts"][0]["body"]["data"]
    decoded_message = base64.urlsafe_b64decode(message_data)

    msg = {
        'thread_num': m['threadId'],
        'id': m['id'],
        'received': mDate,
        'from': mFrom,
        'to': mTo,
        'subject': mSubject,
        'message_content': str(decoded_message, 'utf-8')
    }

    # Save credentials back to session in case access token was refreshed.
    # ACTION ITEM: In a production app, you likely want to save these
    #              credentials in a persistent database instead.
    flask.session['credentials'] = credentials_to_dict(credentials)

    return flask.jsonify(**msg)


def apiRequestThreads():
    if 'credentials' not in flask.session:
        return flask.redirect('authorize')

    # Load credentials from the session.
    credentials = google.oauth2.credentials.Credentials(
        **flask.session['credentials'])

    service = googleapiclient.discovery.build(
        API_SERVICE_NAME, API_VERSION, credentials=credentials)

    # Call the Gmail API
    query = "in:inbox is:unread -category:(promotions OR social)"
    threads = service.users().threads().list(userId='me', q=query).execute().\
        get('threads', [])

    thrds = dict()
    for thread in threads:
        tdata = service.users().threads().get(userId='me', id=thread['id']).\
            execute()
        nmsgs = len(tdata['messages'])

        if nmsgs >= 1:  # skip if <3 msgs in thread
            msg = tdata['messages'][0]['payload']
            mfrom = ''
            msubject = ''
            mDate = ''
            for header in msg['headers']:
                if header['name'] == 'From':
                    mfrom = header['value']
                if header['name'] == 'Subject':
                    msubject = header['value']
                if header['name'] == 'Date':
                    mDate = header['value']
            if msubject:  # skip if no Subject line
                thrds[thread['id']] = {
                    'id': thread['id'],
                    'from': mfrom,
                    'subject': msubject + ' ('+ str(nmsgs) + ')',
                    'date': mDate
                }

    # Save credentials back to session in case access token was refreshed.
    # ACTION ITEM: In a production app, you likely want to save these
    #              credentials in a persistent database instead.
    flask.session['credentials'] = credentials_to_dict(credentials)

    return flask.jsonify(**thrds)


# request mail content for a single thread
def apiRequestThreadMails(threadID):
    if 'credentials' not in flask.session:
        return flask.redirect('authorize')

    # Load credentials from the session.
    credentials = google.oauth2.credentials.Credentials(
        **flask.session['credentials'])

    service = googleapiclient.discovery.build(
        API_SERVICE_NAME, API_VERSION, credentials=credentials)

    # Call the Gmail API
    messages = service.users().threads().get(userId='me', id=threadID).\
        execute().get('messages', [])

    msgs = dict()
    for message in messages:
        m = service.users().messages().get(userId='me',
                                               id=message['id']).execute()

        mDate = ''
        mFrom = ''
        mTo = ''
        mSubject = ''
        for header in m['payload']["headers"]:
            if header['name'] == "Date":
                mDate = header['value']
            if header['name'] == "From":
                mFrom = header['value']
            if header['name'] == "To":
                mTo = header['value']
            if header['name'] == "Subject":
                mSubject= header['value']

        message_data = m['payload']["parts"][0]["body"]["data"]
        decoded_message = base64.urlsafe_b64decode(message_data)

        msgs[message['id']] = {
            'thread_num': m['threadId'],
            'id': m['id'],
            'received': mDate,
            'from': mFrom,
            'to': mTo,
            'subject': mSubject,
            'message_content': str(decoded_message, 'utf-8')
        }

    # Save credentials back to session in case access token was refreshed.
    # ACTION ITEM: In a production app, you likely want to save these
    #              credentials in a persistent database instead.
    flask.session['credentials'] = credentials_to_dict(credentials)

    return flask.jsonify(**msgs)

