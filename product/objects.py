# imports
from django.db import models
from django.db.models import Q
from django.utils.text import slugify


class ProductManager(models.Manager):
    def create(self, **kwargs):
        name = kwargs.get("name")

        if name:
            base_slug = slugify(name)
            slug = base_slug
            counter = 1

            while self.filter(slug=slug).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1

            kwargs["slug"] = slug

        return super().create(**kwargs)

    def search(self, content):
        model = self.get_queryset()
        return model.filter(
            Q(name__icontains=content) | Q(description__icontains=content)
        )


class CategoryManager(models.Manager):
    def create(self, **kwargs):
        slug = slugify(kwargs.get("name"))
        kwargs["slug"] = slug
        return super().create(**kwargs)
