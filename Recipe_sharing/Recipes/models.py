from django.db import models

# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=100)
    def __str__(self): 
        return self.name

class SkillLevel(models.Model):
    level_name = models.CharField(max_length=50)
    def __str__(self): 
        return self.level_name

class Recipe(models.Model):
    title = models.CharField(max_length=200)
    summary = models.TextField()
    cooking_time = models.PositiveIntegerField(help_text="Minutes")
    image = models.ImageField(upload_to='recipe_pics/', blank=True, null=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    level = models.ForeignKey(SkillLevel, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self): 
        return self.title

class Ingredient(models.Model):
    recipe = models.ForeignKey(Recipe, related_name='ingredients', on_delete=models.CASCADE)
    item_name = models.CharField(max_length=200)
    amount = models.CharField(max_length=50)

class InstructionStep(models.Model):
    recipe = models.ForeignKey(Recipe, related_name='steps', on_delete=models.CASCADE)
    step_number = models.PositiveIntegerField()
    description = models.TextField()

class PublicFeedback(models.Model):
    recipe = models.ForeignKey(Recipe, related_name='comments', on_delete=models.CASCADE)
    visitor_name = models.CharField(max_length=100)
    comment_text = models.TextField()
    date_added = models.DateTimeField(auto_now_add=True)

class 