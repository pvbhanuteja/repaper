=====
Usage
=====


To use repaper in a project::

    from repaper import repaper


To generate a google form from the a form image::
    from repaper import repaper

    # Specify path to image of the form
    re_paper = repaper(
        '../samples/test.jpg')

    # specify google oauth clients_secret.json path you can generate your own JSON file for your google 
    # account look at the docs here to generate : https://developers.google.com/forms/api/quickstart/python#set_up_your_environment
    form_id = re_paper.make_google_from(
        '../secrets/credentials.json')

    print(f'''Form created with form id: {form_id["formId"]} and is accessible at: \n https://docs.google.com/forms/d/{form_id['formId']}/viewform \n
    edit and publish the form to make it accessible to others''')

Command line usage to generate google form from image::
    repaper google-form --img_path ./samples/test.jpg --oauth_json ./secrets/credentials.json