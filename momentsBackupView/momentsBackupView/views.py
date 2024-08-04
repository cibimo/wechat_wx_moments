import os

from django.http.response import *
from django.shortcuts import render, redirect

import json, requests, datetime, urllib, shutil, random, string, zlib, base64, time, re

export_dir = "/Volumes/4T_RAID0/微信朋友圈自动导出"
userPosts = json.loads(open(f"{export_dir}/posts.json").read())


def userList(request):
    users = []
    for wxid in userPosts:
        users.append({
            "wxid": wxid,
            "nick": userPosts[wxid]['nickname']
        })
    return render(request, "userList.html", {"users": users})

def user(request):
    wxid = request.GET.get('wxid')
    moments = []
    for date in sorted(list(userPosts[wxid]['post']), reverse=True):
        for post in userPosts[wxid]['post'][date]:
            moment = {
                "date": f"{date[0:10]} {date[11:13]}:{date[13:15]}",
                "num": post['num'],
                "text": None,
                "url": None,
                "image": []
            }
            image = []
            for i in os.listdir(f"{export_dir}/posts/{wxid}/{date}_{post['num']}"):
                if i.endswith(".jpg"):
                    image.append(i)
                elif i == "text.txt":
                    try:
                        moment['text'] = open(f"{export_dir}/posts/{wxid}/{date}_{post['num']}/text.txt").read()
                    except:
                        pass
                elif i == "url.txt":
                    moment['url'] = open(f"{export_dir}/posts/{wxid}/{date}_{post['num']}/url.txt").read()

            for i in sorted(image):
                params = {
                    "wxid": wxid,
                    "moment": f"{date}_{post['num']}",
                    "image": i
                }
                moment['image'].append(f"/getImage?{urllib.parse.urlencode(params)}")
            moments.append(moment)
    return render(request, "user.html", {"wxid": wxid, "nick": userPosts[wxid]['nickname'], "moments": moments})

def getImage(request):
    wxid = request.GET.get('wxid')
    moment = request.GET.get('moment')
    image = request.GET.get('image')
    with open(f"{export_dir}/posts/{wxid}/{moment}/{image}", "rb") as f:
        return HttpResponse(f.read(), content_type="image/jpeg")