from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from .models import AncRequest
from .serializers import AncRequestSerializer


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def GetRequestsOnAnnouncement(request, anc_id):
    anc_requests = AncRequest.objects.filter(req_anc=anc_id)
    serializer = AncRequestSerializer(anc_requests, many=True)
    return Response(serializer.data)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def GetRequestsOfHost(request, host_id):
    anc_requests = AncRequest.objects.filter(host=host_id)
    serializer = AncRequestSerializer(anc_requests, many=True)
    return Response(serializer.data)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def CreateRequest(request, anc_id):
    serializer = AncRequestSerializer(data=request.data, context={"request" : request, "anc_id" : anc_id})

    if serializer.is_valid():
        serializer.save()
    return Response(serializer.data)


