import os
import anthropic
from django.http import JsonResponse
from dotenv import load_dotenv
from django.views.decorators.http import require_POST
import json
from django.http import HttpResponse
from django.middleware.csrf import get_token
from django.views.decorators.csrf import ensure_csrf_cookie, csrf_protect
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import ensure_csrf_cookie, csrf_protect
from django.views.decorators.http import require_http_methods

load_dotenv()

ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")

client = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)

def test_view(request):
    print("\nDEBUG: test_view was called")
    return HttpResponse("Test view works")

@require_http_methods(["GET", "OPTIONS"])
@ensure_csrf_cookie
def get_csrf_token(request):
    if request.method == "OPTIONS":
        response = JsonResponse({})
    else:
        print("\nDEBUG: get_csrf_token view was called") 
        print("=== CSRF Token Request ===")
    
    existing_token = request.COOKIES.get('csrftoken')
    print(f"1. Existing token in request cookies: {existing_token}")
    
    if existing_token:
        token = existing_token
        print(f"2. Use existing token: {token}")
    else:
        token = get_token(request)
        print(f"2. Generated new token: {token}")

    response = JsonResponse({"csrfToken": token})

    response.set_cookie(
        'csrftoken',
        token,
        samesite='None', 
        secure=True,
        httponly=False, 
        max_age=31449600
    )

    response["Access-Control-Allow-Origin"] = "http://localhost:5173"
    response["Access-Control-Allow-Credentials"] = "true"
    response["Access-Control-Allow-Methods"] = "GET, POST, OPTIONS"
    response["Access-Control-Allow-Headers"] = "X-CSRFToken, Content-Type, X-Requested-With"
    
    
    print(f"3. Cookie token set/confirmed: {token}")
    print(f"4. Response headers: {dict(response.headers)}")
    print("=== End CSRF Token Request ===\n")
    
    return response


@require_http_methods(["POST", "OPTIONS"])
@csrf_protect
def get_claude_response(request):
    print("\n=== Claude Response Request ===")
    print(f"Request Method: {request.method}")
    
    if request.method == "OPTIONS":
        print("Handling OPTIONS request")
        response = JsonResponse({})
        response["Access-Control-Allow-Origin"] = "https://ohkaleno.netlify.app"
        response["Access-Control-Allow-Credentials"] = "true"
        response["Access-Control-Allow-Methods"] = "GET, POST, OPTIONS"
        response["Access-Control-Allow-Headers"] = "X-CSRFTOKEN, Content-Type, X-Requested-With"
        print(f"OPTIONS response headers: {dict(response.headers)}")
        return response

    print("\nPOST Request Details:")
    print(f"1. CSRF Cookie: {request.COOKIES.get('csrftoken')}")
    print(f"2a. X-CSRFTOKEN Header: {request.headers.get('X-CSRFTOKEN')}")
    print(f"2b. X-CSRFToken Header: {request.headers.get('X-CSRFToken')}")
    print(f"2c. x-csrftoken Header: {request.headers.get('x-csrftoken')}")
    print(f"3. All Headers: {dict(request.headers)}")
    print(f"4. Request META CSRF: {request.META.get('HTTP_X_CSRFTOKEN')}")
    print(f"5. All Cookies: {request.COOKIES}")
    
    try:
        body = json.loads(request.body)
        user_prompt = body.get("userPrompt", "")
        
        # response = JsonResponse({
        #     "message": f"Received user prompt: {user_prompt}"
        # })


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
        response["Access-Control-Allow-Origin"] = "http://localhost:5173"
        response["Access-Control-Allow-Credentials"] = "true"
        return response
        
    except Exception as e:
        print(f"Error in get_claude_response: {str(e)}")
        response = JsonResponse({
            "error": str(e),
            "message": "Sorry, there seems to be a veggie jam in my Ninja. Please try again later."
        })
        response["Access-Control-Allow-Origin"] = "http://localhost:5173"
        response["Access-Control-Allow-Credentials"] = "true"
        return response
