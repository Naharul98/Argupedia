from django.db import models
import re
import bleach
import markdown
from django.conf import settings
from django.contrib.auth.models import User
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.urls import reverse
from django.utils import timezone
from django.utils.functional import cached_property
from django.utils.html import format_html
from mptt.models import MPTTModel, TreeForeignKey


class Scheme(models.Model):
    scheme_name = models.CharField(max_length=100)
    def __str__(self):
        return self.scheme_name

class SchemeStructure(models.Model):
    ORDERING = [('1', '1'),('2', '2'),('3', '3'),('4', '4'),('5', '5'),('6', '6'),('7', '7'),('8', '8'),]
    scheme = models.ForeignKey(Scheme, on_delete=models.CASCADE, related_name="scheme")
    section_title = models.CharField(max_length=100)
    ordering = models.CharField(max_length=50,choices=ORDERING)
    section_description = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return self.section_title

class CriticalQuestion(models.Model):
    related_scheme = models.ForeignKey(Scheme, on_delete=models.CASCADE, related_name="related_scheme")
    is_attack_on_conclusion = models.BooleanField()
    question = models.CharField(max_length=500)

    def __str__(self):
        return self.question

class Entry(MPTTModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="author")
    parent = TreeForeignKey("self", null=True, blank=True, on_delete=models.CASCADE, related_name="children")
    content = models.TextField(max_length=4000, default="", help_text="")
    content_formatted = models.TextField(default="")
    title = models.TextField(max_length=100, default="", help_text="", blank=True)
    upvotes = models.ManyToManyField(User, blank=True, related_name="upvotes")
    downvotes = models.ManyToManyField(User, blank=True, related_name="downvotes")
    created_date = models.DateTimeField(default=timezone.now)
    modified_date = models.DateTimeField(blank=True, null=True)
    scheme_used = models.ForeignKey(Scheme, on_delete=models.CASCADE, related_name="scheme_used")
    critical_question = models.ForeignKey(CriticalQuestion, null=True, blank=True, on_delete=models.CASCADE, related_name="critical_question")

    class MPTTMeta:
        order_insertion_by = ["-created_date"]

    class Meta:
        verbose_name_plural = "Entries"

    def __str__(self):
        if len(self.content) > 45:
            return f'"{self.content:.45}..."'
        return f'"{self.content}"'

    def get_absolute_url(self):
        return reverse('entry-detail-view', args=[str(self.id)])

    def format_content(self):
        self.content_formatted = self.content
        # Clean and format content
        self.content_formatted = bleach.clean(markdown.markdown(self.content_formatted, extensions=["extra"]),settings.MARKDOWN_TAGS,settings.MARKDOWN_ATTRS,)
        self.content = bleach.clean(self.content, settings.MARKDOWN_TAGS, settings.MARKDOWN_ATTRS)

    def save(self, *args, **kwargs):
        created = True if not self.pk else False
        if not created:
            self.modified_date = timezone.now()
        self.format_content()
        super().save(*args, **kwargs)
        if created:
            self.upvotes.add(self.user)

    @cached_property
    def votes_sum(self):
        """
        Returns substract of downvotes from upvotes
        """
        return self.upvotes.count() - self.downvotes.count()

    @cached_property
    def root_pk(self):
        """
        Returns id of root node (if node is a root node then root_pk = self.pk)
        """
        return self.get_root().pk

    @cached_property
    def has_children(self):
        """
        Returns True if entry has children nodes
        """
        return self.get_children().exists()

    def parent_formatted(self):
        """
        Formats parent node into a hyperlink
        """
        if not self.parent:
            return "-"
        url = reverse("admin:app_entry_change", args=(self.parent.pk,))
        return format_html('<a href="{}">#{}</a>', url, self.parent.pk)

    def user_formatted(self):
        """
        Formats author into a hyperlink
        """
        url = reverse("admin:app_user_change", args=(self.user.pk,))
        return format_html('<a href="{}">{}</a>', url, self.user.username)

    parent_formatted.short_description = "Parent entry"
    user_formatted.short_description = "User"