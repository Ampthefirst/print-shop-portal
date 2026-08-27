from django.contrib import admin
from django.http import HttpResponseRedirect
from django.urls import reverse

from .models import BusinessConfig


@admin.register(BusinessConfig)
class BusinessConfigAdmin(admin.ModelAdmin):
    """
    Single-row admin. Adding and deleting are disabled, and the changelist
    redirects straight to the one record so there is never an empty list to
    puzzle over.
    """

    fieldsets = (
        ("Branding", {"fields": ("business_name", "tagline")}),
        ("Contact", {"fields": ("support_email", "phone", "pickup_address")}),
        (
            "Pricing",
            {
                "fields": ("tax_rate", "delivery_base_fee_cents"),
                "description": (
                    "Tax is stored as a decimal rate, so 7.25% is entered as "
                    "0.0725. Quotes record the rate in force when they were "
                    "issued, so changing this never alters an existing order."
                ),
            },
        ),
        (
            "Order limits",
            {"fields": ("max_print_files", "max_item_quantity", "max_upload_mb")},
        ),
    )
    readonly_fields = ("updated_at",)

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    def changelist_view(self, request, extra_context=None):
        config = BusinessConfig.load()
        return HttpResponseRedirect(
            reverse("admin:core_businessconfig_change", args=[config.pk])
        )
