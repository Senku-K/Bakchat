# Create your views here.
from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.views.decorators.http import require_GET
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate
from django.contrib import messages
from .models import Message, UserProfile
from .forms import MessageForm, SignUpForm, UserProfileForm
from datetime import datetime

def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            display_name = form.cleaned_data.get('display_name')
            if display_name:
                user.profile.display_name = display_name
                user.profile.save()
            login(request, user)
            return redirect('chat_room')
    else:
        form = SignUpForm()
    return render(request, 'chat/signup.html', {'form': form})

@login_required
def profile(request):
    if request.method == 'POST':
        form = UserProfileForm(request.POST, instance=request.user.profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your profile was successfully updated!')
            return redirect('chat_room')
    else:
        form = UserProfileForm(instance=request.user.profile)
    return render(request, 'chat/profile.html', {'form': form})

@login_required
def chat_room(request):
    messages_list = Message.objects.filter(room="Bakchodikachoda").select_related('user', 'user__profile', 'replied_to', 'replied_to__user', 'replied_to__user__profile').order_by('timestamp')

    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            message = form.save(commit=False)
            message.user = request.user
            
            # Handle reply
            reply_to_id = request.POST.get('reply_to')
            if reply_to_id:
                try:
                    replied_to_message = Message.objects.get(id=reply_to_id)
                    message.replied_to = replied_to_message
                except Message.DoesNotExist:
                    pass
                
            message.save()
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({'status': 'success'})
            return redirect('chat_room')
    else:
        form = MessageForm()

    return render(request, 'chat/chat_room.html', {
        'messages': messages_list,
        'form': form,
        'user': request.user
    })

@login_required
@require_GET
def get_messages(request):
    last_timestamp = request.GET.get('last_timestamp')
    if last_timestamp:
        try:
            last_timestamp = datetime.fromisoformat(last_timestamp)
            messages = Message.objects.filter(
                room="Bakchodikachoda",
                timestamp__gt=last_timestamp
            ).select_related('user', 'user__profile', 'replied_to', 'replied_to__user', 'replied_to__user__profile').order_by('timestamp')
        except ValueError:
            messages = Message.objects.filter(room="Bakchodikachoda").select_related('user', 'user__profile', 'replied_to', 'replied_to__user', 'replied_to__user__profile').order_by('timestamp')
    else:
        messages = Message.objects.filter(room="Bakchodikachoda").select_related('user', 'user__profile', 'replied_to', 'replied_to__user', 'replied_to__user__profile').order_by('timestamp')

    messages_data = [{
        'id': msg.id,
        'username': msg.user.profile.display_name or msg.user.username,
        'content': msg.content,
        'timestamp': msg.timestamp.isoformat(),
        'is_self': msg.user == request.user,
        'replied_to': {
            'id': msg.replied_to.id,
            'username': msg.replied_to.user.profile.display_name or msg.replied_to.user.username,
            'content': msg.replied_to.content
        } if msg.replied_to else None
    } for msg in messages]

    return JsonResponse({'messages': messages_data})

