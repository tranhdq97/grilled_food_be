from rest_framework import serializers


class MasterBaseSlz(serializers.Serializer):
    id = serializers.IntegerField(required=False)
    name = serializers.CharField(max_length=255)


class MasterBaseCreateSlz(serializers.Serializer):
    name = serializers.CharField(max_length=255)


# -------------------------------------------- Params
class MasterBaseListReqParams(serializers.Serializer):
    parent_id = serializers.IntegerField(required=False)
