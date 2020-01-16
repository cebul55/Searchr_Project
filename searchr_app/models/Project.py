from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.db import models
from django.utils.text import slugify

# from searchr_app.models import Phrase


class Project(models.Model):
    """
    class Project is responsible for grouping Searches that belongs to a user.
    @:param str title
    @:param User user
    @:param Text description
    @:param Boolean is_private

    """
    PROJECT_TITLE_LENGTH = 128
    title = models.CharField(max_length=PROJECT_TITLE_LENGTH, blank=False, null=False,)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=False)
    description = models.TextField(blank=True)
    is_private = models.BooleanField(default=True, null=False)
    slug = models.SlugField(max_length=PROJECT_TITLE_LENGTH, null=False, unique=False)
    tag_weights = models.TextField(blank=False)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if self.title == '':
            raise ValidationError('Title can not be empty.')
        self.slug = slugify(self.title.strip())
        super(Project, self).save(*args, **kwargs)

    def validate_unique(self, exclude=None):
        if Project.objects.exclude(id=self.id).filter(title=self.title, is_private=False):
            raise ValidationError("Project with provided title already exists!")
        super(Project, self).validate_unique(exclude)

    # def _has_phrases(self):
    #     if self.id is None:
    #         return False
    #     phrases = Phrase.objects.get(projects=self)
    #     if phrases.len() > 0:
    #         return True
    #     else:
    #         return False

    class Meta:
        unique_together = ('title', 'user')
