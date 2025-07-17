from django.utils import timezone
from django.db.models import Q
from .models import Items
from datetime import timedelta
import os

from apscheduler.schedulers.background import BackgroundScheduler

def remove():
    print("remove start")
    two_days_ago = timezone.now() - timedelta(days=2)
    old_objects = Items.objects.filter(created__lt=two_days_ago).exclude(status__icontains="removed")

    for objects in old_objects:
        try:
            id = str(objects.id)
            os.remove(f"./js/progress/{id}.txt")
        except:
            pass
        if objects.img:
            img = "./media/"+str(objects.img)
            try:
                os.remove(img)
            except:
                pass
        if objects.img_back_none:
            img_back_none = "./media/"+str(objects.img_back_none)
            try:
                os.remove(img_back_none)
            except:
                pass
        if objects.video:
            video = "./media/"+str(objects.video)
            try:
                os.remove(video)
            except:
                pass

        objects.status = "removed"
        objects.save()
        print(str(objects.id)+" removed")

    print("remove end")

def reset():#鯖起動時に実行
    print("reset start")
    error_objects = Items.objects.filter(Q(status="generating") | Q(status="waiting") | Q(status="unstarted"))

    for objects in error_objects:
        try:
            id = str(objects.id)
            os.remove(f"static/after/js/progress/{id}.txt")
        except:
            pass
        if objects.img:
            img = "./media/"+str(objects.img)
            try:
                os.remove(img)
            except:
                pass
        if objects.img_back_none:
            img_back_none = "./media/"+str(objects.img_back_none)
            try:
                os.remove(img_back_none)
            except:
                pass
        if objects.video:
            video = "./media/"+str(objects.video)
            try:
                os.remove(video)
            except:
                pass
        objects.status = "error"
        objects.save()
        print(str(objects.id)+" removed for error")

    print("reset end")


def start():
    scheduler = BackgroundScheduler()
    scheduler.add_job(remove, "interval", days=2)
    scheduler.start()
