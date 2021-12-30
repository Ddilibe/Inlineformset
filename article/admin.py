from django.contrib import admin
from .models import Article, Add_image, Add_video, Add_body


class Add_videoInlineAdmin(admin.TabularInline):
    model = Add_video
    
class Add_imageInlineAdmin(admin.TabularInline):
    model = Add_image
    
class Add_bodyInlineAdmin(admin.TabularInline):
    model = Add_body
    
class ArticleAdmin(admin.ModelAdmin):
    inlines = [Add_bodyInlineAdmin,Add_imageInlineAdmin,Add_videoInlineAdmin]
    prepopulated_fields = {'slug': ('title', )}

admin.site.register(Article,ArticleAdmin)

