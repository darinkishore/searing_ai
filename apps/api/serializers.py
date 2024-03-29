from rest_framework import serializers
from rest_framework.serializers import PrimaryKeyRelatedField
from rest_framework_api_key.models import APIKey



from apps.users.models import CustomUser
from apps.data.models import Document, Summary, Question

class UserSerializer(serializers.ModelSerializer):

    # define a document link with the documents for the current user
    documents = serializers.HyperlinkedRelatedField(
        many=True,
        read_only=True,
        view_name='api:documents-detail'
    )

    class Meta:
        model = CustomUser
        fields = ['id', 'email', 'documents',
                  'is_superuser', 'date_joined', 'last_login']


class DocumentFormSerializer(serializers.ModelSerializer):
    def create(self, validated_data):
        return Document.objects.create(**validated_data)

    def validate(self, data):
        instance = Document(**data)
        instance.full_clean()
        return data

    class Meta:
        model = Document
        fields = ['file', 'title']


class DocumentSerializer(serializers.ModelSerializer):

    # link to the user who created the document
    user = serializers.HyperlinkedRelatedField(
        read_only=True,
        view_name='api:users-detail'
    )

    def create(self, validated_data):
        return Document.objects.create(**validated_data)

    def validate(self, data):
        instance = Document(**data)
        instance.full_clean()
        return data

    class Meta:
        model = Document
        fields = ['id', 'file', 'created_at', 'title', 'updated_at', 'user',
                  'summary', 'questions', 'ocr_text']


class SummarySerializer(serializers.ModelSerializer):

    # link to the document that the summary is for
    document = serializers.HyperlinkedRelatedField(
        read_only=True,
        view_name='api:documents-detail',
        allow_null=True
    )

    class Meta:
        model = Summary
        fields = ['id', 'document', 'content', 'created_at', 'updated_at']

class QuestionSerializer(serializers.ModelSerializer):

    # link to the document that the question is for
    document = serializers.HyperlinkedRelatedField(
        read_only=True,
        view_name='api:documents-detail',
        allow_null=True
    )

    class Meta:
        model = Question
        fields = ['id', 'document', 'question', 'answer', 'created_at', 'updated_at']
