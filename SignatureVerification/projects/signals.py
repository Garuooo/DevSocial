from django.db.models.signals import post_save, pre_delete
from .models import Review, Project


def CreateReview(sender, instance, created, **kwargs):
    review = instance
    project = review.project
    if created == True:
        project.vote_total = project.vote_total + 1
        if review.value == "up":
            project.positive_votes = project.positive_votes + 1
        project.vote_ratio = round(
            project.positive_votes/project.vote_total * 100)
    project.save()


def DeleteReview(sender, instance, **kwargs):
    review = instance
    project = review.project
    project.vote_total = project.vote_total - 1
    if review.value == "up":
        project.positive_votes = project.positive_votes - 1
    project.vote_ratio = round(project.positive_votes/project.vote_total * 100)
    project.save()


post_save.connect(CreateReview, sender=Review)
pre_delete.connect(DeleteReview, sender=Review)
