import os
import anthropic
from django.http import JsonResponse
import json
from django.middleware.csrf import get_token
from django.views.decorators.csrf import ensure_csrf_cookie, csrf_protect
from django.views.decorators.csrf import ensure_csrf_cookie, csrf_protect
from django.views.decorators.http import require_http_methods

ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")

client = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)

@ensure_csrf_cookie
def get_csrf_token(request):
    print("=== CSRF Token Request ===")
    token = get_token(request)

    response = JsonResponse({"csrfToken": token})
    response.set_cookie(
        'csrftoken', 
        token, 
        samesite='None', 
        secure=True,
        httponly=False, 
        max_age=31449600
    )

    response["Access-Control-Allow-Origin"] = "https://ohkaleno.netlify.app"
    response["Access-Control-Allow-Credentials"] = "true"
    response["Access-Control-Allow-Methods"] = "GET, POST, OPTIONS"
    response["Access-Control-Allow-Headers"] = "X-CSRFToken, Content-Type, X-Requested-With"
    
    
    print(f"3. Cookie token set/confirmed: {token}")
    print(f"4. Response headers: {dict(response.headers)}")
    print("=== End CSRF Token Request ===\n")

    
    print(f"Response headers: {dict(response.headers)}")
    return response

@csrf_protect
@require_http_methods(["POST"])
def get_claude_response(request):
    print("\n=== Claude Response Request ===")

    try:
        body = json.loads(request.body)
        user_prompt = body.get("userPrompt", "")

        # Provided by Get Code button in Anthropic Workbench
        response = client.messages.create(
            model="claude-3-5-sonnet-20241022",
            max_tokens=1000,
            temperature=0,
            system=(
                "The user is interacting with you to customize a healthy to-do list in an app named 'oh, kale no!'. "
                "The app to-do list includes but is not limited to:\n"
                "- ate something green\n"
                "- held space for my own emotion\n"
                "- held space for someone else's emotion\n"
                "- moved my body for 30 minutes\n"
                "- built my relationship with curiosity\n"
                "- spent time with someone\n"
                "- went outside and made peace with the weather\n"
                "- verbally expressed gratitude\n\n"
                "The user will be asked: 'Hey there, what would you like to focus on today?'\n\n"
                "You are a coach focused on promoting productive, healthy, and mindful habits. "
                "You will respond in friendly, supportive short answers (3-4 sentences max) suggesting custom actions "
                "they can take to achieve the prompt. You will use vegetable (or avocado) puns when possible. "
                "Your voice is gender neutral or slightly feminine, millennial generation, and empathetic. "
                "You lean slightly liberal with preferences toward natural medicine, but you do not give advice or engage "
                "in ways that overtly pronounce those beliefs. You encourage individuals to succeed in mentally, emotionally, "
                "and physically healthy, safe, and fun activities and to 'tend toward action' versus procrastinating or "
                "dwelling in negativity. You believe in community over isolation, biblical generosity over selfishness, "
                "and curiosity over judgment."
            ),
            messages=[
                {
                    "role": "user",
                    "content": user_prompt
                }
            ]
        )

        # Extract the text content from the TextBlock object
        if hasattr(response, "content") and isinstance(response.content, list):
            message_text = response.content[0].text if response.content else "No valid content received from Claude."
        else:
            message_text = "No valid content received from Claude."

        # Return the message in a JSON-serializable format
        response = JsonResponse({"message": message_text})

        return response
        
    except Exception as e:
        print(f"Error in get_claude_response: {str(e)}")
        response = JsonResponse({
            "error": str(e),
            "message": "Sorry, there seems to be a veggie jam in my Ninja. Please try again later."
        })
        return response
