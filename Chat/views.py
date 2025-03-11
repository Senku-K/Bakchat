# Create your views here.
from django.shortcuts import render, redirect
from .models import User, Message
from .forms import MessageForm

def chat_room(request):
    username = request.session.get('username')

    if not username:
        username = f"Bakchod{User.objects.count() + 1}"
        User.objects.create(username=username)
        request.session['username'] = username

    messages = Message.objects.filter(room="Bakchodikachoda").order_by('timestamp')

    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            Message.objects.create(
                user=User.objects.get(username=username),
                content=form.cleaned_data['content']
            )
            return redirect('chat_room')
    else:
        form = MessageForm()

    return render(request, 'chat/chat_room.html', {'messages': messages, 'form': form, 'username': username})

