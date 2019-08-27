from django.db import models
from datetime import datetime


# Create your models here.

class JedzonkoPage(models.Model):
    title = models.CharField(max_length=255, null=False)
    description = models.TextField(null=False)
    slug = models.CharField(max_length=255, null=False)

    def __str__(self):
        return self.title


class JedzonkoRecipe(models.Model):
    name = models.CharField(max_length=255, null=False)
    ingredients = models.TextField(null=False)
    description = models.TextField(null=False)
    created = models.DateField(default=datetime.now)
    updated = models.DateField(default=datetime.now)
    preparation_method = models.TextField(null=False, default="")
    preperation_time = models.IntegerField(null=False)
    votes = models.IntegerField(null=True, default=0)

    def __str__(self):
        return self.name


class JedzonkoPlan(models.Model):
    name = models.CharField(max_length=255, null=False)
    description = models.TextField(null=False)
    created = models.DateField(default=datetime.now)

    def __str__(self):
        return self.name


class JedzonkoDayName(models.Model):
    dayname = models.CharField(max_length=16, null=False)
    order = models.IntegerField(null=False)

    def __str__(self):
        return self.order


class JedzonkoRecipePlan(models.Model):
    meal_name = models.CharField(max_length=255, null=False)
    order = models.IntegerField(null=False)
    recipe = models.ForeignKey(JedzonkoRecipe, on_delete=models.CASCADE)
    plan = models.ForeignKey(JedzonkoPlan, on_delete=models.CASCADE)
    day_name = models.ForeignKey(JedzonkoDayName, on_delete=models.CASCADE)

    def __str__(self):
        return self.meal_name
