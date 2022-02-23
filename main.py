import instaloader
import urllib.request
import gdrive
import os


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
        # self.is_filled = False

    def download(self):
        profile = self.ig.check_profile_id(self.dp.lower())
        url_pic = profile.profile_pic_url
        urllib.request.urlretrieve(url_pic, self.filename)

    def send(self):
        service = gdrive.googledrive_authenticate()
        files = [self.filename]
        gdrive.upload_pic(service, files)

    def delete(self):
        if os.path.isfile(self.filename):
            os.remove(self.filename)

    def archive(self):
        self.download()
        self.send()
        self.delete()

        print('arch')
        pass


def inputs(arche):
    # if not arche.is_filled:
    newname = input("Filename: ") + '.jpg'
    if newname != '.jpg':
        arche.filename = newname

    arche.dp = input("Username: ")


arch = Arch()

while True:
    n = input("Write '1' for archive to GDrive '2' for download file or something else to Exit\n")
    if n == '1':
        inputs(arch)
        arch.archive()
        print("File is Archived")

    elif n == '2':
        inputs(arch)
        arch.download()
        print("File is Download")

    else:
        break
