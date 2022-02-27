import sys
from time import sleep
import urllib.request
import gdrive
import os
from tqdm import tqdm
import instaloader


class Arch:
    def __init__(self):
        self.filename = "test.jpg"
        self.dp = "iwanshes"
        self.ig = instaloader.Instaloader()

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

        # preparations
        inputs(self, False)
        max_count = 5
        try:
            temp_input = int(input('Input desired quantity of photos (default=5): '))
            if temp_input:
                max_count = temp_input
        except ValueError:
            print('Value was set to default value (5).')

        draw_progress_bar(0, post_text='preparations')
        prof = self.ig.check_profile_id(self.dp.lower())
        draw_progress_bar(0.15, post_text='downloading')

        # getting files
        posts = prof.get_posts()
        count = 1
        downloaded_files = []
        for post in posts:
            photo_name = str(post.date) + '.jpg'
            # тут на виндовсе возможна ошибка со знаком двоиточия
            # photo_name = photo_name.replace(':', '-')
            urllib.request.urlretrieve(post.url, photo_name)
            downloaded_files.append(photo_name)

            if max_count <= count:
                break

            count += 1

        # uploading files
        draw_progress_bar(0.45, post_text='uploading')
        gdrive_service = gdrive.googledrive_authenticate()
        gdrive.upload_pic(gdrive_service, downloaded_files, gdrive.get_id_of_folder(gdrive_service, arch.dp))
        draw_progress_bar(0.85, post_text='cleaning')

        for file in downloaded_files:
            delete_file(file)
        draw_progress_bar(1, post_text='done\n')


def delete_file(filename):
    if os.path.isfile(filename):
        os.remove(filename)


def draw_progress_bar(percent, bar_len=20, prefix='', post_text=''):
    # percent float from 0 to 1.
    sys.stdout.write("\r")
    sys.stdout.write(str(prefix)
                     + "[{:<{}}] {:.0f}% ".format("=" * int(bar_len * percent), bar_len, percent * 100)
                     + str(post_text))
    sys.stdout.flush()


def inputs(arche, fn_is_needed=True):
    if fn_is_needed:
        newname = input("Filename: ") + '.jpg'
        if newname != '.jpg':
            arche.filename = newname

    arche.dp = input("Username: ")


arch = Arch()

while True:
    n = input("1 = Archive avatar \n"
              "2 = Download avatar \n"
              "3 = Archive latest posts \n"
              "Any other input = exit \n"
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
