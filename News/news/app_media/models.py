import datetime

from django.db import models

class File(models.Model):
    """генерирует путь и имя файла в формате "текущаяДата_имяОргинальногоФайла".  "ddmmyy-hh-mm-ss"."""
    def get_file_path(self, filename):
        current_date = datetime.datetime.now()
        current_date_string = current_date.strftime('%d%m%y-%H-%M-%S')
        name = current_date_string + '_' + filename
        path = "files/{filename}".format(filename=name)
        return path

    file = models.FileField(upload_to=get_file_path)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
