from django.db import models
import uuid
from django.core.exceptions import ValidationError
from django.core.validators import FileExtensionValidator
from django.core.validators import MinValueValidator, MaxValueValidator

class Items(models.Model):

    def file_limit(value):
        limit = 500000000
        if value.size>limit:
            raise ValidationError("ファイルサイズが大きすぎます")

    pin = models.IntegerField(
        validators=[MinValueValidator(1000), MaxValueValidator(9999)],
        verbose_name="PIN"
    )
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
        verbose_name="ID"
    )
    created = models.DateTimeField(
        auto_now_add=True,
        verbose_name="created"
    )
    video = models.FileField(
        upload_to="after/video/",
        null=True, verbose_name="video",
        validators=[FileExtensionValidator(allowed_extensions=["mp4", ]), file_limit]
    )
    img = models.ImageField(
        upload_to="after/img/",
        null=True,
        blank=True,
        verbose_name="img"
    )
    img_back_none = models.ImageField(
        upload_to="after/img/",
        null=True,
        blank=True,
        verbose_name="img_back_none"
    )
    status = models.CharField(
        max_length=20,
        default="unstarted",
        verbose_name="進捗状況"
    )

    def __str__(self):
        return str(self.id)
