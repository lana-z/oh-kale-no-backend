import os
import anthropic
from django.http import JsonResponse
from django.middleware.csrf import get_token
from django.views.decorators.csrf import ensure_csrf_cookie, csrf_protect
from django.views.decorators.http import require_http_methods
from .models import VisitCounter

ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")

@ensure_csrf_cookie
def get_csrf_token(request):
    return JsonResponse({'csrfToken': get_token(request)})

@csrf_protect
@require_http_methods(["POST"])
def get_claude_response(request):
    try:
        user_input = request.POST.get('user_input', '')
        client = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)
        
        message = client.messages.create(
            model="claude-3-sonnet-20240229",
            max_tokens=1024,
            temperature=0.7,
            system="You are a friendly wellness coach who speaks in vegetable puns. Keep responses brief and playful.",
            messages=[{"role": "user", "content": user_input}]
        )
        
        return JsonResponse({
            'message': message.content[0].text
        })
    except Exception:
        return JsonResponse({
            'message': "Let's take a fresh approach - like a crisp lettuce leaf!"
        }, status=500)

def get_visit_count(request):
    try:
        counter = VisitCounter.objects.first()
        count = counter.count if counter else 0
        return JsonResponse({'count': count})
    except Exception:
        return JsonResponse({'count': 0})

@require_http_methods(["POST"])
def increment_visit_count(request):
    try:
        count = VisitCounter.increment()
        return JsonResponse({'count': count})
    except Exception:
        return JsonResponse({'count': 0})
