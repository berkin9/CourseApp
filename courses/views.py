from datetime import date,datetime
from django.shortcuts import get_object_or_404, redirect, render
from .models import Course, Category
from django.core.paginator import Paginator
from courses.forms import CourseCreateForm, CourseEditForm
import random
import os
from django.contrib.auth.decorators import login_required, user_passes_test

def index(request):
    kurslar = Course.objects.filter(isActive=1)
    kategoriler = Category.objects.all()

    paginator = Paginator(kurslar, 4)
    page = request.GET.get('page',1)
    page_obj  = paginator.page(page)

    return render(request, 'courses/list.html', {
        'categories': kategoriler,
        'page_obj'  : page_obj,
    })
    
# def create_course(request):
#     if request.method == "POST":
#         title = request.POST["title"]
#         description = request.POST["description"]
#         imageUrl = request.POST["imageUrl"]
#         slug = request.POST["slug"]
#         isActive = request.POST.get("isActive", False)

#         if isActive == "on":
#             isActive = True

#         kurs = Course(title=title, description = description,imageUrl=imageUrl, slug = slug, isActive = isActive)
#         kurs.save()
#         return redirect("/kurslar")

#     return render(request, "courses/create-course.html")

def isAdmin(user):
    return user.is_superuser

@user_passes_test(isAdmin)
def create_course(request):
    if request.method == "POST":
        form = CourseCreateForm(request.POST)

        if form.is_valid():
            kurs = Course(
                title=form.cleaned_data["title"],
                description=form.cleaned_data["description"],
                imageUrl=form.cleaned_data["imageUrl"],
                slug = form.cleaned_data["slug"],
                isActive = form.cleaned_data["isActive"])

            kurs.save()
            return redirect("/kurslar")

    else:
        form = CourseCreateForm()
    return render(request, "courses/create-course.html", {"form":form})

def search(request):
    if "q" in request.GET and request.GET["q"] != "":
        q = request.GET["q"]
        kurslar = Course.objects.filter(isActive=True,title__contains=q).order_by("date")
        kategoriler = Category.objects.all()
    else:
        return redirect("/kurslar")


    return render(request, 'courses/index.html', {
        'categories': kategoriler,
        'courses': kurslar,
    })  
@login_required()
def course_list(request):
    kurslar = Course.objects.all()
    return render(request, 'courses/course-list.html', {
        'courses': kurslar
    })
@user_passes_test(isAdmin)
def course_edit(request, id):
    course = get_object_or_404(Course, pk=id)

    if request.method == "POST":
        form = CourseEditForm(request.POST, instance=course)
        form.save()
        return redirect("course_list")
    else:
        form = CourseEditForm(instance=course)

    return render(request, "courses/edit-course.html", { "form":form })
    
@user_passes_test(isAdmin)
def upload(request):
    if request.method == "POST":
        uploaded_image = request.FILES['image']
        handle_uploaded_files(uploaded_image)
        return render(request, "courses/success.html")
    return render(request, "courses/upload.html")


def handle_uploaded_files(file):
    number = random.randint(1,99999)
    filename, file_extention = os.path.splitext(file.name)
    name = filename + "_" + str(number) + file_extention
    with open("temp/" + name,"wb+") as destination:
        for chunk in file.chunks():
            destination.write(chunk)

@user_passes_test(isAdmin)
def course_delete(request, id):
    course = get_object_or_404(Course, pk=id)
    if request.method == "POST":
        course.delete()
        return redirect("course_list")

    return render(request, "courses/course-delete.html", { "course":course })
   
def details(request, slug):
    course = get_object_or_404(Course, slug=slug)

    context = {
        'course': course
    }
    return render(request, 'courses/details.html', context)

def getCoursesByCategory(request, slug):
    kurslar = Course.objects.filter(categories__slug=slug, isActive=True)
    kategoriler = Category.objects.all()

    paginator = Paginator(kurslar, 3)
    page = request.GET.get('page',1)
    page_obj  = paginator.page(page)

    return render(request, 'courses/list.html', {
        'categories': kategoriler,
        'page_obj'  : page_obj,
        'seciliKategori': slug
    })
    