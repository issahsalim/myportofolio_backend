import logging
import threading
from django.shortcuts import render
from django.core.mail import send_mail
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from rest_framework import viewsets, mixins, status, permissions
from rest_framework.response import Response
from .models import PersonalInfo, Skill, Project, ContactMessage, Testimonial
from .serializers import (
    PersonalInfoSerializer,
    SkillSerializer,
    ProjectSerializer,
    ContactMessageSerializer,
    TestimonialSerializer,
)

logger = logging.getLogger(__name__)

def _send_contact_emails_async(instance):

    try:
        # 1. Confirmation email to client 
        client_subject = f"Message Received | Issah Abdulsalim Boresa"
        client_body = (
            f"Dear {instance.name},\n\n"
            f"Thank you for reaching out to me \n\n"
            f"I have received your message regarding \"{instance.subject or 'your inquiry'}\". "
            f"I appreciate you taking the time to get in touch, and I will review your message and get back to you shortly.\n\n"
            f"If you have any urgent details to share, feel free to reply directly to this email or reach out via phone/WhatsApp at (059) 6878044.\n\n"
            f"Warm regards,\n\n"
            f"Issah Abdulsalim Boresa\n"
            f"Technology Optimist\n"
            f"Email: issahsalim233@gmail.com | issah.boresa.stu@uenr.edu.gh\n"
            f"Phone: (059) 6878044\n"
        )
        
        # 2. Notification email to Issah
        admin_subject = f"🔔 New Portfolio Message from {instance.name}"
        admin_body = (
            f"You received a new message from your portfolio website!\n\n"
            f"From: {instance.name} ({instance.email})\n"
            f"Subject: {instance.subject or 'N/A'}\n\n"
            f"Message:\n{instance.message}\n"
        )

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
        logger.error(f"Failed to dispatch contact email asynchronously: {e}")


def _send_testimonial_emails_async(instance):
    """
    Sends automated professional & friendly thank-you email to the client (if email provided)
    and notifies admin about the new testimonial submission.
    """
    try:
        # 1. Thank-you email to client if email was provided
        if instance.email:
            client_subject = "Thank You for Your Feedback! | Issah Abdulsalim Boresa"
            client_body = (
                f"Dear {instance.name},\n\n"
                f"Thank you so much for taking the time to share your feedback and testimonial about our work together!\n\n"
                f"Your words and support mean a lot to me. Your feedback has been received and will be reviewed shortly. \n\n"
                f"I truly enjoyed collaborating with you and look forward to working together again in the future!\n\n"
                f"Warm regards,\n\n"
                f"Issah Abdulsalim Boresa\n"
                f"Technology Optimist\n"
                f"Email: issahsalim233@gmail.com | issah.boresa.stu@uenr.edu.gh\n"
                f"Phone: (059) 6878044\n"
            )

            send_mail(
                subject=client_subject,
                message=client_body,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[instance.email],
                fail_silently=True,
            )

        # 2. Notification email to Admin
        admin_subject = f"⭐ New Testimonial Submitted by {instance.name}"
        admin_body = (
            f"You received a new client testimonial!\n\n"
            f"Name: {instance.name}\n"
            f"Title/Role: {instance.title}\n"
            f"Email: {instance.email or 'Not provided'}\n\n"
            f"Comment:\n{instance.comment}\n\n"
            f"Status: Pending Approval\n"
            f"Log into Django Admin to approve this testimonial for frontend display.\n"
        )

        send_mail(
            subject=admin_subject,
            message=admin_body,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=['issahsalim233@gmail.com'],
            fail_silently=True,
        )
    except Exception as e:
        logger.error(f"Failed to dispatch testimonial email asynchronously: {e}")


def submit_testimonial_view(request):
    """
    Renders and handles submission for the client testimonial form.
    Clients access this page on the backend project.
    """
    context = {}

    if request.method == 'POST':
        name = request.POST.get('name', '').strip()
        title = request.POST.get('title', '').strip()
        email = request.POST.get('email', '').strip()
        comment = request.POST.get('comment', '').strip()
        image = request.FILES.get('image')

        try:
            rating = int(request.POST.get('rating', 5))
            if rating < 1 or rating > 5:
                rating = 5
        except (ValueError, TypeError):
            rating = 5

        if not name or not title or not comment:
            context['error_message'] = "Please fill in all required fields (Name, Title/Role, and Comment)."
        else:
            testimonial = Testimonial.objects.create(
                name=name,
                title=title,
                email=email if email else None,
                rating=rating,
                comment=comment,
                image=image,
                is_approved=False # Pending admin approval
            )

            # Trigger background email task
            threading.Thread(
                target=_send_testimonial_emails_async,
                args=(testimonial,),
                daemon=True
            ).start()

            context['success_message'] = "Your feedback has been submitted successfully and is pending review. Thank you for your support!"

    return render(request, 'testimonial_form.html', context)


class PersonalInfoViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Exposes personal info. Lists return the single active profile.
    Time Complexity: O(1) (database query is limit 1, returning single record).
    """
    queryset = PersonalInfo.objects.all()
    serializer_class = PersonalInfoSerializer
    permission_classes = [permissions.AllowAny]

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
    permission_classes = [permissions.AllowAny]

class ProjectViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Exposes projects ordered by priority.
    Time Complexity: O(N) where N is number of projects.
    """
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    permission_classes = [permissions.AllowAny]


class TestimonialViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Exposes ONLY approved testimonials for frontend display.
    Time Complexity: O(N) where N is number of approved testimonials.
    Index on `is_approved` ensures fast O(log N) lookup.
    """
    queryset = Testimonial.objects.filter(is_approved=True)
    serializer_class = TestimonialSerializer
    permission_classes = [permissions.AllowAny]


@method_decorator(csrf_exempt, name='dispatch')
class ContactMessageViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):
    """
    Allows guest users to post message submissions.
    Bypasses CSRF checking and dispatches emails asynchronously in background thread so HTTP response returns instantly.
    Time Complexity: O(1) for database insert.
    """
    queryset = ContactMessage.objects.all()
    serializer_class = ContactMessageSerializer
    permission_classes = [permissions.AllowAny]
    authentication_classes = []

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        try:
            self.perform_create(serializer)
            headers = self.get_success_headers(serializer.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
        except Exception as e:
            logger.error(f"Error saving contact message: {e}", exc_info=True)
            return Response(
                {"detail": f"Message processing error: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    def perform_create(self, serializer):
        instance = serializer.save()
        # Non-blocking async email dispatch thread
        threading.Thread(target=_send_contact_emails_async, args=(instance,), daemon=True).start()




