from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify
from common import TimeStampMixin

class Category(TimeStampMixin):
    category_name = models.CharField(max_length=100, unique=True)

    class Meta:
        verbose_name_plural = "Categories"
        ordering = ["category_name"]

    def __str__(self):
        return self.category_name


class Tag(TimeStampMixin):
    tag_name = models.CharField(max_length=50, unique=True)

    class Meta:
        ordering = ["tag_name"]

    def __str__(self):
        return self.tag_name
    
    
class Post(TimeStampMixin):
    class Status(models.TextChoices):
        DRAFT = "DRAFT", "Draft"
        PUBLISHED = "PUBLISHED", "Published"

    title = models.CharField(max_length=255)

    slug = models.SlugField(max_length=255, unique=True, blank=True)

    content = models.TextField()

    featured_image = models.ImageField(
        upload_to="posts/",
        blank=True,
        null=True
    )

    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name="posts"
    )

    tags = models.ManyToManyField(
        Tag,
        related_name="posts",
        blank=True
    )

    author = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        related_name="posts",
        null=True,
        blank=True
    )

    status = models.CharField(
        max_length=10,
        choices=Status.choices,
        default=Status.DRAFT
    )

    view_count = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.title)
            slug = base_slug
            counter = 1

            while Post.objects.filter(slug=slug).exclude(pk=self.pk).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1

            self.slug = slug

        super().save(*args, **kwargs)
        

class Comment(TimeStampMixin):
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        related_name="comments"
    )
    
    author = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        related_name="comments",
        null=True,
        blank=True
    )

    comment = models.TextField()
    parent = models.ForeignKey(
        'self',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='replies'
    )

    class Meta:
        ordering = ["created_at"]

    def __str__(self):
        return f"{self.author.username if self.author else 'Anonymous'} on {self.post.title}"