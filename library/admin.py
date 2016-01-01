from django.contrib import admin
from django.apps import apps
from .models import Video

for model in apps.get_app_config('library').get_models():
    if model == Video:
        @admin.register(Video)
        class VideoAdmin(admin.ModelAdmin):
            raw_id_fields = ("maker", "label", "series", "director", "actresses", "keywords")
            search_fields = [ "%s__name" % f for f in raw_id_fields ]
    else:
        admin.site.register(model)
