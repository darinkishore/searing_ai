from rest_framework import serializers
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

class DocumentSerializer(serializers.ModelSerializer):

    # link to the user who created the document
    user = serializers.HyperlinkedRelatedField(
        read_only=True,
        view_name='api:users-detail'
    )

    class Meta:
        model = Document
        fields = ('id', 'file', 'created_at', 'title', 'updated_at', 'user', 'summary', 'questions')

    def create(self, validated_data):
        document = Document.objects.create(**validated_data)
        return document

class SummarySerializer(serializers.ModelSerializer):

    # link to the document that the summary is for
    document = serializers.HyperlinkedRelatedField(
        read_only=True,
        view_name='api:documents-detail'
    )

    class Meta:
        model = Summary
        fields = ['id', 'document', 'content', 'created_at', 'updated_at']

class QuestionSerializer(serializers.ModelSerializer):

    # link to the document that the question is for
    document = serializers.HyperlinkedRelatedField(
        read_only=True,
        view_name='api:documents-detail'
    )

    class Meta:
        model = Question
        fields = ['id', 'document', 'question', 'answer', 'created_at', 'updated_at']