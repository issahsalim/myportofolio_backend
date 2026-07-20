from django.contrib import admin
from .models import PersonalInfo, Skill, Project, ContactMessage

@admin.register(PersonalInfo)
class PersonalInfoAdmin(admin.ModelAdmin):
    list_display = ('name', 'role', 'email', 'phone', 'location')
    
    def has_add_permission(self, request):
        # Limit to only 1 profile row in the DB
        if self.model.objects.exists():
            return False
        return True

@admin.register(Skill)
class SkillAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'level', 'order')
    list_editable = ('level', 'order')
    list_filter = ('category',)
    search_fields = ('name',)

@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('title', 'subtitle', 'order')
    list_editable = ('order',)
    search_fields = ('title', 'tech_stack', 'description')

@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'subject', 'created_at')
    readonly_fields = ('name', 'email', 'subject', 'message', 'created_at')
    
    def has_add_permission(self, request):
        # Messages should only come from frontend form submissions
        return False
