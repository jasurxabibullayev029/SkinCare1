import os
import openai
from django.conf import settings

# Test OpenAI API connection
def test_openai_api():
    api_key = getattr(settings, 'OPENAI_API_KEY', None)

    if not api_key or api_key == 'your-openai-api-key-here':
        print("❌ OpenAI API key not configured")
        return False

    print(f"✅ API key found: {api_key[:20]}...")

    try:
        openai.api_key = api_key
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": "Hello"}],
            max_tokens=10
        )
        print("✅ OpenAI API working correctly")
        return True
    except Exception as e:
        print(f"❌ OpenAI API error: {str(e)}")
        return False

if __name__ == "__main__":
    print("Testing OpenAI API connection...")
    test_openai_api()
