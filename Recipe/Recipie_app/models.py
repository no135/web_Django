from django.db import models
# Create your models here.

class Role(models.Model):
    name = models.CharField(max_length=20, unique=True) # e.g., 'Admin', 'User', 'Viewer'
    
    def __str__(self):
        return self.name

class Account(models.Model):
    username = models.CharField(max_length=50, unique=True)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=255)
    role = models.ForeignKey(Role, on_delete=models.PROTECT)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.username} ({self.role.name})"


class Category(models.Model):
    name = models.CharField(max_length=50)
    
    def __str__(self):
        return self.name

class Recipe(models.Model):
    author = models.ForeignKey(Account, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    description = models.TextField()
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)
    ingredients = models.TextField()
    instructions = models.TextField()
    image = models.ImageField(upload_to='recipe_pics/', blank=True, null=True)
    is_approved = models.BooleanField(default=False) # Controlled by Admin
    created_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class RecipeIngredient(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    item_name = models.CharField(max_length=100)
    quantity = models.CharField(max_length=50)

# --- 3. VIEWER INTERACTIONS ---

class Comment(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE, related_name="comments")
    user = models.ForeignKey(Account, on_delete=models.CASCADE)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

class Rating(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    user = models.ForeignKey(Account, on_delete=models.CASCADE)
    stars = models.IntegerField(choices=[(i, i) for i in range(1, 6)])

class Favorite(models.Model):
    user = models.ForeignKey(Account, on_delete=models.CASCADE)
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)


class ActionType(models.Model):
    name = models.CharField(max_length=50) 

    def __str__(self):
        return self.name

class AdminLog(models.Model):
    admin = models.ForeignKey(Account, on_delete=models.CASCADE)
    action = models.ForeignKey(ActionType, on_delete=models.CASCADE)
    target_recipe = models.ForeignKey(Recipe, on_delete=models.SET_NULL, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    reason = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return f"{self.admin.username} performed {self.action.name}"