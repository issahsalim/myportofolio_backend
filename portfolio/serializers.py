from rest_framework import serializers
from .models import PersonalInfo, Skill, Project, ContactMessage

class PersonalInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = PersonalInfo
        fields = '__all__'

class SkillSerializer(serializers.ModelSerializer):
    class Meta:
        model = Skill
        fields = '__all__'

class ProjectSerializer(serializers.ModelSerializer):
    tech_list = serializers.SerializerMethodField()

    class Meta:
        model = Project
        fields = ['id', 'title', 'subtitle', 'description', 'tech_stack', 'tech_list', 'live_url', 'github_url', 'image', 'order']

    def get_tech_list(self, obj):
        # O(T) complexity where T is the length of tech_stack string
        if obj.tech_stack:
            return [tech.strip() for tech in obj.tech_stack.split(',') if tech.strip()]
        return []

class ContactMessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContactMessage
        fields = '__all__'
