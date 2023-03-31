from django.shortcuts import render
from pytube import YouTube


def home(request):
    if request.method == "GET":
        return render(request, "base.html", {})

    elif request.method == "POST":
        video = request.POST["video-link"]

        youtube_object = YouTube(video)
        #youtube_object = youtube_object.streams.get_highest_resolution()
        youtube_object = youtube_object.streams.all()

        try:
            print("Downloading...")
            # youtube_object.download()
            print("Downloaded!")
        except:
            print("An error has occurred")

        print("Download is completed successfully")

        filtered_object = []
        for k in youtube_object:
            print("got -- ", k.video_codec)
            foo = {"title": k.title, "type": }
            filtered_object.append()


        return render(request, "result.html", {"video": { "link": video, "result": youtube_object }})