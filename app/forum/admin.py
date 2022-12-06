from django.contrib import admin
from django.template.loader import render_to_string
from django.utils.safestring import mark_safe
from forum.models import Entry, EntryFile, User, Thread


class UserAdmin(admin.ModelAdmin):
    list_display = ('identifier', 'display_name', 'created_at')
    readonly_fields = ('identifier', 'display_name', 'created_at', 'identicon_image')

    def identicon_image(self, obj):
        return mark_safe('<img src="{url}" width="{width}" height={height} />'.format(
                url=obj.identicon.url,
                width=obj.identicon.width,
                height=obj.identicon.height,
            )
        )

    identicon_image.allow_tags = True


class EntryInstanceInline(admin.TabularInline):
    model = Entry


class EntryFileInstanceInline(admin.TabularInline):
    model = EntryFile


class EntryAdmin(admin.ModelAdmin):
    list_display = ('creator', 'thread', 'creation_date', 'was_popularity_calculated', 'attachments')
    inlines = [EntryFileInstanceInline]

    def attachments(self, obj):
        return [
            file
            for file in obj.attached_files
        ]


class ThreadAdmin(admin.ModelAdmin):
    list_display = ('title', 'entries_amount', 'created_date', 'all_files_size_mb')

    inlines = [EntryInstanceInline]


class EntryFileAdmin(admin.ModelAdmin):
    list_display = ('original_file', 'compressed_file', 'size', 'as_link', 'interactive')
    readonly_fields = ('original_file', 'compressed_file', 'size', 'as_link', 'interactive')

    def as_link(self, obj: EntryFile):
        return mark_safe('<a href="{url}"/>{filename}</a>'.format(
                url=com.url if (com := obj.compressed_file) else obj.original_file.url,
                filename=obj.original_file,
            )
        )

    def size(self, obj: EntryFile):
        return f'{obj.original_file.size} Bytes'

    def interactive(self, obj: EntryFile):
        return render_to_string("components/displayable_file.html", context={"file": obj})

    as_link.allow_tags = True
    interactive.allow_tags = True

    # inlines = [ReverseEntryInstanceInline]


admin.site.register(User, UserAdmin)
admin.site.register(Thread, ThreadAdmin)
admin.site.register(Entry, EntryAdmin)
admin.site.register(EntryFile, EntryFileAdmin)
