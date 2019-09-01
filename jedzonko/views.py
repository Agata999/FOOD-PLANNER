from django.http import HttpResponse, HttpResponseForbidden
from datetime import datetime
from random import sample
from jedzonko.models import JedzonkoRecipe, JedzonkoPage, JedzonkoRecipePlan, JedzonkoPlan, JedzonkoDayName
from django.views import View
from math import ceil
from django.shortcuts import render, redirect
from django.core.paginator import Paginator


def my_plan_details(id):
    my_temp_id = int(id)
    my_plan_details = JedzonkoRecipePlan.objects.filter(plan_id=my_temp_id).order_by("day_name_id", 'order').all()
    days = [1, 2, 4, 5, 6, 7]
    prep_data = {}
    for day in days:
        prep_data[JedzonkoDayName.objects.get(id=day).dayname] = []
        for recipe in my_plan_details.filter(day_name_id=day).all():
            prep_data[JedzonkoDayName.objects.get(id=day).dayname].append(
                JedzonkoRecipe.objects.get(id=recipe.recipe_id))
    return prep_data


def plan_details_views(request):
    plan_details = JedzonkoPlan.objects.all().order_by("-created")[0]
    count_of_recipe_views = count_of_recipe()
    count_of_plan_view = count_of_plan()
    return render(request, "dashboard.html",
                  {"plan_details": plan_details, "count_of_recipe_views": count_of_recipe_views,
                   "count_of_plan_view": count_of_plan_view})


def count_of_recipe():
    return JedzonkoRecipe.objects.count()


def count_of_plan():
    return JedzonkoPlan.objects.count()


def recipe_list(request):
    if request.method == 'GET':
        recipes_list = JedzonkoRecipe.objects.all().order_by('-votes', 'created')
        paginator = Paginator(recipes_list, 50)
        page = request.GET.get('page')
        recipes = paginator.get_page(page)
        return render(request, 'app-recipes.html', {
            'recipes': recipes
        })
    elif request.method == 'POST':
        name = request.POST['name']
        recipe_list = JedzonkoRecipe.objects.filter(name__icontains=name)
        paginator = Paginator(recipe_list, 50)
        page = request.GET.get('page')
        recipes = paginator.get_page(page)
        return render(request, 'app-recipes.html', {
            'recipes': recipes
        })


def delete_recipe(request, r_id):
    recipe = JedzonkoRecipe.objects.get(pk=r_id)
    if request.method == 'GET':
        return render(request, 'app-delete-recipe.html')
    elif request.method == 'POST':
        recipe.delete()
        return redirect(recipe_list)


def add_recipe(request):
    if request.method == 'GET':
        return render(request, 'app-add-recipe.html')

    elif request.method == 'POST':
        name = request.POST['name']
        ingredients = request.POST['ingredients']
        description = request.POST['description']
        preperation_time = request.POST['preperation_time']
        preparation_method = request.POST['preparation_method']
        if name and ingredients and description and preperation_time and preparation_method:
            JedzonkoRecipe.objects.create(name=name, ingredients=ingredients, description=description,
                                          preperation_time=preperation_time, preparation_method=preparation_method, votes=0)
            return redirect(recipe_list)
        else:
            fill = 'Wypełnij poprawnie wszystkie pola !'
            return render(request, 'app-add-recipe.html', {
                'fill': fill
            })


def recipe_details(request, r_id):
    recipe = JedzonkoRecipe.objects.get(pk=r_id)
    if request.method == "GET":

        return render(request, 'app-recipe-details.html',
                      {'id_for_form': r_id, 'recipe': recipe})

    else:
        recipe.votes += 1
        recipe.save()
        flag = True
        return render(request, 'app-recipe-details.html', {'recipe': recipe, 'flag' : flag})


def get(request):
    ctx = {"actual_date": datetime.now()}
    return render(request, "test.html", ctx)


def loading_page(request):
    """1.1"""
    recipes_sample = JedzonkoRecipe.objects.all()
    temp = []
    for element in recipes_sample:
        temp.append(element.id)
    recipes_sample_list = []
    recipe_id_sample = sample(temp, 3)
    for id_temp in recipe_id_sample:
        recipes_sample_list.append(JedzonkoRecipe.objects.get(id=id_temp))
    return render(request, "index.html", {'samples': recipes_sample_list})


def contact_view(request):
    """1.2"""
    if JedzonkoPage.objects.filter(slug='under_construction').count() == 0:
        JedzonkoPage.objects.create(title='Strona w przygotowaniu',
                                    description='Nasi pracownicy juz przygotowuja ten kawalek strony, cierpliwosci!!',
                                    slug='under_construction')

    if JedzonkoPage.objects.filter(slug='contact').count() > 0:
        return render(request, "app-article-page.html", {'msg': JedzonkoPage.objects.get(slug='contact')})
    else:
        return render(request, "app-article-page.html", {'msg': JedzonkoPage.objects.get(slug='under_construction')})



def about_view(request):
    """1.2"""
    if JedzonkoPage.objects.filter(slug='under_construction').count() == 0:
        JedzonkoPage.objects.create(title='Strona w przygotowaniu',
                                    description='Nasi pracownicy juz przygotowuja ten kawalek strony, cierpliwosci!!',
                                    slug='under_construction')

    if JedzonkoPage.objects.filter(slug='about').count() > 0:
        return render(request, "app-article-page.html", {'msg': JedzonkoPage.objects.get(slug='about  ')})
    else:
        return render(request, "app-article-page.html", {'msg': JedzonkoPage.objects.get(slug='under_construction')})


def plan_add_view(request):
    """6.1 , 6.2"""
    if request.method == 'GET':
        return render(request, 'app-add-schedules.html')
    else:
        if request.POST['planName'] and request.POST['planDescription']:
            new_plan = JedzonkoPlan(name=request.POST['planName'], description=request.POST['planDescription'])
            new_plan.save()
            request.session['plan_id'] = JedzonkoPlan.objects.get(name=request.POST['planName'],
                                                                  description=request.POST['planDescription']).id
            return redirect('/plan/add/details')


def plan_add_details(request):
    """9.1 9.2 9.3 """
    if request.method == 'GET':
        if request.session.get('plan_id'):
            new_plan = JedzonkoPlan.objects.get(id=int(request.session.get('plan_id')))
            meal_list = ['Sniadanie', 'Drugie Sniadanie', 'Zupa', 'Drugie danie', 'Podwieczorek', 'Kolacja',
                         'Przekaska']
            recipes = JedzonkoRecipe.objects.all()
            week_days = JedzonkoDayName.objects.order_by('id').all()
            if JedzonkoRecipePlan.objects.filter(plan_id=int(request.session.get('plan_id'))).count() == 0:
                return render(request, 'app-schedules-meal-recipe.html',
                              {'new_plan': new_plan,
                               'recipes': recipes,
                               'week_days': week_days,
                               'meal_list': meal_list})
            else:
                prep_data = my_plan_details(int(request.session.get('plan_id')))
                return render(request, 'app-schedules-meal-recipe.html',
                              {'new_plan': new_plan,
                               'recipes': recipes,
                               'week_days': week_days,
                               'meal_list': meal_list,
                               'my_plan_data': prep_data})

        else:
            return HttpResponseForbidden
    else:
        if request.POST.get('remove_id'):
            del request.session['plan_id']
            return redirect('/plan/list')
        elif request.POST.get('show_plan'):
            return redirect('/plan/{}'.format(int(request.session['plan_id'])))

        else:
            meal = JedzonkoRecipePlan(meal_name=request.POST['meal_name_f'],
                                      order=int(request.POST['meal_number']),
                                      day_name_id=request.POST['day'],
                                      plan_id=request.POST['plan_id'],
                                      recipe_id=request.POST['recipe'])
            try:
                meal.save()
            except:
                pass
            return redirect('/plan/add/details')


def plan_list_page1(request):
    """7.1"""
    return redirect('/plan/list/1')


def plan_list(request, page_number):
    """7.1"""
    plans = JedzonkoPlan.objects.order_by('name').all()
    min = 1
    max = 50
    pages = ceil(len(plans) / 50)
    all1 = {}

    for p in range(1, pages + 1):
        dict_name = 'page_' + str(p)
        all1[dict_name] = []

    for b in range(1, pages + 1):
        all1['page_' + str(b)] = plans[min:max + 1]
        min += 50
        if max + 50 > len(plans):
            max = len(plans)
        else:
            max += 50

    page = 'page_' + str(page_number)
    pages = [n for n in range(1, pages + 1)]
    return render(request, 'app-schedules.html', {'plans': all1,
                                                  'page_in': page,
                                                  'page_count': pages,
                                                  'current_page': int(page_number)})


def edit_recipe(request, r_id):
    recipe = JedzonkoRecipe.objects.get(pk=r_id)
    if request.method == 'GET':
        return render(request, 'app-edit-recipe.html', {
            'recipe': recipe
        })
    elif request.method == 'POST':
        name = request.POST['name']
        description = request.POST['description']
        preparation_method = request.POST['preparation_method']
        preperation_time = request.POST['preperation_time']
        ingredients = request.POST['ingredients']

        recipe.name = name
        recipe.save()
        recipe.description = description
        recipe.save()
        recipe.preparation_method = preparation_method
        recipe.save()
        recipe.preperation_time = preperation_time
        recipe.save()
        recipe.ingredients = ingredients
        recipe.save()

        return redirect(recipe_list)


def plan_id(request, plan_number):
    my_plan = JedzonkoPlan.objects.get(id=int(plan_number))
    prep_data = my_plan_details(plan_number)
    return render(request, 'app-details-schedules.html', {'my_plan': my_plan,
                                                          'my_plan_data': prep_data})
