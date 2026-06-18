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
