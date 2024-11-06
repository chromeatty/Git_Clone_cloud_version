from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, render, redirect
from .forms import RequestForm
from .models import Request
from django.contrib import messages

@login_required
def create_request(request):
    if request.method == 'POST':
        form = RequestForm(request.POST)
        if form.is_valid():
            # Create a new offer instance but do not save to DB yet
            new_offer = form.save(commit=False)
            # Set the user field, which is not part of the form itself
            new_offer.user = request.user
            # Now save the object to DB
            new_offer.save()
            # Redirect to a page to view the offer list or confirmation
            return redirect('user_request_list')
    else:
        form = RequestForm()  # An empty form for GET request

    return render(request, 'create_request.html', {'form': form})

@login_required
def user_request_list(request):
    req = Request.objects.filter(user=request.user)
    return render(request, 'user_request_list.html', {'requests_app': req})



@login_required
def edit_request(request, pk):
    req = get_object_or_404(Request, pk=pk, user=request.user)
    if request.method == 'POST':
        form = RequestForm(request.POST, instance=req)
        if form.is_valid():
            form.save()
            return redirect('user_request_list')
    else:
        form = RequestForm(instance=req)
    return render(request, 'edit_request.html', {'form': form})


"""
@login_required
def delete_request(request, pk):
    req = get_object_or_404(Request, pk=pk, user=request.user)  # Ensures only the owner can delete
    if request.method == 'POST':
        req.delete()
        messages.success(request, "The request has been deleted successfully.")
        return redirect('user_request_list')
    else:
        messages.error(request, "Invalid method.")
        return redirect('user_request_list')
"""
from django.http import JsonResponse



@login_required
def delete_request(request, pk):
    if request.method == 'POST' and request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        req = get_object_or_404(Request, pk=pk, user=request.user)
        req.delete()
        return JsonResponse({"status": "success", "message": "Request deleted successfully."})
    return JsonResponse({"status": "error", "message": "Invalid request."}, status=400)


# This is to allow requesers to view offers and like/ save what they have seen


from offers.models import Offer


@login_required
def requester_view_offers(request):
    offers = Offer.objects.all()
    if request.method == 'POST':
        offer_id = request.POST.get('offer_id')
        offer = Offer.objects.get(id=offer_id)
        if offer.likes.filter(id=request.user.id).exists():
            offer.likes.remove(request.user)
        else:
            offer.likes.add(request.user)
        return redirect('requester_view_offers')

    return render(request, 'requester_view_offers.html', {'offers': offers})

@login_required
def requester_view_offers_detail(request, pk):
    offer = get_object_or_404(Offer, pk=pk)
    return render(request, 'requester_view_offers_detail.html', {'offer': offer})

@login_required
def requester_liked_offers(request):
    offers = Offer.objects.filter(likes=request.user)# only show offers that the user has liked
    if request.method == 'POST':
        offer_id = request.POST.get('offer_id')
        offer = Offer.objects.get(id=offer_id)
        if offer.likes.filter(id=request.user.id).exists():
            offer.likes.remove(request.user)
            offers = Offer.objects.filter(likes=request.user)
        #else:
            #offer.likes.add(request.user) # This is not needed here as you cant add a like from this page
            return redirect('requester_liked_offers')
    return render(request, 'requester_liked_offers.html', {'offers': offers})

