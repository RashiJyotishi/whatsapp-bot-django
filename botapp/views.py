from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from twilio.twiml.messaging_response import MessagingResponse
import requests
import os
# At top of views.py or apps.py
from dotenv import load_dotenv
load_dotenv()


@csrf_exempt
def whatsapp_bot(request):
    if request.method == "POST":
        incoming_msg = request.POST.get("Body", "").strip()
        resp = MessagingResponse()
        msg = resp.message()

        # Load API key
        api_key = os.getenv("GEMINI_API_KEY")
        print(os.getenv("GEMINI_API_KEY"))
        if not api_key:
            msg.body("Gemini API key not configured properly.")
            return HttpResponse(str(resp), content_type='application/xml')

        headers = {
            "Content-Type": "application/json"
        }

        payload = {
            "contents": [
                {
                    "parts": [
                        {"text": incoming_msg}
                    ]
                }
            ]
        }

        gemini_url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={api_key}"

        try:
            r = requests.post(gemini_url, headers=headers, json=payload, timeout=10)
            r.raise_for_status()
            data = r.json()

            # Safely extract Gemini's response
            reply = data.get("candidates", [{}])[0].get("content", {}).get("parts", [{}])[0].get("text", "")
            if reply:
                msg.body(reply)
            else:
                msg.body("Gemini did not return a valid response.")

        except Exception as e:
            print("Error:", e)
            msg.body("Sorry! Couldn't get a response from Gemini right now.")

        return HttpResponse(str(resp), content_type='application/xml')

    return HttpResponse("Only POST requests allowed.", status=405)
