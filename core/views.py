import os
import anthropic
from django.http import JsonResponse, HttpResponse
import json
from django.middleware.csrf import get_token
from django.views.decorators.csrf import ensure_csrf_cookie, csrf_protect
from django.views.decorators.http import require_http_methods

ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")

client = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)

@ensure_csrf_cookie
def get_csrf_token(request):
    print("\n=== CSRF Token Request ===")
    print(f"Origin header: {request.headers.get('Origin')}")
    print(f"Cookie token: {request.COOKIES.get('csrftoken')}")
    print(f"CSRF Token in header: {request.headers.get('X-CSRFToken')}")
    
    token = get_token(request)
    response = JsonResponse({})

    # Set the same token in both cookie and header
    response['X-CSRFToken'] = token
    
    # Handle CORS headers
    origin = request.headers.get('Origin')
    if origin:
        response["Access-Control-Allow-Origin"] = origin
        response["Access-Control-Allow-Credentials"] = "true"
        response["Access-Control-Allow-Methods"] = "GET, POST, OPTIONS"
        response["Access-Control-Allow-Headers"] = "X-CSRFToken, Content-Type, X-Requested-With"
        response["Access-Control-Expose-Headers"] = "Content-Type, X-CSRFToken"
    
    print("=== End CSRF Token Request ===\n")
    return response

@csrf_protect
@require_http_methods(["POST", "OPTIONS"])
def get_claude_response(request):
    print("\n=== Claude Response Request ===")
    print(f"Request method: {request.method}")
    print(f"All headers: {dict(request.headers)}")
    print(f"All cookies: {request.COOKIES}")
    print(f"CSRF Token in header: {request.headers.get('X-CSRFToken')}")
    print(f"CSRF Token in cookie: {request.COOKIES.get('csrftoken')}")
    print(f"CSRF Token in META: {request.META.get('HTTP_X_CSRFTOKEN')}")
    print(f"Content type: {request.headers.get('Content-Type')}")
    print("=== End Claude Response Request ===\n")
    
    if request.method == "OPTIONS":
        print("*** Handling OPTIONS request ***")
        response = JsonResponse({})

        origin = request.headers.get('Origin')
        print(f"Origin header: {origin}")

        if origin:
            response["Access-Control-Allow-Origin"] = origin
            print(f"Matched allowed origin: {origin}")
        else:
            response["Access-Control-Allow-Origin"] = "http://localhost:5173"
        response["Access-Control-Allow-Credentials"] = "true"
        response["Access-Control-Allow-Methods"] = "GET, POST, OPTIONS"
        response["Access-Control-Allow-Headers"] = "X-CSRFToken, Content-Type, X-Requested-With"
        print(f"OPTIONS response headers: {dict(response.headers)}")
        return response

    try:
        body = json.loads(request.body)
        user_prompt = body.get("userPrompt", "")
        print(f"Received prompt: {user_prompt}")

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
