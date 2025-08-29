from django.http import JsonResponse

from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view

from .models import Conversation, ConversationMessage
from .serializers import ConversationListSerializer, ConversationDetailSerializer, ConversationMessageSerializer
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from useraccount.models import User


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def conversations_list(request):
    conversations = request.user.conversations.prefetch_related('users').all()
    serializer = ConversationListSerializer(request.user.conversations.all(), many=True)
    return JsonResponse(serializer.data, safe=False)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def conversations_detail(request, pk):
    conversation = get_object_or_404(request.user.conversations.prefetch_related('messages__created_by', 'messages__sent_to'), pk=pk)
    conversation_serializer = ConversationDetailSerializer(conversation, many=False)
    messages_serializer = ConversationMessageSerializer(conversation.messages.all(), many=True)

    return JsonResponse({
        'conversation': conversation_serializer.data,
        'messages': messages_serializer.data
    }, safe=False)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def conversations_start(request, user_id):
    target_user = get_object_or_404(User, pk=user_id)
    conversation = Conversation.objects.filter(users=request.user).filter(users=target_user).first()
    
    # Check for existing conversation between the two users
    if conversation:
        return JsonResponse({'success': True, 'conversation_id': conversation.id})        
        
    # Create new conversation
    conversation = Conversation.objects.create()
    conversation.users.add(request.user, target_user)

    return JsonResponse({'success': True, 'conversation_id': conversation.id})