from django.db import models


class UserModel(models.Model):
    username = models.CharField(max_length=32, unique=True)
    password = models.CharField(max_length=256)
    email = models.CharField(max_length=64, unique=True)

    sex = models.BooleanField(default=False)
    icon = models.ImageField(upload_to='icons')
    is_delete = models.BooleanField(default=False)

    class Meta:
        db_table = "axf_users"


class UserTicketModel(models.Model):
    user = models.ForeignKey(UserModel)
    ticket = models.CharField(max_length=256)
    out_time = models.DateTimeField()

    class Meta:
        db_table ="axf_users_ticket"