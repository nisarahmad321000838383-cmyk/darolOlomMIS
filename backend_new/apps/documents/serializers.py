"""
Serializers for documents app
"""
from rest_framework import serializers
from .models import Document


class DocumentSerializer(serializers.ModelSerializer):
    """Serializer for Document model"""
    document_type_display = serializers.CharField(source='get_document_type_display', read_only=True)
    uploaded_by_name = serializers.CharField(source='uploaded_by.name', read_only=True)
    verified_by_name = serializers.CharField(source='verified_by.name', read_only=True)
    file_name = serializers.CharField(read_only=True)
    file_size = serializers.FloatField(read_only=True)
    file_extension = serializers.CharField(read_only=True)
    file_url = serializers.SerializerMethodField()

    class Meta:
        model = Document
        fields = [
            'id', 'title', 'description', 'document_type', 'document_type_display',
            'file', 'file_url', 'file_name', 'file_size', 'file_extension',
            'student', 'teacher', 'uploaded_by', 'uploaded_by_name',
            'is_verified', 'verified_by', 'verified_by_name', 'verified_at',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'uploaded_by', 'verified_by', 'verified_at', 'created_at', 'updated_at']

    def get_file_url(self, obj):
        request = self.context.get('request')
        if obj.file and request:
            return request.build_absolute_uri(obj.file.url)
        return None


class DocumentCreateSerializer(serializers.ModelSerializer):
    """Serializer for creating documents"""
    class Meta:
        model = Document
        fields = ['title', 'description', 'document_type', 'file', 'student', 'teacher']

    def validate(self, data):
        # Document must belong to either student or teacher, not both or neither
        student = data.get('student')
        teacher = data.get('teacher')
        
        if student and teacher:
            raise serializers.ValidationError(
                'سند نمی‌تواند هم به دانش‌آموز و هم به استاد تعلق داشته باشد'
            )
        
        if not student and not teacher:
            # Allow general documents (not belonging to anyone)
            pass
        
        return data

    def validate_file(self, value):
        # Check file size (max 10MB)
        if value.size > 10 * 1024 * 1024:
            raise serializers.ValidationError('حجم فایل نباید بیشتر از 10 مگابایت باشد')
        
        return value


class DocumentVerifySerializer(serializers.Serializer):
    """Serializer for verifying documents"""
    is_verified = serializers.BooleanField()
