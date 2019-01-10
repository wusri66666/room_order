from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.

class MyUser(AbstractUser):
    phone = models.CharField(max_length=11)


class MeetingRoom(models.Model):
    name = models.CharField(max_length=32)
    addr = models.CharField(max_length=32)

    def __str__(self):
        return self.name


class ReserveRecord(models.Model):
    user = models.ForeignKey(MyUser)
    room = models.ForeignKey(MeetingRoom)
    data = models.DateField(verbose_name='预定日期')
    time1 = (
        (1,'8:00'),
        (2,'9:00'),
        (3,'10:00'),
        (4,'11:00'),
        (5,'12:00'),
        (6,'13:00'),
        (7,'14:00'),
        (8,'15:00'),
        (9,'16:00'),
        (10,'17:00'),
    )
    timeline = models.IntegerField(choices=time1,verbose_name='预定时间')
    class Meta:
        unique_together = ['data','timeline','room']

    def __str__(self):
        return self.name


