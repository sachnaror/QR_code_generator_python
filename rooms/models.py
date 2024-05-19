from io import BytesIO

import wifi_qrcode_generator
from django.core.files.base import ContentFile
# Create your models here.
from django.db import models
from django.utils.text import slugify


class Room(models.Model):
    name = models.CharField(max_length=120)
    qr_code = models.ImageField(upload_to='qr_codes', blank=True)

    def __str__(self):
        return str(self.name)

    def save(self, *args, **kwargs):
        if not self.qr_code:
            slug = slugify(self.name)
            qr_code = wifi_qrcode_generator.wifi_qrcode(
                f'wifi-{slug}', False, 'WPA', 'lolapola'
            )
            fname = f'qr_code-{slug}.png'

            buffer = BytesIO()
            qr_code.save(buffer, format='PNG')

            self.qr_code = ContentFile(buffer.getvalue(), fname)

        super().save(*args, **kwargs)
