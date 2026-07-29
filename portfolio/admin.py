from django.contrib import admin
from .models import PersonalInfo, Skill, Project, ContactMessage, Testimonial

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

@admin.register(Testimonial)
class TestimonialAdmin(admin.ModelAdmin):
    list_display = ('name', 'title', 'email', 'rating', 'is_approved', 'created_at')
    list_editable = ('is_approved',)
    list_filter = ('rating', 'is_approved', 'created_at')
    search_fields = ('name', 'title', 'email', 'comment')
    actions = ['approve_testimonials', 'unapprove_testimonials']


    @admin.action(description="Approve selected testimonials for frontend display")
    def approve_testimonials(self, request, queryset):
        updated = queryset.update(is_approved=True)
        self.message_user(request, f"{updated} testimonial(s) successfully approved.")

    @admin.action(description="Unapprove selected testimonials")
    def unapprove_testimonials(self, request, queryset):
        updated = queryset.update(is_approved=False)
        self.message_user(request, f"{updated} testimonial(s) unapproved.")

