from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.timezone import now
from django.utils.dateformat import DateFormat
from .models import Message, User, Room
import json

@csrf_exempt
def chat_room(request):  # Handles fetching messages for the main chatroom
    messages = Message.objects.all().order_by("timestamp")
    return render(request, "chat/chat_room.html", {"messages": messages})

@csrf_exempt
def send_message(request):  # AJAX endpoint for sending messages
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            username = data.get("username", "").strip()
            room_name = data.get("room", "").strip()
            content = data.get("content", "").strip()

            if not username or not room_name or not content:
                return JsonResponse({"error": "Invalid data"}, status=400)

            user, _ = User.objects.get_or_create(username=username)
            room, _ = Room.objects.get_or_create(name=room_name)
            message = Message.objects.create(user=user, room=room, content=content, timestamp=now())

            return JsonResponse({
                "message": {
                    "id": message.id,
                    "user": message.user.username,
                    "room": message.room.name,
                    "content": message.content,
                    "timestamp": message.timestamp.strftime("%Y-%m-%d %H:%M:%S"),  # Formatted timestamp
                }
            }, status=201)
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON format."}, status=400)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)

    return JsonResponse({"error": "Invalid request method."}, status=405)


def get_messages(request):  # AJAX endpoint for fetching messages
    messages = Message.objects.order_by("timestamp").values("user__username", "room__name", "content", "timestamp")
    for msg in messages:
        msg['timestamp'] = DateFormat(msg['timestamp']).format("Y-m-d H:i:s")  # Custom format for timestamp
    return JsonResponse(list(messages), safe=False)
