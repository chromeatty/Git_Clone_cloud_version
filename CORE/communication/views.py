from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render

from accounts.models import User
from .forms import MessageForm
from .models import Message

@login_required
def send_message(request, recipient_id=None):
    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            msg = form.save(commit=False)
            msg.sender = request.user
            msg.save()
            return redirect('inbox')
    else:
        initial = {}
        if recipient_id:
            initial['recipient'] = User.objects.get(pk=recipient_id)
        form = MessageForm(initial=initial)
    return render(request, 'send_message.html', {'form': form})

@login_required
def inbox(request):
    messages = Message.objects.filter(recipient=request.user).order_by('-timestamp')
    return render(request, 'inbox.html', {'messages': messages})

@login_required
def send_message_to(request, recipient_id):
    return send_message(request, recipient_id)

