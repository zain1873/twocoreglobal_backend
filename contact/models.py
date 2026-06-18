from django.db import models


class ContactSubmission(models.Model):
    INTEREST_CHOICES = [
        ("Website", "Website"),
        ("SEO", "SEO"),
        ("Branding", "Branding"),
        ("Google Ads", "Google Ads"),
        ("Meta Ads", "Meta Ads"),
        ("CRM & Automation", "CRM & Automation"),
        ("Other", "Other"),
    ]
    BUDGET_CHOICES = [
        ("Under $2,000", "Under $2,000"),
        ("$2,000 – $5,000", "$2,000 – $5,000"),
        ("$5,000 – $10,000", "$5,000 – $10,000"),
        ("$10,000+", "$10,000+"),
        ("Let's Discuss", "Let's Discuss"),
    ]
    HEAR_CHOICES = [
        ("Google Search", "Google Search"),
        ("Social Media", "Social Media"),
        ("Referral", "Referral"),
        ("Advertisement", "Advertisement"),
        ("Other", "Other"),
    ]

    full_name = models.CharField(max_length=150)
    email = models.EmailField()
    phone = models.CharField(max_length=30)
    company_name = models.CharField(max_length=150, blank=True)
    designation = models.CharField(max_length=150, blank=True)
    hear_about = models.CharField(max_length=30, choices=HEAR_CHOICES, blank=True)
    message = models.TextField()
    interests = models.JSONField(default=list, blank=True)
    budget = models.CharField(max_length=30, choices=BUDGET_CHOICES, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.full_name} <{self.email}> — {self.created_at:%Y-%m-%d}"
