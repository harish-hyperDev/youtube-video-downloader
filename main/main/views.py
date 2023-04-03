from django.shortcuts import render
from starlette.responses import FileResponse

from pytube import YouTube


def send_file(file_path, file_name):
    return FileResponse(
        path = file_path,
        media_type = 'application/octet-stream',
        filename = file_name
    )


def home(request):
    if request.method == "GET":
        return render(request, "base.html", {})

    elif request.method == "POST":
        video = request.POST["video-link"]

        youtube_object = YouTube(video)
        youtube_object = youtube_object.streams.filter(file_extension='mp4')

        filtered_object = []
        for k in youtube_object:

            try:
                # print("res ", k)

                foo = {
                    "title": k.title,
                    "type": k.mime_type.split('/')[0],
                    "full_type": k.mime_type.split('/')[0] + "/" + k.resolution + " - " + str(k.filesize_mb) + " MB",
                    "format": k.mime_type.split('/')[1],
                    "index": youtube_object.index(k),
                    "full": k,
                    "full_name": k.get_file_path().split('/')[len(k.get_file_path().split('/')) - 1],
                    "full_path": k.get_file_path(),
                }
                filtered_object.append(foo)

            except:
                pass

        try:
            if request.POST["video-index"]:
                selected_video = request.POST["video-index"]
                print(selected_video)

                for k in filtered_object:
                    if k["full_type"] == selected_video:
                        print("full name ", k["full_name"])
                        print("Downloading...")
                        k["full"].download()
                        print("Downloaded!")
                        # send_file(k["full_name"])
                        # k["full"].download()

                        send_file(file_path=k["full_path"], file_name=k["full_name"])
                        print("file sent")



        except:
            pass

        return render(request, "result.html", {"video": {"link": video, "result": filtered_object}})
