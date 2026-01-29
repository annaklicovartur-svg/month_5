from django.db import models

class Category(models.Model):
    name = models.CharField(max_length=255, verbose_name='Enter your category: ' )

class Product(models.Model):
    title = models.CharField(max_length=255)
    description = models.CharField(null=True, blank=True)
    price = models.IntegerField()
    # category = models.ForeignKey()

class Review(models.Model):
    text = models.TextField(null=True, blank=True)
    # product = models.ForeignKey()

    def __str__(self):
        return self.title