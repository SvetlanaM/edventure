from django.contrib import admin
from hellodjango.helloapp.models import UnknownUser, Author, Source, Type, Category, Content, ContentDetail, ContentUser, UserDetail, Comment

class ContentAdmin(admin.ModelAdmin):
    list_display = ('title', 'created_at', 'video')
    list_filter = ('created_at', 'title',)
    date_hierarchy = 'created_at'
    ordering = ('created_at',)
    prepopulated_fields = {"slug" : ("title",)}
    
class ContentDetailAdmin(admin.ModelAdmin) :
    list_display = ('link', 'start_course', 'start_is', 'workload')
    date_hierarchy = 'start_course'
    
class UserDetailAdmin(admin.ModelAdmin) :
    list_display = ('user', 'slug',)
    prepopulated_fields = {"slug" : ("user",)}
class AuthorAdmin(admin.ModelAdmin):
    list_display =('last_name','first_name',)
    search_field =('last_name',)
    prepopulated_fields = {"slug" : ("last_name", "first_name",)}

class SourceAdmin(admin.ModelAdmin) :
    list_display=('source',)
    prepopulated_fields = {"slug" : ("source",)}

class TypeAdmin(admin.ModelAdmin) :
    list_display=('description',)
    prepopulated_fields = {"slug" : ("description",)}

class CategoryAdmin(admin.ModelAdmin) :
    list_display = ('name',)
    prepopulated_fields = {"slug" : ("name",)}
    fields = ('name', 'slug', 'tags', )

class ContentUserAdmin(admin.ModelAdmin) :
    list_display = ('my_list_choices', 'user',)
    prepopulated_fields = {"slug" : ("title",)}

class CommentAdmin(admin.ModelAdmin) :
    list_display = ('post', 'author' , 'comment', 'parent', 'added',)
    
admin.site.register(UnknownUser)
admin.site.register(Author, AuthorAdmin)
admin.site.register(Source, SourceAdmin)
admin.site.register(Type, TypeAdmin)
admin.site.register(TagItem)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Content, ContentAdmin)
admin.site.register(ContentDetail, ContentDetailAdmin)
admin.site.register(ContentUser, ContentUserAdmin)
admin.site.register(UserDetail, UserDetailAdmin)
admin.site.register(Comment, CommentAdmin)
