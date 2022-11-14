from __future__ import print_function

from apiclient import discovery
from httplib2 import Http
from oauth2client import client, file, tools



def create_google_form(path_to_client_json, questions, title, form_description='Sample Form'):
    SCOPES = "https://www.googleapis.com/auth/forms.body"
    DISCOVERY_DOC = "https://forms.googleapis.com/$discovery/rest?version=v1"

    store = file.Storage('token.json')
    creds = None
    if not creds or creds.invalid:
        flow = client.flow_from_clientsecrets(path_to_client_json, SCOPES)
        flags = tools.argparser.parse_args(args=[])
        flags.noauth_local_webserver = True
        creds = tools.run_flow(flow, store,flags)

    form_service = discovery.build('forms', 'v1', http=creds.authorize(
        Http()), discoveryServiceUrl=DISCOVERY_DOC, static_discovery=False)

    # Request body for creating a form
    NEW_FORM = {
        "info": {
            "title": title,
        }
    }
    req_list = []
    for question in questions:
        req_list.append(
            {
            "createItem": {
            "item": {
                "title": question,
                "questionItem" :{ 
                "question": {
                    "required": True,
                    
                    "textQuestion": {
                        
                        "paragraph": False
                    }
                },
               }
            },
            "location": {
                "index": 0
            }
        }
        })
         
    NEW_QUESTION = {
        "requests": req_list
        }
    result = form_service.forms().create(body=NEW_FORM).execute()

    # Adds the question to the form
    question_setting = form_service.forms().batchUpdate(formId=result["formId"], body=NEW_QUESTION).execute()

    # Prints the result to show the question has been added
    get_result = form_service.forms().get(formId=result["formId"]).execute()

    return get_result
