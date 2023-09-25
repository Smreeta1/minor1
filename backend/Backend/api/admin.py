from django.contrib import admin
from .models import citizen, driver

class CitizenDriverAdmin(admin.ModelAdmin):
    list_display = ("first_name","last_name", "address", "email", "citizenship_no")
    search_fields = ("first_name","last_name", "email", "citizenship_no")
    list_filter = ("address",)
    
    def get_queryset(self, request):
        # Combine both citizen and driver objects
        return super().get_queryset(request).union(
            citizen.objects.all(),
            driver.objects.all()
        )

admin.site.register(citizen, CitizenDriverAdmin)
admin.site.register(driver, CitizenDriverAdmin)
