from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.db import models


class Project(models.Model):
    """
    class Project is responsible for grouping Searches that belongs to a user.

    """
    PROJECT_TITLE_LENGTH = 128
    title = models.CharField(max_length=PROJECT_TITLE_LENGTH, blank=False, null=False, default=None)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=False)
    description = models.TextField(blank=True)
    is_private = models.BooleanField(default=True, null=False)

    def __str__(self):
        return self.title

    def validate_unique(self, exclude=None):
        if Project.objects.exclude(id=self.id).filter(title=self.title, is_private=False):
            raise ValidationError("Project with provided title already exists!")
        super(Project, self).validate_unique(exclude)

    class Meta:
        unique_together = ('title', 'user')
