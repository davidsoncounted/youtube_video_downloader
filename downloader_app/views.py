from django.shortcuts import render
from pytubefix import YouTube
from django.http import HttpResponse
import os
from urllib.error import HTTPError, URLError
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
# Create your views here.

from django.shortcuts import render
from googleapiclient.discovery import build
from urllib.parse import urlparse, parse_qs

API_KEY = 'YOUR_YOUTUBE_API_KEY'

def fetch_video_details(request):
    video_data = None
    error_message = None

    if request.method == 'POST':
        video_url = request.POST.get('video_url')
        
        # Extract the video ID from the URL
        video_id = parse_qs(urlparse(video_url).query).get('v')
        if video_id:
            video_id = video_id[0]
            try:
                youtube = build('youtube', 'v3', developerKey=API_KEY)
                request = youtube.videos().list(part='snippet', id=video_id)
                response = request.execute()

                if response['items']:
                    video = response['items'][0]['snippet']
                    video_data = {
                        'title': video['title'],
                        'description': video['description'],
                        'thumbnail_url': video['thumbnails']['high']['url'],
                        'video_url': video_url,
                    }
                else:
                    error_message = "Video not found."
            except Exception as e:
                error_message = str(e)
        else:
            error_message = "Invalid YouTube URL."

    return render(request, 'index.html', {'video_data': video_data, 'error_message': error_message})



def index(request):
    if request.method == 'POST':
        video_url = request.POST.get('text-url')
        if video_url:
            try: 
                yt = YouTube(video_url)
                stream = yt.streams.filter(progressive= True, file_extension='mp4').first()
                file_path = stream.download()
                messages.success(request, 'download successfull')

                with open(file_path, 'rb') as f:
                    response = HttpResponse(f.read(), content_type ='video/mp4')
                    response['Content-Disposition'] = f'attachment; filename="{yt.title}.mp4"'
                    os.remove(file_path)
                    return response
            except Exception as e:
                return HttpResponse(f'Error occured: {str(e)}')

    return render(request, 'index.html') 


def video_converter(request):

    return render(request, 'vid-converter.html')


