from django.shortcuts import render, redirect, get_object_or_404
from .models import Recipe, Category, SkillLevel, Ingredient, InstructionStep, PublicFeedback

# Create your views here.
def recipe_list(request):
    recipes = Recipe.objects.all().order_by('-created_at')
    return render(request, 'index.html', {'recipes': recipes})

def recipe_detail(request, pk):
    recipe = get_object_or_404(Recipe, pk=pk)
    if request.method == "POST":
        PublicFeedback.objects.create(
            recipe=recipe,
            visitor_name=request.POST.get('name'),
            comment_text=request.POST.get('comment')
        )
        return redirect('recipe_detail', pk=pk)
    return render(request, 'detail.html', {'recipe': recipe})

def add_recipe(request):
    if request.method == "POST":
        recipe = Recipe.objects.create(
            title=request.POST.get('title'),
            summary=request.POST.get('summary'),
            cooking_time=request.POST.get('time'),
            category_id=request.POST.get('category'),
            level_id=request.POST.get('level'),
            image=request.FILES.get('image')
        )
        
        ing_text = request.POST.get('ingredients_text', '')
        for line in ing_text.split('\n'):
            if ':' in line:
                name, amt = line.split(':')
                Ingredient.objects.create(recipe=recipe, item_name=name.strip(), amount=amt.strip())
        
        step_text = request.POST.get('steps_text', '')
        for i, text in enumerate(step_text.split('\n'), 1):
            if text.strip():
                InstructionStep.objects.create(recipe=recipe, step_number=i, description=text.strip())
                
        return redirect('recipe_list')
    
    context = {
        'categories': Category.objects.all(),
        'levels': SkillLevel.objects.all()
    }
    return render(request, 'add_recipe.html', context)

def manage_content(request):
    if request.method == "POST":
        action = request.POST.get('action')
        
        if action == "add_category":
            Category.objects.create(name=request.POST.get('name'))
        elif action == "update_category":
            obj = get_object_or_404(Category, id=request.POST.get('cat_id'))
            obj.name = request.POST.get('name')
            obj.save()
        elif action == "delete_category":
            get_object_or_404(Category, id=request.POST.get('cat_id')).delete()

        elif action == "add_level":
            SkillLevel.objects.create(level_name=request.POST.get('level_name'))
        elif action == "update_level":
            obj = get_object_or_404(SkillLevel, id=request.POST.get('lvl_id'))
            obj.level_name = request.POST.get('level_name')
            obj.save()
        elif action == "delete_level":
            get_object_or_404(SkillLevel, id=request.POST.get('lvl_id')).delete()

        elif action == "delete":
            get_object_or_404(Recipe, id=request.POST.get('recipe_id')).delete()
        elif action == "update":
            recipe = get_object_or_404(Recipe, id=request.POST.get('recipe_id'))
            recipe.title = request.POST.get('title')
            recipe.summary = request.POST.get('summary')
            recipe.cooking_time = request.POST.get('time')
            recipe.category_id = request.POST.get('category')
            recipe.level_id = request.POST.get('level')
            
            if request.FILES.get('image'):
                recipe.image = request.FILES.get('image')
            
            recipe.save()

            recipe.ingredients.all().delete()
            for line in request.POST.get('ingredients_text', '').split('\n'):
                if ':' in line:
                    name, amt = line.split(':')
                    Ingredient.objects.create(recipe=recipe, item_name=name.strip(), amount=amt.strip())

            recipe.steps.all().delete()
            for i, text in enumerate(request.POST.get('steps_text', '').split('\n'), 1):
                if text.strip():
                    InstructionStep.objects.create(recipe=recipe, step_number=i, description=text.strip())

        return redirect('manage_content')

    context = {
        'categories': Category.objects.all(),
        'levels': SkillLevel.objects.all(),
        'recipes': Recipe.objects.all()
    }
    return render(request, 'manage.html', context)