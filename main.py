import urllib.request
import gdrive
import os
from tqdm import tqdm
import instaloader

# filename = 'test.jpg'
# ig = instaloader.Instaloader()
# dp = 'iwanshes'
#
# profile = ig.check_profile_id(dp.lower())
# url_pic = profile.profile_pic_url
#
# urllib.request.urlretrieve(url_pic, filename)
#
# service = gdrive.googledrive_authenticate()
#
# files = [filename]
#
# gdrive.upload_pic(service, files)


class Arch:
    def __init__(self):
        self.filename = "test.jpg"
        self.dp = "iwanshes"
        self.ig = instaloader.Instaloader()
        self.is_filled = False
        self.folder_instagram = ''

    def download_profile_pic(self):
        profile = self.ig.check_profile_id(self.dp.lower())
        url_pic = profile.profile_pic_url
        urllib.request.urlretrieve(url_pic, self.filename)

    def download_with_progressbar(self):
        todo_list = [self.download_profile_pic]
        for item in tqdm(todo_list):
            item()

    def send(self):
        service = gdrive.googledrive_authenticate()
        parent_id = gdrive.get_id_of_folder(service, arch.dp)
        files = [self.filename]
        gdrive.upload_pic(service, files, parent_id)

    def delete(self):
        if os.path.isfile(self.filename):
            os.remove(self.filename)

    def archive(self):
        todo_list = [self.download_profile_pic, self.send, self.delete]
        for item in tqdm(todo_list):
            item()

    def archive_latest_posts(self):
        inputs(self)
        prof = self.ig.check_profile_id(self.dp.lower())
        max_count = 5
        count = 1
        for post in prof.get_posts():
            res = self.ig.download_post(post, self.dp)
            photo_name = str(post.date) + '.jpg'
            urllib.request.urlretrieve(post.url, photo_name)
            print(res)

            if max_count < count:
                break

            count += 1


def inputs(arche):
    if not arche.is_filled:
        newname = input("Filename: ") + '.jpg'
        if newname != '.jpg':
            arche.filename = newname

        arche.dp = input("Username: ")





arch = Arch()

while True:
    n = input("1 = Archive avatar \n "
              "2 = Download avatar \n "
              "3 = Archive latest posts \n "
              "Any other input = exit \n "
              "Your input: ")
    if n == '1':
        inputs(arch)
        arch.archive()
        print("File is Archived")

    elif n == '2':
        inputs(arch)
        arch.download_with_progressbar()
        print("File is Downloaded")
    elif n == '3':
        arch.archive_latest_posts()
    else:
        break
