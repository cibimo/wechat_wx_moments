import os, re, json
import tarfile, shutil

import_dirs = [
    '/Users/xxx/xxx/moments'
]

export_dir = "/Volumes/4T_RAID0/微信朋友圈自动导出"

if os.path.exists(f"{export_dir}/posts.json"): # 读取数据库
    userPosts = json.loads(open(f"{export_dir}/posts.json").read())
else:
    userPosts = {}

# tar_file = tarfile.open(f"{export_dir}/posts.tar", 'a')

def addPost(nickname, wxid, postdate, import_path):
    global userPosts, export_dir, tar_file

    if wxid not in userPosts:
        userPosts[wxid] = {
            "nickname": [],
            "post": {}
        } # 初始化

    if nickname not in userPosts[wxid]['nickname']: # 添加昵称
        userPosts[wxid]['nickname'].append(nickname)

    if postdate not in userPosts[wxid]['post']:
        userPosts[wxid]['post'][postdate] = []

    num = len(userPosts[wxid]['post'][postdate])

    shutil.move(import_path, f"{export_dir}/posts/{wxid}/{postdate}_{num}")
    # tar_file.add(import_path, arcname=f"/{wxid}/{postdate}_{num}")

    userPosts[wxid]['post'][postdate].append({
        "num": num
    })

for import_dir in import_dirs:
    for folder in os.listdir(import_dir):
        if folder.startswith('.'):
            continue
        folderInfo = re.match(r'(.*?)\((.*?)\)_(\d{4}-\d{2}-\d{2}-\d{4})', folder) # 判断是否包含日期（有日期则为手动导出）
        if folderInfo: # 为手动导出 直接进行处理
            nickname = folderInfo.group(1)
            wxid = folderInfo.group(2)
            postdate = folderInfo.group(3)
            addPost(nickname, wxid, postdate, f"{import_dir}/{folder}")
            continue
        folderInfo = re.match(r'(.*?) \((.*?)\)', folder)
        if folderInfo:
            nickname = folderInfo.group(1)
            wxid = folderInfo.group(2)
            for post in os.listdir(f"{import_dir}/{folder}"):
                if post.startswith('.'):
                    continue
                postdate = re.match('(\d{4}-\d{2}-\d{2}-\d{4})', post).group(1)
                addPost(nickname, wxid, postdate, f"{import_dir}/{folder}/{post}")

# tar_file.close()

with open(f"{export_dir}/posts.json", "w+") as f:
    f.write(json.dumps(userPosts, ensure_ascii=False, separators=(',',':')))
