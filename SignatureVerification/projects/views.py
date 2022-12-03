from django.shortcuts import render
from django.shortcuts import redirect
from .forms import ProjectCreationForm, ReviewForm
from django.contrib.auth.decorators import login_required
from .models import Project, Review, Tag 
from django.contrib import messages
# Create your views here.


@login_required(login_url='login')
def create_project(request):
    form = ProjectCreationForm()
    if request.method == "POST":
        form = ProjectCreationForm(request.POST, request.FILES)
        if form.is_valid():
            project = form.save(commit=False)
            project.owner = request.user.profile
            project.save()
            return redirect("profiles")
    context = {"form": form}
    return render(request, "project_form.html", context)


@login_required(login_url='login')
def update_project(request, pk):
    try:
        project = Project.objects.get(id=pk)
    except:
        messages.error(request, "Project Not Found")
        return redirect("projects")
    if project.owner != request.user.profile:
        messages.error(request, "You are the owner of the projects")
        return redirect("projects")
    form = ProjectCreationForm(instance=project)
    if request.method == "POST":
        form = ProjectCreationForm(
            request.POST, request.FILES, instance=project)
        if form.is_valid():
            form.save()
        messages.success(request, "Updated")
        return redirect("projects")

    context = {"form": form}
    return render(request, "project_form.html", context)


@login_required(login_url='login')
def delete_project(request, pk):
    try:
        project = Project.objects.get(id=pk)
    except:
        messages.error(request, "Project Not Found")
        return redirect("projects")
    if project.owner != request.user.profile:
        messages.error(request, "You are the owner of the projects")
        return redirect("projects")
    if request.method == "POST":
        project.delete()
        messages.success(request, "Deleted")
        return redirect("projects")
    return render(request, "delete_project.html")


def project(request, pk):
    form = ReviewForm()
    try:
        project = Project.objects.get(id=pk)
    except:
        messages.error(request, "Project Not Found")
        return redirect("projects")
    try:
        reviews = Review.objects.filter(project=project)
        reviewers = []
        for review in reviews:
            reviewers.append(review.owner)
    except:
        return redirect("projects")
    if project == None:
        messages.error(request, "Project not found")
        return redirect("profiles")

    if request.method == "POST":
        if project.owner == request.user.profile:
            messages.error(request, "You are the owner of the project")
            return redirect("projects")
        try:
            review = Review.objects.get(
                owner=request.user.profile, project=project)
            messages.error(request, "You are the already submitted a review")
            return redirect("project", project.id)
        except:
            form = ReviewForm()
            form = ReviewForm(request.POST)
            if form.is_valid():
                form = form.save(commit=False)
                form.project = project
                form.owner = request.user.profile
                form.save()
                return redirect("project", project.id)
    context = {"project": project, "reviews": reviews,
               "reviewers": reviewers, "form": form}
    return render(request, "project.html", context)


def projects(request):
    projects = Project.objects.all()
    context = {'projects': projects}
    return render(request, "projects.html", context)


def update_review(request, pk):
    try:
        review = Review.objects.get(id=pk)
        value = review.value
    except:
        messages.error(request, "Review Not Found")
        return redirect("projects")
    if review.owner != request.user.profile:
        messages.error(request, "You are the owner of the Review")
        return redirect("projects")
    project = review.project
    form = ReviewForm(instance=review)
    if request.method == "POST":
        form = ReviewForm(request.POST, instance=review)
        if form.is_valid():
            form = form.save()
            if form.value != value:
                if form.value == "up":
                    project.positive_votes = project.positive_votes + 1
                else:
                    project.positive_votes = project.positive_votes - 1
                project.vote_ratio = round(
                    project.positive_votes/project.vote_total * 100)
                project.save()
            return redirect("project", project.id)
    context = {"value": "create", "form": form}
    return render(request, 'review.html', context)


def delete_review(request, pk):
    try:
        review = Review.objects.get(id=pk)
        project = review.project
    except:
        messages.error(request, "Review Not Found")
        return redirect("projects")
    if review.owner != request.user.profile:
        messages.error(request, "You are the owner of the Review")
        return redirect("projects")
    if request.method == "POST":
        review.delete()
        return redirect("project", project.id)
    return render(request, 'delete_review.html')




