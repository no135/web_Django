from django.db import models


# Create your models here.

class articles(models.Model):
    title = models.CharField(max_length=450)
    description = models.TextField
    date = models.DateTimeField(auto_now_add=True)

    def _str_(self):
        return self.title