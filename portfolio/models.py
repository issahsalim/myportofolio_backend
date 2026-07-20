from django.db import models

class PersonalInfo(models.Model):
    name = models.CharField(max_length=100)
    role = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    location = models.CharField(max_length=100)
    linkedin = models.URLField(blank=True, null=True)
    github = models.URLField(blank=True, null=True)
    youtube = models.URLField(blank=True, null=True)
    bio = models.TextField()
    resume = models.FileField(upload_to='resumes/', blank=True, null=True)
    profile_image = models.ImageField(upload_to='profile/', blank=True, null=True)

    class Meta:
        verbose_name_plural = "Personal Info"

    def __str__(self):
        return self.name

class Skill(models.Model):
    CATEGORY_CHOICES = [
        ('Frontend', 'Frontend'),
        ('Backend', 'Backend'),
        ('AI_ML', 'AI & Machine Learning'),
        ('Tools_Other', 'Tools & Other'),
    ]
    name = models.CharField(max_length=100)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, db_index=True)
    level = models.IntegerField(default=80, help_text="Skill level percentage (0 to 100)")
    order = models.IntegerField(default=0, help_text="Display order", db_index=True)

    class Meta:
        ordering = ['order', 'category', 'name']

    def __str__(self):
        return f"{self.name} ({self.category})"

class Project(models.Model):
    title = models.CharField(max_length=200)
    subtitle = models.CharField(max_length=200, blank=True, null=True)
    description = models.TextField()
    tech_stack = models.CharField(max_length=500, help_text="Comma-separated values, e.g. Django, React, PostgreSQL")
    live_url = models.URLField(blank=True, null=True)
    github_url = models.URLField(blank=True, null=True)
    image = models.ImageField(upload_to='projects/', blank=True, null=True)
    order = models.IntegerField(default=0, help_text="Display order", db_index=True)

    class Meta:
        ordering = ['order', 'title']

    def __str__(self):
        return self.title

class ContactMessage(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    subject = models.CharField(max_length=200)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Message from {self.name} - {self.subject}"
