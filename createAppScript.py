"""
Shows basic usage of the Apps Script API.
Call the Apps Script API to create a new script project, upload a file to the
project, and log the script's URL to the user.
"""
import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient import errors
from googleapiclient.discovery import build

# If modifying these scopes, delete the file token.json.
SCOPES = [
    "https://www.googleapis.com/auth/script.projects",
    "https://www.googleapis.com/auth/spreadsheets",
    'https://www.googleapis.com/auth/drive'
]

SAMPLE_CODE = """
// Your custom function in Sheets
function onOpen() {
  const ui = SpreadsheetApp.getUi();
  ui.createMenu('AI Assistant')
    .addItem('Generate with Gemini', 'getAns')
    .addToUi();
}

function getAns() {
  const sheet = SpreadsheetApp.getActiveSpreadsheet().getActiveSheet();
  const cell = sheet.getActiveCell() 
  const row = cell.getRow();
  const col = cell.getColumn();
  const prompt = cell.getValue() 
  // const row = SpreadsheetApp.getCurrentCell().getRow();
  const headers = sheet.getRange(1, 1, 1, sheet.getLastColumn()).getValues()[0];
  const contextRange = sheet.getRange(row, 1, 1, sheet.getLastColumn()).getValues()[0];
  // const combVal = cols.map(function(value, index){
  //   return value + ' is ' + contextRange[index];
  // })

  var combVal = contextRange.map(function(value, index){
    if (value == null || value.trim() === ""){
      return ""
    }
    else{
      return headers[index] + ' is ' + value;
    }
  }) 
  if (prompt == null || prompt.trim() === ""){  
    var fullPrompt = `Context: ${combVal.join(" | ")} \nPrompt: Given the context - company information, Answer this question in only a few words with the answer only: ${headers[col-1]} of the company`;
  }
  else{
    var fullPrompt = `Context: ${combVal.join(" | ")} \nPrompt: Given the context - company information, Answer this question in only a few words: ${prompt}?`;
  }
  // const scrapedContent = scrapeWeb(prompt); // your own backend or proxy
  
  const finalResponse = callGeminiAPI(fullPrompt);

  cell.setValue(finalResponse);
  // cell.setValue(fullPrompt);
  return {'Row': row , 'combVal' : combVal , 'fullprompt': fullPrompt , 'response': finalResponse}
}

function callGeminiAPI(prompt) {
  const apiKey = "your_api_key";
  // const url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent?key=" + apiKey;
  const url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key=" + apiKey;

  const payload = {
    "contents": [{ "parts": [{ "text": prompt }] }]
  };

  const options = {
    method: 'POST',
    contentType: 'application/json',
    payload: JSON.stringify(payload)
  };

  const response = UrlFetchApp.fetch(url, options);
  const json = JSON.parse(response.getContentText());
  return json?.candidates?.[0]?.content?.parts?.[0]?.text || "No response from Gemini.";
}

// function doPost(e) {
//   const data = JSON.parse(e.postData.contents);
//   const prompt = data.prompt;
//   const result = GET_ANSWER(prompt); // or your internal function
//   return ContentService.createTextOutput(result);
// }

function doPost(e) {
  try {
    const data = JSON.parse(e.postData.contents);
    const prompt = data.prompt;

    // const answer = `You asked: ${prompt}`; // Replace with Gemini call or your logic
    const answer = GET_ANSWER(prompt)
    return ContentService.createTextOutput(JSON.stringify(answer)).setMimeType(ContentService.MimeType.JSON);
  } catch (err) {
    return ContentService.createTextOutput("Error: " + err.message);
  }
}
""".strip()

#SAMPLE_MANIFEST = """
# {
#   "timeZone": "America/New_York",
#   "exceptionLogging": "CLOUD"
# }
# """.strip()

SAMPLE_MANIFEST = """
{
  "timeZone": "America/New_York",
  "dependencies": {
    "enabledAdvancedServices": [{
      "userSymbol": "Sheets",
      "serviceId": "sheets",
      "version": "v4"
    }]
  },
  "exceptionLogging": "STACKDRIVER",
  "runtimeVersion": "V8",
  "oauthScopes": [
        "https://www.googleapis.com/auth/script.external_request",
        "https://www.googleapis.com/auth/spreadsheets.currentonly",
        "https://www.googleapis.com/auth/spreadsheets"
  ]
}
""".strip()

BOUND_SCRIPT_ID = "1iWTABHzaYGcv6VoH5CaxUEFD7NZLF5EMT0-_cbYo2iQEkiUG0pojNIvR" 

def main():
  """Calls the Apps Script API."""
  creds = None
  # The file token.json stores the user's access and refresh tokens, and is
  # created automatically when the authorization flow completes for the first
  # time.
  if os.path.exists("token.json"):
    creds = Credentials.from_authorized_user_file("token.json", SCOPES)
  # If there are no (valid) credentials available, let the user log in.
  if not creds or not creds.valid:
    if creds and creds.expired and creds.refresh_token:
      creds.refresh(Request())
    else:
      flow = InstalledAppFlow.from_client_secrets_file(
          "./client_secret_desktop.json", SCOPES
      )
      creds = flow.run_local_server(port=0)
    # Save the credentials for the next run
    with open("token.json", "w") as token:
      token.write(creds.to_json())

  try:
    service = build("script", "v1", credentials=creds)

    # Call the Apps Script API
    # Create a new project
    # request = {"title": "My Script"}
    # response = service.projects().create(body=request).execute()

    # Upload two files to the project
    request = {
        "files": [
            {"name": "Code", "type": "SERVER_JS", "source": SAMPLE_CODE},
            {
                "name": "appsscript",
                "type": "JSON",
                "source": SAMPLE_MANIFEST,
            },
        ]
    }
    response = (
        service.projects()
        .updateContent(body=request, scriptId=BOUND_SCRIPT_ID)
        .execute()
    )
    print("https://script.google.com/d/" + response["scriptId"] + "/edit")
  except errors.HttpError as error:
    # The API encountered a problem.
    print(error.content)


if __name__ == "__main__":
  main()
