from django.shortcuts import render, redirect
from .models import Account, Role, Category, Recipe, RecipeIngredient, Comment, Rating, Favorite, ActionType, AdminLog
from django.contrib import messages
import hashlib


# Create your views here.
def hash_password(password):
    return hashlib.sha256(str.encode(password)).hexdigest()

def get_logged_user(request):
    user_id = request.session.get('user_id')
    if user_id:
        return Account.objects.get(id=user_id)
    return None

def register(request):
    roles = Role.objects.exclude(name='Admin')
    if request.method == 'POST':
        username = request.POST.get('username')
        role_id = request.POST.get('role')
        if Role.objects.get(id=role_id).name == 'Admin' and Account.objects.filter(role__name='Admin').exists():
            return render(request, 'register.html', {'error': 'Admin already exists', 'roles': roles})
        
        user = Account(
            username=username,
            email=request.POST.get('email'),
            password=hash_password(request.POST.get('password')),
            role_id=role_id
        )
        user.save()
        return redirect('login')
    return render(request, 'register.html', {'roles': roles})

def login_view(request):
    if request.method == 'POST':
        u = request.POST.get('username')
        p = hash_password(request.POST.get('password'))
        user = Account.objects.filter(username=u, password=p).first()
        if user:
            request.session['user_id'] = user.id
            request.session['role'] = user.role.name
            return redirect('home')
    return render(request, 'login.html')

def logout_view(request):
    request.session.flush()
    return redirect('login')


def home(request):
    recipes = Recipe.objects.filter(is_approved=True).order_by('-created_on')
    return render(request, 'home.html', {'recipes': recipes})

def recipe_detail(request, recipe_id):
    recipe = Recipe.objects.get(id=recipe_id)
    ingredients = RecipeIngredient.objects.filter(recipe=recipe)
    comments = Comment.objects.filter(recipe=recipe)
    user = get_logged_user(request)
    
    if request.method == 'POST' and user:
        comment_text = request.POST.get('comment')
        Comment.objects.create(recipe=recipe, user=user, text=comment_text)
        return redirect('recipe_detail', recipe_id=recipe_id)
        
    return render(request, 'recipe_detail.html', {'recipe': recipe, 'ingredients': ingredients, 'comments': comments})

def search_recipes(request):
    query = request.GET.get('q')
    results = Recipe.objects.filter(title__icontains=query, is_approved=True)
    return render(request, 'home.html', {'recipes': results})

def category_recipes(request, cat_id):
    recipes = Recipe.objects.filter(is_approved=True, category_id=cat_id)
    return render(request, 'home.html', {'recipes': recipes})


def submit_recipe(request):
    user = get_logged_user(request)
    if not user or user.role.name != 'User': 
        return redirect('login')
    
    if request.method == 'POST':
        category_id = request.POST.get('category')
        if category_id:
            category_obj = Category.objects.get(id=category_id)
        else: 
            category_obj = None

        Recipe.objects.create(
            author=user,
            title=request.POST.get('title'),
            description=request.POST.get('description'),
            category=category_obj,
            ingredients=request.POST.get('ingredients_raw'), 
            instructions=request.POST.get('instructions'),
            image=request.FILES.get('image_file')
        )
        return redirect('my_recipes')
    categories = Category.objects.all()
    return render(request, 'submit_recipe.html',{'categories': categories})

def my_recipes(request):
    user = get_logged_user(request)
    recipes = Recipe.objects.filter(author=user)
    return render(request, 'my_recipes.html', {'recipes': recipes})

def edit_recipe(request, recipe_id):
    user = get_logged_user(request)
    recipe = Recipe.objects.get(id=recipe_id)
    
    if not user or recipe.author != user:
        return redirect('home')

    if request.method == 'POST':
        recipe.title = request.POST.get('title')
        recipe.description = request.POST.get('description')
        recipe.ingredients = request.POST.get('ingredients_raw')
        recipe.instructions = request.POST.get('instructions')
        category_id = request.POST.get('category')
        if category_id:
            recipe.category = Category.objects.get(id=category_id)
        else:
            recipe.category = None
        if request.FILES.get('image_file'):
            recipe.image = request.FILES.get('image_file')        
        recipe.is_approved = False  
        recipe.save()
        return redirect('my_recipes')
    categories = Category.objects.all()
    return render(request, 'edit_recipe.html', {'recipe': recipe,'categories': categories})

def delete_recipe(request, recipe_id):
    Recipe.objects.filter(id=recipe_id).delete()
    return redirect('my_recipes')

def add_to_favorites(request, recipe_id):
    user = get_logged_user(request)
    recipe = Recipe.objects.get(id=recipe_id)
    Favorite.objects.get_or_create(user=user, recipe=recipe)
    return redirect('recipe_detail', recipe_id=recipe_id)

def rate_recipe(request, recipe_id):
    if request.method == 'POST':
        user = get_logged_user(request)
        Rating.objects.update_or_create(
            user=user, recipe_id=recipe_id, 
            defaults={'stars': request.POST.get('stars')}
        )
    return redirect('recipe_detail', recipe_id=recipe_id)


def admin_dashboard(request):
    user = get_logged_user(request)
    if user.role.name != 'Admin': return redirect('home')
    pending = Recipe.objects.filter(is_approved=False)
    return render(request, 'admin_dash.html', {'pending': pending})

def manage_categories(request):
    user = get_logged_user(request)
    if not user or user.role.name != 'Admin':
        return redirect('home')
    
    categories = Category.objects.all()
    return render(request, 'manage_categories.html', {'categories': categories})

def approve_recipe(request, recipe_id):
    user = get_logged_user(request)
    recipe = Recipe.objects.get(id=recipe_id)
    recipe.is_approved = True
    recipe.save()
    action = ActionType.objects.get_or_create(name='APPROVE')[0]
    AdminLog.objects.create(admin=user, action=action, target_recipe=recipe)
    return redirect('admin_dashboard')

def reject_recipe(request, recipe_id):
    recipe = Recipe.objects.get(id=recipe_id)
    recipe.delete()
    return redirect('admin_dashboard')

def manage_users(request):
    users = Account.objects.all()
    return render(request, 'manage_users.html', {'users': users})

def delete_user(request, user_id):
    Account.objects.filter(id=user_id).delete()
    return redirect('manage_users')

def admin_logs(request):
    logs = AdminLog.objects.all().order_by('-timestamp')
    return render(request, 'logs.html', {'logs': logs})


def add_category(request):
    if request.method == 'POST':
        Category.objects.create(name=request.POST.get('name'))
    return redirect('manage_categories')

def delete_category(request, cat_id):
    Category.objects.filter(id=cat_id).delete()
    return redirect('manage_categories')

def profile_settings(request):
    user = get_logged_user(request)
    if request.method == 'POST':
        user.email = request.POST.get('email')
        new_password = request.POST.get('password')
        if new_password and new_password.strip() != "":
            user.password = hash_password(new_password)
        user.save()
    return render(request, 'profile.html', {'user': user})
def role(request):
    user = get_logged_user(request)
    if not user or user.role.name != 'Admin':
        return redirect('home')

    if request.method == 'POST':
        role_name = request.POST.get('role_name')
        
        if role_name:
            if not Role.objects.filter(name=role_name).exists():
                Role.objects.create(name=role_name)
                messages.success(request, f"Role '{role_name}' created successfully!")
            else:
                messages.error(request, "This role already exists.")
        
        return redirect('manage_roles') 

    roles = Role.objects.all()
    return render(request, 'role_template.html', {'roles': roles})