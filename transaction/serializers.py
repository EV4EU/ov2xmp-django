from rest_framework import serializers
from transaction.models import Transaction
from connector.models import Connector
from connector.serializers import ConnectorSerializer
from api.serializers import RelatedFieldAlternative


class TransactionSerializer(serializers.ModelSerializer):
    id_tag = serializers.SlugRelatedField(many=False, read_only=True, slug_field="idToken")
    connector = RelatedFieldAlternative(queryset=Connector.objects.all(), serializer=ConnectorSerializer)

    class Meta:
        model = Transaction
        fields = "__all__"
