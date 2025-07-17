from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.http import Http404, HttpResponse, JsonResponse
from django.urls import reverse
from django.forms.models import model_to_dict
from datetime import datetime
from zoneinfo import ZoneInfo

from .forms import ItemsForm
from .models import Items
from .generate import handler
import threading
import uuid
import json
import base64

class IndexView(View):
    def get(self,request):
        datetime_now = datetime.now(ZoneInfo("Asia/Tokyo")).strftime("%Y/%m/%d %H:%M:%S")
        form = ItemsForm()
        return render(request, "after/index.html", {"datetime_now" : datetime_now, "form":form})

    def post(self,request):
        form = ItemsForm(request.POST, request.FILES)
        if form.is_valid():
            objects = form.save()

            file_name = str(objects.video)[12:-4]
            progress_path = "./static/after/js/progress/" + str(objects.id) + ".txt"
            img_path = "./media/after/img/" + str(objects.id) + ".png"
            img_path_shadow = "./media/after/img/" + str(objects.id) + "_shadow" + ".png"

            data = {"img" : img_path[8:], "img_back_none" : img_path_shadow[8:]}
            Items.objects.filter(pk=objects.id).update(**data)
            with open(progress_path, "w", encoding='utf-8') as f:
                f.write("0.00")

            objects = get_object_or_404(Items, id=objects.id)
            thread = threading.Thread(target=handler, args=(objects,))
            thread.start()

            request.session[str(objects.id)] = objects.pin
            return  redirect("after:result", objects.id)
        else:
            return redirect("after:index")

class LoginView(View):
    def get(self,request):
        return render(request, "after/login.html")

    def post(self,request,*args,**kwargs):
        try:
            id = request.POST["id"]
            pin = int(request.POST["pin"])
            objects = get_object_or_404(Items, id=id)
        except:
            raise Http404

        if objects.pin == pin:
            if objects.status=="removed":
                text = {
                    "id": str(objects.id),
                    "title": "削除済み",
                    "info":"指定のデータは2日が経過したため削除されました。"
                }
                return render(request, "after/removed.html", {"text":text})
            if objects.status=="error":
                text = {
                    "id": str(objects.id),
                    "title": "エラー",
                    "info":"指定のデータはエラーが発生したため生成が中断されました。"
                }
                return render(request, "after/removed.html", {"text":text})
            if objects.status=="timeout":
                text = {
                    "id": str(objects.id),
                    "title": "エラー",
                    "info":"指定のデータは生成中にタイムアウトしました。"
                }
                return render(request, "after/removed.html", {"text":text})
            request.session[str(objects.id)] = objects.pin
            return  redirect("after:result", objects.id)
        else:
            raise Http404

class ResultView(View):
    def get(self,request,id):
        referer = request.META.get("HTTP_REFERER")
        index_referer = request.build_absolute_uri(reverse("after:index"))
        login_referer = request.build_absolute_uri(reverse("after:login"))

        if not referer:
            return redirect("after:index")
        if not referer.startswith(index_referer) and not referer.startswith(login_referer):
            return redirect("after:index")
        else:
            objects = get_object_or_404(Items, id=id)
            pin = request.session.get(str(id), None)
            if pin == objects.pin:
                if objects.status == "removed":
                    return render(request, "after/removed.html", {"objects":objects})
                if objects.status == "error":
                    return render(request, "after/removed.html", {"objects":objects})
                return render(request, "after/result.html", {"objects":objects})
            else:
                return redirect("after:index")


class ProgressView(View):
    def post(self,request):
        #memo:http://127.0.0.1:8000/after/result/a2c0c652-f244-4665-99ff-56bef8b00bbf/
        body = json.loads(request.body)
        pin = request.session.get(body, None)
        objects = get_object_or_404(Items, id=uuid.UUID(body))

        if pin == objects.pin:
            path = "static/after/js/progress/" + body + ".txt"#画像のIDを受け取って適切なパスを作成
            with open(path) as f:
                progress_now = f.read()
            return HttpResponse(progress_now)
        else:
            return redirect("after:index")

class ImgView(View):
    def post(self,request):
        body = json.loads(request.body.decode("utf-8"))
        purpose = body.get("purpose")
        id = body.get("id")

        if purpose == "example":
            path = "./media/after/src/example.png"
            with open(path, "rb") as f:
                encoded_img = base64.b64encode(f.read()).decode('utf-8')
            return JsonResponse({"img_base64": encoded_img})

        if purpose == "waiting":
            path = "./media/after/src/waiting.png"
            with open(path, "rb") as f:
                encoded_img = base64.b64encode(f.read()).decode('utf-8')
            return JsonResponse({"img_base64": encoded_img})

        if purpose == "progressing":
            path = "./media/after/src/progressing.png"
            with open(path, "rb") as f:
                encoded_img = base64.b64encode(f.read()).decode('utf-8')
            return JsonResponse({"img_base64": encoded_img})

        if purpose == "result":
            pin = request.session.get(id, None)
            objects = get_object_or_404(Items, id=uuid.UUID(id))
            if pin == objects.pin:
                path = "./media/after/img/" + id + ".png"
                with open(path, "rb") as f:
                    encoded_img = base64.b64encode(f.read()).decode('utf-8')
                return JsonResponse({"img_base64": encoded_img})
            else:
                return redirect("after:index")

class GitView(View):
    def get(self,request):
        return render(request, "after/git_link.html")

index = IndexView.as_view()
login = LoginView.as_view()
result = ResultView.as_view()
progress = ProgressView.as_view()
img = ImgView.as_view()
git_link = GitView.as_view()
