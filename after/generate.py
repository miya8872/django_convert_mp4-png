from .models import Items
from datetime import datetime
import cv2
import os
import threading
import time

class Generate():
    def __init__(self,objects):
        #保存pathの設定
        self.id = objects.id
        self.video_path = "./media/after" + str(objects.video)[5:]
        self.img_path = "./media/after/img/" + str(objects.id) + ".png"
        self.img_path_shadow = "./media/after/img/" + str(objects.id) + "_shadow" + ".png"
        self.progress_path = "./static/after/js/progress/" + str(objects.id) + ".txt"
        self.video_data = cv2.VideoCapture(self.video_path)
        self.timeout = 900

        #設定項目の初期化
        self.setting = {
            "frame" : 2, #frame : 何フレーム毎か
            "sensitivity" : 120, #sensitivity : センシ
            "save_only" : True, #save_only : 背景無しを保存するか
            "back" : 0.5, #back : 合成時の背景の割合
            "shadow" : 0.5 #shadow : 合成時の残像の割合
        }

        if self.setting["frame"] == 0:#フレーム頻度の自動設定
            video_frame = int(self.video_data.get(cv2.CAP_PROP_FRAME_COUNT))
            try:
                self.setting["frame"] = round(float(video_frame/50))
                if self.setting["frame"]==0:
                    self.setting["frame"] = 1
            except:
                self.setting["frame"] = 1

    def save(self,blended,shad):
        cv2.imwrite(self.img_path, blended)
        cv2.imwrite(self.img_path_shadow, shad)
        with open(self.progress_path, "w", encoding="utf-8") as f:
            f.write("100.00")

    def generate(self):
        n = 0
        x = 0
        i = 0
        l = 0
        prec = 0
        pre1 = []
        pre2 = []
        video_frame = int(self.video_data.get(cv2.CAP_PROP_FRAME_COUNT))
        start_time = time.time()
        while(True):
            n += 1
            if n/video_frame < 1.0:
                with open(self.progress_path, "w", encoding='utf-8') as f:
                    f.write(str("{:.2f}".format((n / video_frame) * 100)))
                    print(str(self.id)+":"+str("{:.2%}".format(n/video_frame)))
            if time.time() - start_time > self.timeout:
                raise TimeoutError
            ret, src = self.video_data.read()
            if not ret:
                break

            if n == 1:#初期設定
                first = src
                if first.ndim == 3:  # RGBならアルファチャンネル追加
                    first = cv2.cvtColor(first, cv2.COLOR_RGB2RGBA)
                first_copy = first.copy()
                h, w, c = first.shape
                h = h - 1
                w = w - 1

                i = 0
                l = 0#白紙画像の作成
                shad = first.copy()
                while(i<h):
                    i += 1
                    l = 0
                    while(l<w):
                        l += 1
                        shad[i,l] = [0,0,0,0]

                i = 0
                l = 0#pre作成
                while(i<h):
                    i += 1
                    l = 0
                    while(l<w):
                        l += 1
                        pre1.append(0)
                        pre2.append(0)

        #nfの値で何フレーム毎か指定
            else:#画像処理
                if 0 == n%self.setting["frame"]:
                    x += 1
                    img = src
                    if src.ndim == 3:
                        img = cv2.cvtColor(src, cv2.COLOR_RGB2RGBA)
                    diff = cv2.absdiff(first, img)

                    i = 0
                    l = 0
                    prec = -1
                    while(i<h):
                        if x == 1:
                            break
                        i += 1
                        l = 0
                        while(l<w):
                            prec += 1
                            l += 1
                            if 0 == x%2:
                                pre2[prec] = 0
                            else:
                                pre1[prec] = 0
                            pixelValue = diff[i,l]
                            b, g, r , a = pixelValue
                            sam = b + g + r

                            if sam >= self.setting["sensitivity"]:
                                if 0 == x%2:
                                    if pre1[prec] == 0:
                                        shad[i,l] = img[i,l]
                                        pre2[prec] = 1
                                else:
                                    if pre2[prec] == 0:
                                        shad[i,l] = img[i,l]
                                        pre1[prec] = 1

                    first = img.copy()

        blended = cv2.addWeighted(src1=first_copy,alpha=self.setting["back"],src2=shad,beta=self.setting["shadow"],gamma=0)
        self.save(blended,shad)

def handler(objects):
    running_list = list(Items.objects.filter(status="generating"))
    obj = Generate(objects)
    first = True
    while len(running_list)>2:
        if first:
            first = False
            with open(obj.progress_path, "w", encoding='utf-8') as f:
                f.write("-1.00")
                print(str(obj.id)+" is waiting")
        time.sleep(2)
        running_list = list(Items.objects.filter(status="generating"))

    objects.status = "generating"
    objects.save()
    try:
        obj.generate()
        objects.status = "generated"
        objects.save()
        print("--------------------------------")
        print(str(objects.id) + " is generated")
        print("--------------------------------")
    except TimeoutError as e:
        objects.status = "timeout"
        objects.save()
        print("--------------------------------")
        print(str(objects.id) + " is timeout")
        print("--------------------------------")
    except Exception as e:
        objects.status = "error"
        objects.save()
        print("--------------------------------")
        print(str(objects.id) + " is error")
        print(e)
        print("--------------------------------")
