from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from pytube import YouTube
import json
from django.conf import settings
import os
import assemblyai as aai
from openai import OpenAI
from .models import BlogPost


# Create your views here.
@login_required
def index(request):
    return render(request, "index.html")


def blog_list(request):
    blog_articles = BlogPost.objects.filter(user=request.user)
    return render(request, "all-blogs.html", {"blog_articles": blog_articles})


def blog_details(request, pk):
    blog_article_detail = BlogPost.objects.get(id=pk)
    if request.user == blog_article_detail.user:
        return render(
            request, "blog-details.html", {"blog_article_detail": blog_article_detail}
        )
    else:
        return redirect("/")


def user_login(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect("/")
        else:
            return render(request, "login.html", {"error": "Invalid credentials"})
    return render(request, "login.html")


def user_signup(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]
        password = request.POST["password"]
        repeatPassword = request.POST["repeatPassword"]
        if password != repeatPassword:
            return render(request, "signup.html", {"error": "Passwords do not match"})
        else:
            try:
                user = User.objects.create_user(
                    username=username, email=email, password=password
                )
                user.save()
                login(request, user)
                return redirect("/")
            except Exception as e:
                return render(request, "signup.html", {"error": str(e)})
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect("login")
    return render(request, "signup.html")


def user_logout(request):
    logout(request)
    return redirect("/")


def yt_title(link):
    yt = YouTube(link)
    title = yt.title
    return title


def download_audio(link):
    yt = YouTube(link)
    video = yt.streams.filter(only_audio=True).first()
    out_file = video.download(output_path=settings.MEDIA_ROOT)
    base, ext = os.path.splitext(out_file)
    new_file = base + ".mp3"
    os.rename(out_file, new_file)
    return new_file


def get_transcription(link):
    audio_file = download_audio(link)
    try:
        aai.settings.api_key = os.getenv("ASSEMBLYAI_API_KEY")
        transcriber = aai.Transcriber()
        transcript = transcriber.transcribe(audio_file)
        return transcript.text
    finally:
        # Ensure the audio file is deleted
        if os.path.exists(audio_file):
            os.remove(audio_file)


def generate_blog_from_transcription(transcription):

    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    completion = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a blog expert"},
            {
                "role": "user",
                "content": "Generate a blog post from the following transcription: "
                + transcription,
            },
        ],
    )

    return completion.choices[0].message.content


@csrf_exempt
def generate_blog(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            yt_link = data["link"]
        except (KeyError, json.JSONDecodeError):
            return JsonResponse({"error": "Invalid data sent"}, status=400)

        # get yt title
        title = yt_title(yt_link)

        # get transcript
        transcription = get_transcription(yt_link)
        if not transcription:
            return JsonResponse({"error": " Failed to get transcript"}, status=500)

        # use OpenAI to generate the blog
        blog_content = generate_blog_from_transcription(transcription)
        if not blog_content:
            return JsonResponse(
                {"error": " Failed to generate blog article"}, status=500
            )

        # save blog article to database
        new_blog_article = BlogPost.objects.create(
            user=request.user,
            youtube_title=title,
            youtube_link=yt_link,
            generated_content=blog_content,
        )
        new_blog_article.save()

        # return blog article as a response
        return JsonResponse({"content": blog_content})
    else:
        return JsonResponse({"error": "Invalid request method"}, status=405)
