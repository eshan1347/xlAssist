# xlAssist
Tool to auto complete columns in google sheet with LLMs &amp; Web Search Engine

## Introduction 
An Intelligent & knowledgeable auto completion tool embedded into google sheets with LLM + Search agents.

## Setup 
1. Replace placeholder with your Gemini model api key in variable, api_key in the createAppScript code. 
2. Get Script ID for your Google sheet . Extensions -> App Script -> Copy URL. 
3. Add your Script ID for your Google Sheet to the runAppScript file
4. Execute `python runAppScript.py`

## Future Scope
- Develop frontend as an extension which implements all of the above functionality.
- Automate Script ID extraction from the Google sheet . Currently the Script ID is not provided by the API & randomly generated . One possible way is to generate with an autonomous agent & retrieve it.
- Improve Search results with a better search agent.
- Improve Overall Results with prompt engineering.
