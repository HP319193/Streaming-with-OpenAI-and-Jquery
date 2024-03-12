from django.shortcuts import render
from django.http import StreamingHttpResponse
from openai import OpenAI
from django.views.decorators.csrf import csrf_protect
from dotenv import load_dotenv
import os

load_dotenv()

client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
def index(request):
    return render(request, "index.html")

def generate(query):
    for chunk in client.chat.completions.create(
            model='gpt-3.5-turbo',
            messages=[
                {'role': 'user', 'content': query}
            ],
            temperature=0,
            stream=True 
        ):
            content = chunk.choices[0].delta.content
            if content is not None: 
                yield content
                
@csrf_protect
def message(request):
    query = request.POST.get("query")
    response = StreamingHttpResponse(generate(query), content_type='text/event-stream')
    return response
