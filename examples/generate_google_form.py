from repaper import repaper

re_paper = repaper(
    '../samples/test.jpg')

form_id = re_paper.make_google_from(
    '../secrets/credentials.json')

print(f'''Form created with form id: {form_id["formId"]} and is accessible at: \n https://docs.google.com/forms/d/{form_id['formId']}/viewform \n
edit and publish the form to make it accessible to others''')
