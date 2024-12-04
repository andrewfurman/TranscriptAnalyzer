# analyze_transcript_gpt.py

# The analyze transcript gpt function is used to extract structured information from a call center transcript between someone calling a business. This function will intake two varialbes:  Call Transcript String (required field), and addtional call info (optional field).

# The function will return JSON that is returned from ChatGPT API. IT will use the ChatGPT 4o mini model to analyze the transcript.

# The transcript analyzer should return JSON that includes the Caller info (Person calling the business, Caller Name, Caller Phone Number, Caller Email, Caller Address, Caller City, Caller State,). If any of these pieces of information are not available, then the JSON should include a value saying '🚫 Not Provided'.  The output should also include call infromation, call duration, call type, call status, call notes, call resolution, call resolution notes, call resolution date, call resolution time. The first field in the response should be type of call (home booking, sales call, etc.). The second field should be a field saying 'Sale_Made', which should be a boolean value. The third field should be a field explaining the sale_status_explination, this should be an explination of how we know that the sale was made, or not made.)


import os
import json
from openai import OpenAI

client = OpenAI(api_key=os.environ['OPENAI_API_KEY'])

def analyze_transcript_gpt(transcript_string, additional_call_info=None):
    payload = {
        "model": "gpt-4o-mini",
        "messages": [
            {
                "role": "system",
                "content": "You are an assistant that analyzes call center transcripts to extract key information about the interaction. Provide detailed analysis of caller information and call outcomes."
            },
            {
                "role": "user",
                "content": f"Analyze this call transcript: {transcript_string}\nAdditional Info: {additional_call_info if additional_call_info else 'None provided'}"
            }
        ],
        "response_format": {
            "type": "json_schema",
            "json_schema": {
                "name": "call_analysis",
                "strict": True,
                "schema": {
                    "type": "object",
                    "properties": {
                        "call_analysis": {
                            "type": "object",
                            "properties": {
                                "call_type": {"type": "string"},
                                "sale_made": {"type": "boolean"},
                                "sale_status_explanation": {"type": "string"},
                                "caller_name": {"type": "string"},
                                "caller_phone": {"type": "string"},
                                "caller_email": {"type": "string"},
                                "caller_address": {"type": "string"},
                                "caller_city": {"type": "string"},
                                "caller_state": {"type": "string"},
                                "duration": {"type": "string"},
                                "status": {"type": "string"},
                                "notes": {"type": "string"},
                                "resolution": {"type": "string"},
                                "resolution_notes": {"type": "string"},
                                "resolution_date": {"type": "string"},
                                "resolution_time": {"type": "string"}
                            },
                            "required": [
                                "call_type", "sale_made", "sale_status_explanation",
                                "caller_name", "caller_phone", "caller_email",
                                "caller_address", "caller_city", "caller_state",
                                "duration", "status", "notes", "resolution",
                                "resolution_notes", "resolution_date", "resolution_time"
                            ],
                            "additionalProperties": False
                        }
                    },
                    "required": ["call_analysis"],
                    "additionalProperties": False
                }
            }
        }
    }

    response = client.chat.completions.create(**payload)
    return json.loads(response.choices[0].message.content)["call_analysis"]

if __name__ == "__main__":
    test_transcript = """Hello, this is John calling about booking a home visit..."""
    result = analyze_transcript_gpt(test_transcript)
    print(json.dumps(result, indent=2))