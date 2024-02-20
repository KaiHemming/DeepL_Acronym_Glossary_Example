# Allows users to administer glossaries, which are then outputted in DeepL's request format. 
# Part of a solution to replace acronyms in text, using DeepL glossaries.
# Supports only tsv format.

# Example Request:
# curl -X POST 'https://api-free.deepl.com/v2/glossaries' \
# --header 'Authorization: DeepL-Auth-Key [yourAuthKey]' \
# --header 'Content-Type: application/json' \
# --data '{
#   "name": "My Glossary",
#   "source_lang": "en",
#   "target_lang": "de",
#   "entries": "Hello\tGuten Tag",
#   "entries_format": "tsv"
# }'
# # https://www.deepl.com/de/docs-api/glossaries 

import json
import os
from flask import Flask, request

app = Flask(__name__)
AUTH_KEY = "[yourAuthKey]" # TODO: Auth key goes here
URL = "https://api-free.deepl.com/v2/glossaries"
HEADERS = {"Authorization" : "DeepL-Auth-Key " + AUTH_KEY,
           "Content-Type" : "application/json"}


@app.route('/')
def hello():
    return 'App is running.'

@app.route('/glossary', methods=['GET', 'POST'])
def glossaryReadWrite():
    requestJSON = request.get_json()
    glossaryName = requestJSON.get("glossaryName")
    if request.method == 'POST':
        if not os.path.isfile(glossaryName + ".dat"): 
            data = {
                "name": glossaryName,
                "source_lang": requestJSON.get("sourceLang"),
                "target_lang": requestJSON.get("targetLang"),
                "entries_format": "tsv"
            }
            with open(glossaryName + ".dat", "w") as fw:
                fw.write(json.dumps(data))
            with open(glossaryName + ".tsv", "w") as fw:
                fw.write(requestJSON.get("entries"))
                # return "Created glossary " + request.glossaryName 

            # TODO: Instead of returning as shown above, returned an example request, 
                # should be removed if in final implementation.

            return glossaryToRequest(glossaryName)
        else:
            # TODO: Check if definition(s) already exists in tsv
            with open(glossaryName + ".tsv", "a") as fa:
                # entries assumed to be formatted with trailing newline character
                fa.write(requestJSON.get("entries"))

            return "Added entries to " + glossaryName + ".tsv"
        
    return "Reading glossary " + glossaryName + "\n" + open(requestJSON.glossaryName + ".tsv").read()

# TODO: Not posted to https://api-free.deepl.com/v2/glossaries, example post request returned
# should post in final implementation
@app.route('/postGlossary', methods=['GET'])
def postGlossary():
    return glossaryToRequest(request.args.get("glossaryName"))


def glossaryToRequest(glossaryName):
    if os.path.isfile(glossaryName + ".dat"): 
        data = json.load(open(glossaryName + ".dat"))
        data["entries"] = open(glossaryName + ".tsv").read()

        # Example request
        # request = requests.post(URL, data = json.dumps(data), headers = HEADERS)

        return data
    else:
        return glossaryName + " not found."
 
if __name__ == '__main__':
    app.run(debug=True)
