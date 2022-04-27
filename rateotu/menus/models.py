from decimal import Decimal

from django.db import models
from django.core.validators import MinValueValidator

from rateotu.utils.menus import get_menu_item_img_dir_upload_path

# TODO: add https://github.com/makinacorpus/django-safedelete


class Category(models.Model):
    NAME_CHOICES = [
        ("food", "Food"),
        ("drink", "Drink"),
    ]

    name = models.CharField(
        max_length=255, choices=NAME_CHOICES, help_text="Food or drink"
    )
    slug = models.SlugField(
        max_length=50,
        unique=True,
        help_text="SEO friendly URL path param (needed on the client apps)",
    )
    description = models.TextField(
        max_length=500, blank=True, help_text="Category description"
    )

    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.name


# Todo: Update Menu.updated_at when updating Item (out of sync)
class Item(models.Model):
    category = models.ForeignKey(
        Category, on_delete=models.CASCADE, related_name="menu_items"
    )
    image_url = models.ImageField(
        upload_to=get_menu_item_img_dir_upload_path,
        null=True,
        blank=True,
        help_text="Menu item thumbnail URL",
    )
    name = models.CharField(max_length=200)
    description = models.TextField(
        max_length=500, blank=True, help_text="Food or drink description"
    )
    # Max 999,999.99 (1M of 'space £')
    price = models.DecimalField(
        max_digits=8,
        decimal_places=2,
        validators=[MinValueValidator(Decimal("0.01"))],
        help_text="Price in space £",
    )
    available_quantity = models.PositiveIntegerField(
        default=1,
        help_text="""If a customer orders a multiple of the same food or drink,
                     or for a pre made food and drinks which can be served in
                     restaurants (e.g. cans of something, sweets, etc)""",
    )
    is_active = models.BooleanField(default=True, help_text="Discontinued or not")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class Menu(models.Model):
    """
    Menu model for a different purposes or events:
    - "seasonal" (on planets that have seasonal changes, e.g. Earth),
    - planet based (different species have different cuisines,
                    ingredients, food techniques, ways of eating, etc),
    - special situations (birthdays, space events, etc),
    - religiuous practices,
    - different restaurant locations or branches (in differnt galaxies, planets, etc)

    Also, the restaurant menu can be suspended or discontinued,
    hence the 'is_active' flag.
    """

    items = models.ManyToManyField(Item, related_name="menus")
    name = models.CharField(max_length=255)
    description = models.TextField(
        max_length=500, blank=True, help_text="Menu description"
    )
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Menus"
        verbose_name_plural = "Menus"

    def __str__(self):
        return self.name
