"""
Business-wide settings that must be editable without a code deploy.

Anything here is a value the business owner changes as the business changes:
branding, the sales tax rate, delivery fees, upload limits. None of it belongs
in source code, where changing it means a commit and a redeploy.
"""

from decimal import Decimal

from django.core.cache import cache
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

CACHE_KEY = "core:business_config"
CACHE_TTL = 300


class SingletonModel(models.Model):
    """A model with exactly one row, always at pk=1."""

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        self.pk = 1
        super().save(*args, **kwargs)
        cache.delete(CACHE_KEY)

    def delete(self, *args, **kwargs):
        """Deleting the configuration row is never correct, so it is a no-op."""
        return

    @classmethod
    def load(cls):
        obj, _ = cls.objects.get_or_create(pk=1)
        return obj


class BusinessConfig(SingletonModel):
    """The single row holding every operator-editable business setting."""

    # -- Branding ----------------------------------------------------------
    # Deliberately not hardcoded anywhere: the business name and logo are
    # still undecided, and every template reads them from here.
    business_name = models.CharField(
        max_length=120,
        default="Studio Name",
        help_text="Shown in the site header, page titles and outgoing email.",
    )
    tagline = models.CharField(
        max_length=200,
        blank=True,
        default="Custom CAD design and 3D printing",
        help_text="One line, shown under the business name on the home page.",
    )

    # -- Contact -----------------------------------------------------------
    support_email = models.EmailField(
        default="hello@example.com",
        help_text="Where clients are told to reach you. Not the sending address.",
    )
    phone = models.CharField(max_length=40, blank=True)
    pickup_address = models.TextField(
        blank=True,
        help_text="Shown to clients who choose pickup instead of delivery.",
    )

    # -- Money -------------------------------------------------------------
    # Stored as a rate rather than a percentage: 0.0725 means 7.25%.
    # Each quote snapshots the rate in force when it was issued, so editing
    # this never rewrites the arithmetic on an order that already exists.
    tax_rate = models.DecimalField(
        max_digits=6,
        decimal_places=4,
        default=Decimal("0.0725"),
        validators=[MinValueValidator(Decimal("0")), MaxValueValidator(Decimal("1"))],
        help_text="Sales tax as a decimal rate. 0.0725 is 7.25%.",
    )
    delivery_base_fee_cents = models.PositiveIntegerField(
        default=1500,
        help_text="Flat courier fee in cents, added to delivery orders.",
    )

    # -- Order limits ------------------------------------------------------
    # Validation reads these, so raising a limit is a form edit rather than a
    # migration.
    max_print_files = models.PositiveSmallIntegerField(
        default=10,
        help_text="Maximum distinct model files on one printing order.",
    )
    max_item_quantity = models.PositiveSmallIntegerField(
        default=100,
        help_text="Maximum quantity of any single item.",
    )
    max_upload_mb = models.PositiveSmallIntegerField(
        default=100,
        help_text="Largest accepted single file, in megabytes.",
    )

    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Business configuration"
        verbose_name_plural = "Business configuration"

    def __str__(self):
        return self.business_name

    @property
    def tax_rate_percent(self) -> Decimal:
        """The tax rate as a percentage, for display."""
        return (self.tax_rate * 100).quantize(Decimal("0.01"))

    @property
    def max_upload_bytes(self) -> int:
        return self.max_upload_mb * 1024 * 1024

    @classmethod
    def cached(cls):
        """
        The configuration as read on every page render.

        Cached because it is needed by the base template on every request and
        changes perhaps a few times a year.
        """
        config = cache.get(CACHE_KEY)
        if config is None:
            config = cls.load()
            cache.set(CACHE_KEY, config, CACHE_TTL)
        return config
