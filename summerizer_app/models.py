import email
from django.db import models
from django.db.models.signals import pre_save
from django.dispatch import receiver
import uuid
# Create your models here.

class Feedback_percent(models.Model):
    id=models.UUIDField(default=uuid.uuid4,primary_key=True,unique=True,editable=False)
    good_percent=models.FloatField()
    bad_percent=models.FloatField()


    def __str__(self):
        return "Positive: "+str(round(self.good_percent,2))+" Negative: "+str(round(self.bad_percent,2))



class Feedback(models.Model):
    id=models.UUIDField(default=uuid.uuid4,primary_key=True,unique=True,editable=False)
    IP=models.CharField(max_length=255)
    feedback=models.CharField(max_length=255)
    msg=models.CharField(max_length=255, default="")
    email=models.CharField(max_length=255, default="")

    def __str__(self):
        return self.feedback


@receiver(models.signals.post_delete, sender=Feedback)
def delete_file(sender, instance, *args, **kwargs):
    """ Deletes thumbnail files on `post_delete` """
    try:
        feeds=Feedback.objects.all()
        good=""
        bad=""
        print(feeds.count())
        if(feeds.count()>0):
            good=Feedback.objects.filter(feedback="Good")
            bad=Feedback.objects.filter(feedback="Bad")

            good=(good.count()*100)/feeds.count()
            bad=(bad.count()*100)/feeds.count()
            
            f_percent=Feedback_percent.objects.last()
        if(f_percent):
            try:
                f_percent.bad_percent = bad
                f_percent.good_percent = good
                f_percent.save()
            except:
                f_percent.bad_percent = 0.00
                f_percent.good_percent = 0.00
                f_percent.save()
        else:
            f_percent=Feedback_percent.objects.create(good_percent=good, bad_percent=bad);
            f_percent.save()
    except:
        f_percent=Feedback_percent.objects.last()
        f_percent.good_percent=0.00
        f_percent.bad_percent=0.00
        f_percent.save()
   