from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Message
from .forms import MessageForm
from django.contrib.auth.models import User

@login_required
def inbox(request):
    messages_received = Message.objects.filter(receiver=request.user).order_by('-sent_at')
    unread_count = messages_received.filter(is_read=False).count()
    
    # Mark messages as read when viewing inbox
    for message in messages_received.filter(is_read=False):
        message.is_read = True
        message.save()
    
    return render(request, 'inbox.html', {
        'messages': messages_received,
        'unread_count': unread_count
    })

@login_required
def send_message(request):
    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            message = form.save(commit=False)
            message.sender = request.user
            message.save()
            messages.success(request, 'Message sent successfully!')
            return redirect('inbox')
        else:
            messages.error(request, 'Please fix the errors below.')
    else:
        form = MessageForm()
    
    # Get list of users for the receiver field
    users = User.objects.exclude(id=request.user.id)
    
    return render(request, 'send_message.html', {
        'form': form,
        'users': users
    })
