from rest_framework import serializers

from .models import ContactSubmission

INTEREST_VALUES = [c[0] for c in ContactSubmission.INTEREST_CHOICES]


class ContactSubmissionSerializer(serializers.ModelSerializer):
    interests = serializers.ListField(
        child=serializers.ChoiceField(choices=INTEREST_VALUES),
        required=False,
        default=list,
    )

    class Meta:
        model = ContactSubmission
        fields = [
            "id", "full_name", "email", "phone", "company_name",
            "designation", "hear_about", "message", "interests",
            "budget", "created_at",
        ]
        read_only_fields = ["id", "created_at"]
