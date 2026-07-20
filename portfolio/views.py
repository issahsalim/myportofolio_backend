import logging
from django.core.mail import send_mail
from django.conf import settings
from rest_framework import viewsets, mixins
from rest_framework.response import Response
from .models import PersonalInfo, Skill, Project, ContactMessage
from .serializers import PersonalInfoSerializer, SkillSerializer, ProjectSerializer, ContactMessageSerializer

logger = logging.getLogger(__name__)

class PersonalInfoViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Exposes personal info. Lists return the single active profile.
    Time Complexity: O(1) (database query is limit 1, returning single record).
    """
    queryset = PersonalInfo.objects.all()
    serializer_class = PersonalInfoSerializer

    def list(self, request, *args, **kwargs):
        instance = self.queryset.first()
        if instance:
            serializer = self.get_serializer(instance)
            return Response(serializer.data)
        return Response({})

class SkillViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Exposes skills ordered by priority.
    Time Complexity: O(N) where N is number of skills.
    """
    queryset = Skill.objects.all()
    serializer_class = SkillSerializer

class ProjectViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Exposes projects ordered by priority.
    Time Complexity: O(N) where N is number of projects.
    """
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer

class ContactMessageViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):
    """
    Allows guest users to post message submissions.
    Automatically dispatches:
    1. A friendly professional confirmation email to the client.
    2. A notification email to Issah's inbox (issahsalim233@gmail.com).
    Time Complexity: O(1) for database inserts and email dispatch.
    """
    queryset = ContactMessage.objects.all()
    serializer_class = ContactMessageSerializer

    def perform_create(self, serializer):
        instance = serializer.save()
        
        # 1. Confirmation email to client
        client_subject = f"Message Received | Issah Abdulsalim Boresa"
        client_body = (
            f"Dear {instance.name},\n\n"
            f"Thank you for reaching out to me through my portfolio website!\n\n"
            f"I have received your message regarding \"{instance.subject or 'your inquiry'}\". "
            f"I appreciate you taking the time to get in touch, and I will review your message and get back to you shortly.\n\n"
            f"If you have any urgent details to share, feel free to reply directly to this email or reach out via phone/WhatsApp at (059) 6878044.\n\n"
            f"Warm regards,\n\n"
            f"Issah Abdulsalim Boresa\n"
            f"Full-Stack & Machine Learning Developer\n"
            f"Email: issahsalim233@gmail.com | issah.boresa.stu@uenr.edu.gh\n"
            f"Phone: (059) 6878044\n"
        )
        
        # 2. Notification email to Issah
        admin_subject = f"🔔 New Portfolio Message from {instance.name}"
        admin_body = (
            f"You received a new message from your portfolio website!\n\n"
            f"From: {instance.name} ({instance.email})\n"
            f"Subject: {instance.subject}\n\n"
            f"Message:\n{instance.message}\n"
        )

        try:
            # Send client confirmation
            send_mail(
                subject=client_subject,
                message=client_body,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[instance.email],
                fail_silently=True,
            )

            # Send admin notification
            send_mail(
                subject=admin_subject,
                message=admin_body,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=['issahsalim233@gmail.com'],
                fail_silently=True,
            )
        except Exception as e:
            logger.error(f"Failed to dispatch contact email: {e}")
