from django.forms import ModelForm
from .models import Project, Review, Tag


class ProjectCreationForm(ModelForm):
    class Meta:
        model = Project
        fields = "__all__"
        exclude = ["owner", "vote_total",
                   "vote_ratio", "id", 'created', 'updated']


class ReviewForm(ModelForm):
    class Meta:
        model = Review
        fields = "__all__"
        exclude = ["owner", "project"]
