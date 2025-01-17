from django.db import models

# Create your models here.

class VisitCounter(models.Model):
    count = models.IntegerField(default=0)
    last_updated = models.DateTimeField(auto_now=True)

    @classmethod
    def increment(cls):
        counter = cls.objects.first()
        if not counter:
            counter = cls.objects.create()
        counter.count += 1
        counter.save()
        return counter.count

    def __str__(self):
        return f"Visit Count: {self.count}"
