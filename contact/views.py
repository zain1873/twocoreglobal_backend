from django.conf import settings
from django.core.mail import send_mail
from rest_framework import generics, permissions

from .models import ContactSubmission
from .serializers import ContactSubmissionSerializer


class ContactSubmissionCreateView(generics.CreateAPIView):
    queryset = ContactSubmission.objects.all()
    serializer_class = ContactSubmissionSerializer
    permission_classes = [permissions.AllowAny]

    def perform_create(self, serializer):
        instance = serializer.save()
        send_mail(
            subject=f"New contact form submission — {instance.full_name}",
            message=(
                f"Name: {instance.full_name}\n"
                f"Email: {instance.email}\n"
                f"Phone: {instance.phone}\n"
                f"Company: {instance.company_name}\n"
                f"Budget: {instance.budget}\n"
                f"Interests: {', '.join(instance.interests)}\n\n"
                f"Message:\n{instance.message}"
            ),
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[settings.CONTACT_NOTIFICATION_EMAIL],
            fail_silently=True,
        )
        send_mail(
            subject="We've received your request — Two Core Global",
            message=(
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
            recipient_list=[instance.email],
            fail_silently=True,
        )
