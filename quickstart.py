#!/usr/bin/env python
# -*- coding: utf-8 -*-
""" quickstart """
from __future__ import print_function
import pickle
import os.path
from typing import List, Any
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from flask import Flask

# If modifying these scopes, delete the file token.pickle.
CONFIG_PATH: str = "/Volumes/Data/skeptycal/Documents/_coding/google/secret/"
TOKEN_PATH: str = CONFIG_PATH + 'token.pickle'
CREDENTIALS_PATH: str = CONFIG_PATH + 'credentials.json'
# SCOPES: List[str] = ['https://www.googleapis.com/auth/contacts.readonly']
SCOPES: List[str] = ['https://www.googleapis.com/auth/contacts']
app = Flask(__name__)


def g_login_people_api_v1() -> build:
    """ Return People API V1 service to access google contact info.

        ### Scopes
        Read Only - See and Download Contacts when authenticated:

        SCOPES: List[str] =
        ['https://www.googleapis.com/auth/contacts.readonly']

        See, edit, download, and permanently delete your contacts:

        SCOPES: List[str] =
        ['https://www.googleapis.com/auth/contacts']

        Ref: https://developers.google.com/people/
        """
    creds: Any = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists(TOKEN_PATH):
        with open(TOKEN_PATH, 'rb') as token:
            creds = pickle.load(token)

    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                CREDENTIALS_PATH, SCOPES)
            creds = flow.run_local_server()
        # Save the credentials for the next run
        with open(TOKEN_PATH, 'wb') as token:
            pickle.dump(creds, token)

    return build('people', 'v1', credentials=creds)


def g_get_contact_data(_service: build, pageSize: int) -> Any:
    """ Returns a dictionary of contact informationself.
        pageSize - number of contacts. """
    results = _service.people().connections().list(
        resourceName='people/me',
        pageSize=pageSize,
        personFields='names,emailAddresses').execute()
    return results.get('connections', [])


@app.route('connections')
def serve_connections():
    """ Generate HTML page for connections. """
    pass


@app.route('/')
def hello():
    return "Hello World!"


def main():
    """Shows basic usage of the People API.
    Prints the name of the first 10 connections.
    """
    # Initialize People API Instance
    service = g_login_people_api_v1()

    # Call the People API
    page_size_num: int = 20
    print('List 10 connection names')
    connections = g_get_contact_data(service, pageSize=page_size_num)
    serve_connections(connections)
    for person in connections:
        names = person.get('names', [])
        if names:
            print(names)
            name = names[0].get('displayName')
            print(name)
            print('-' * 79)

    app.run()


if __name__ == '__main__':
    main()
