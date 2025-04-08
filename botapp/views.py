from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from twilio.twiml.messaging_response import MessagingResponse
import requests
import os
import json
from dotenv import load_dotenv

load_dotenv()

# Doctor persona instructions
DOCTOR_CONTEXT = """
You are Dr. HealthBot, an AI medical assistant with expertise in general medicine.
Your role is to provide helpful, accurate, and compassionate medical information while
being careful not to replace professional medical advice.

Guidelines for your responses:
1. Always be polite and empathetic
2. Provide information in clear, simple terms
3. When discussing symptoms, always recommend consulting a real doctor for serious concerns
4. Never diagnose serious conditions - suggest possibilities but emphasize the need for professional evaluation
5. For medication questions, remind users to consult their physician before taking anything
6. Keep responses concise but thorough (1-3 short paragraphs max)

The user's message follows. Please respond as Dr. HealthBot:
"""

@csrf_exempt
def whatsapp_bot(request):
    if request.method == "POST":
        incoming_msg = request.POST.get("Body", "").strip()
        resp = MessagingResponse()
        msg = resp.message()

        # Load API key
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            msg.body("Gemini API key not configured properly.")
            return HttpResponse(str(resp), content_type='application/xml')

        # Prepare the prompt with doctor context
        prompt = f"{DOCTOR_CONTEXT}\n\nPatient: {incoming_msg}\n\nDr. HealthBot:"

        headers = {
            "Content-Type": "application/json"
        }

        payload = {
            "contents": [{
                "role": "user",
                "parts": [{"text": prompt}]
            }],
            "generationConfig": {
                "temperature": 0.5,
                "maxOutputTokens": 800
            }
        }

        # Using the more stable Gemini 1.5 Flash model
        gemini_url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={api_key}"

        try:
            r = requests.post(gemini_url, headers=headers, json=payload, timeout=15)
            r.raise_for_status()
            data = r.json()

            # Debugging: Print the full response
            print("Full API response:", json.dumps(data, indent=2))

            # Safely extract Gemini's response
            if 'candidates' in data and data['candidates']:
                candidate = data['candidates'][0]
                if 'content' in candidate and 'parts' in candidate['content']:
                    reply = candidate['content']['parts'][0].get('text', '')

                    if reply:
                        # Clean up the response
                        cleaned_reply = reply.replace("Dr. HealthBot:", "").strip()
                        msg.body(cleaned_reply[:1600])  # WhatsApp message length limit
                    else:
                        msg.body("I couldn't generate a response. Please try rephrasing your question.")
                else:
                    msg.body("Unexpected response format from the AI service.")
            else:
                # Check for blocked content or errors
                if 'promptFeedback' in data and 'blockReason' in data['promptFeedback']:
                    msg.body("I can't respond to that question due to safety restrictions.")
                else:
                    msg.body("The AI service didn't return a valid response. Please try again.")

        except requests.exceptions.Timeout:
            msg.body("I'm currently busy with other patients. Please try again shortly.")
        except requests.exceptions.HTTPError as e:
            print("HTTP Error:", e.response.text)
            msg.body("There was an error processing your request. Please try again later.")
        except Exception as e:
            print("Error:", str(e))
            msg.body("Sorry! I'm experiencing technical difficulties. For medical emergencies, please contact emergency services.")

        return HttpResponse(str(resp), content_type='application/xml')

    return HttpResponse("Only POST requests allowed.", status=405)