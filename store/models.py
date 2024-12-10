from django.db import models
from django.contrib.auth.models import User
from io import BytesIO
import qrcode
from django.core.files.uploadedfile import InMemoryUploadedFile
from PIL import Image

# Create your models here.
class Product(models.Model):
    ID = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=200)
    price = models.IntegerField()
    image = models.ImageField(null=True, blank=True)

    def __str__(self):
        return self.name

    @property
    def imageURL(self):
        try:
            url = self.image.url
        except:
            url = ''
        return url


		

