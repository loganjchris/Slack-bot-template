import json

def reader(msg):

    """This function opens the saved JSON response from save_sheets.py.
    It searches the first column for the passed msg and returns column 2.
    If there is no match it returns a pre-set response
    """

    with open('data.txt', encoding='utf-8') as json_file:
        result = json.load(json_file)

    values = result.get('values', [])

    #Makes sure there is a response always
    response = False


    #Search spreadsheet for text
    for row in values:
        if row[0] in msg:
            response = row[1]

    return response
