from django.contrib import admin
from main.models import Cars, Specializations, Crafts, Governorates, Zones, Workshops, Images, Contacts, Comments, Rates, Subscribe

class ImagesInline(admin.TabularInline):
    model = Images
    max_num=10
    extra=1


class ContactsInline(admin.TabularInline):
    model = Contacts
    max_num=10
    extra=1


class WorkshopsAdmin(admin.ModelAdmin):
    inlines = [ContactsInline, ImagesInline]
    list_display = ('name', 'owner', 'timestamp')   # for sorting by
    search_fields = ('name', 'owner')               # for searching
    list_filter = ('timestamp', 'is_visible')       # for filtering data by
    ordering = ('-timestamp',)                      # for ordering
    filter_horizontal = ('cars', 'specializations', 'crafts') # instead of multi-select option

models = [
    Cars,
    Specializations,
    Crafts,
    Governorates,
    Zones,
    Contacts,   ## ..............
    Images,      ## ..............
    Comments,
    Rates, 
    Subscribe
]

admin.site.register(models)
admin.site.register(Workshops ,WorkshopsAdmin)