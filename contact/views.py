from django.conf import settings
from django.core.mail import EmailMessage
from rest_framework import generics, permissions

from .models import ContactSubmission
from .serializers import ContactSubmissionSerializer


class ContactSubmissionCreateView(generics.CreateAPIView):
    queryset = ContactSubmission.objects.all()
    serializer_class = ContactSubmissionSerializer
    permission_classes = [permissions.AllowAny]

    def perform_create(self, serializer):
        instance = serializer.save()
        EmailMessage(
            subject=f"New contact form submission — {instance.full_name}",
            body=(
                f"Name: {instance.full_name}\n"
                f"Email: {instance.email}\n"
                f"Phone: {instance.phone}\n"
                f"Company: {instance.company_name}\n"
                f"Budget: {instance.budget}\n"
                f"Interests: {', '.join(instance.interests)}\n\n"
                f"Message:\n{instance.message}"
            ),
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=[settings.CONTACT_NOTIFICATION_EMAIL],
            reply_to=[instance.email],
        ).send(fail_silently=True)
        EmailMessage(
            subject="We've received your request — Two Core Global",
            body=(
                f"Hi {instance.full_name},\n\n"
                "Thank you for reaching out to Two Core Global. We've received "
                "your request and one of our experts will contact you soon.\n\n"
                "Here's a copy of what you submitted:\n\n"
                f"Phone: {instance.phone}\n"
                f"Message:\n{instance.message}\n\n"
                "Best regards,\n"
                "Two Core Global Team"
            ),
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=[instance.email],
            reply_to=[settings.CONTACT_NOTIFICATION_EMAIL],
        ).send(fail_silently=True)
