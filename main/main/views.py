from django.shortcuts import render, redirect, get_object_or_404
from django.http import FileResponse, HttpResponse, HttpResponseNotFound, HttpResponseRedirect


# from starlette.responses import FileResponse

from pytube import YouTube
import os

BASE_DIR = os.path.dirname(os.path.dirname(__file__))


def download(request, test=None):
    print("test in DOWNLOAD --- ", request.args['test'])
    #video = get_object_or_404(Video, pk=pk)
    print("base ", BASE_DIR)
    video = {
        "path": f'{BASE_DIR}/The USD is Finished.mp4',
        "title": 'The USD is Finished.mp4'
    }
    response = FileResponse(open(video["path"], 'rb'), content_type='video/mp4')
    response['Content-Disposition'] = f'attachment; filename="{video["title"]}"'
    return response


def send_file(file_path, file_name, video_object):
    status = video_object.download(skip_existing=True)
    return status
   

def home(request):
    if request.method == "GET":
        return render(request, "base.html", {})

    elif request.method == "POST":
        video = request.POST["video-link"]

        youtube_object = YouTube(video)
        # youtube_object = youtube_object.streams.filter(file_extension='mp4')
        youtube_object = youtube_object.streams.filter(progressive=True)


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

                for k in filtered_object:
                    if k["full_type"] == selected_video:
                        print("full name ", k["full_name"])
                        # k["full"].download()

                        # send_file(k["full_name"])
                        #k["full"].download()

                        # print("full path ", k["full_path"])
                        download_status = send_file(
                            file_path=k["full_path"], 
                            file_name=k["full_name"],
                            video_object=k["full"]
                        )
                        if download_status:
                            response = redirect('download/', test="hello")
                            print("response of redirect ", response)
                            return response

        except:
            pass

        return render(request, "result.html", {"video": {"link": video, "result": filtered_object}})
