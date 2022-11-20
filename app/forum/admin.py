from django.contrib import admin
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
    list_display = ('size', 'as_link', 'as_image')
    readonly_fields = ('size', 'as_link', 'as_image')

    def as_link(self, obj):
        return mark_safe('<a href="{url}"/>{filename}</a>'.format(
                url=obj.original_file.url,
                filename=obj.original_file,
            )
        )

    def size(self, obj: EntryFile):
        return f'{obj.original_file.size}B'

    def as_image(self, obj):
        return mark_safe('<img src="{url}"/>'.format(
                url=obj.original_file.url,
            )
        )

    as_link.allow_tags = True
    as_image.allow_tags = True

    # inlines = [ReverseEntryInstanceInline]


admin.site.register(User, UserAdmin)
admin.site.register(Thread, ThreadAdmin)
admin.site.register(Entry, EntryAdmin)
admin.site.register(EntryFile, EntryFileAdmin)
