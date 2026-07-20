from django.shortcuts import render
from portfolio.models import PersonalInfo, Skill, Project, ContactMessage

def home_view(request):
    """
    Renders the Django backend landing page at root URL
    """
    personal = PersonalInfo.objects.first()
    personal_count = PersonalInfo.objects.count()
    skill_count = Skill.objects.count()
    project_count = Project.objects.count()
    message_count = ContactMessage.objects.count()

    context = {
        'personal': personal,
        'personal_count': personal_count,
        'skill_count': skill_count,
        'project_count': project_count,
        'message_count': message_count,
    }
    return render(request, 'index.html', context)

def custom_404_view(request, exception=None):
    """
    Custom 404 handler for non-existent backend URLs.
    """
    return render(request, '404.html', status=404)
