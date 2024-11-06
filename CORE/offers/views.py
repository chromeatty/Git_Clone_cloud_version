from django.http import HttpResponseForbidden
from django.shortcuts import get_object_or_404, render, redirect
from .forms import OfferForm
from .models import Offer
from django.contrib.auth.decorators import login_required
# get all the requests from requests_app.models
from requests_app.models import Request
from django.contrib import messages # to display messages to the user


@login_required
def create_offer(request):
    if request.method == 'POST':
        form = OfferForm(request.POST)
        if form.is_valid():
            # Create a new offer instance but do not save to DB yet
            new_offer = form.save(commit=False)
            # Set the user field, which is not part of the form itself
            new_offer.user = request.user
            # Now save the object to DB
            new_offer.save()
            # Redirect to a page to view the offer list or confirmation
            return redirect('user_offer_list')
    else:
        form = OfferForm()  # An empty form for GET request

    return render(request, 'create_offer.html', {'form': form})


@login_required
# to display the list of offers provided by the user only!!
def user_offer_list(request):
    offers = Offer.objects.filter(user=request.user)
    return render(request, 'user_offer_list.html', {'offers': offers})

@login_required
def edit_offer(request, pk):
    offer = get_object_or_404(Offer, pk=pk, user=request.user)
    if request.method == 'POST':
        form = OfferForm(request.POST, instance=offer)
        if form.is_valid():
            form.save()
            return redirect('user_offer_list')
    else:
        form = OfferForm(instance=offer)
    return render(request, 'edit_offer.html', {'form': form})


@login_required
def delete_offer(request, pk):
    offer = get_object_or_404(Offer, pk=pk, user=request.user)  # Ensures only the owner can delete
    if request.method == 'POST':
        offer.delete()
        messages.success(request, "The offer has been deleted successfully.")
        return redirect('user_offer_list')
    else:
        messages.error(request, "Invalid method.")
        return redirect('user_offer_list')


@login_required
def view_requests_and_accept(request):
    requests = Request.objects.all()
    return render(request, 'view_requests_and_accept.html', {'requests': requests})


from requests_app.models import Request

from django.http import JsonResponse


@login_required
def offer_view_requests(request, page_type='all'):

    # Determine which requests to display based on the page_type
    if page_type == 'accepted':
        requests = Request.objects.filter(accepted_by=request.user)
        template = 'view_accepted_requests.html'
    else:
        requests = Request.objects.all()
        template = 'view_requests_and_accept.html'

    if request.method == 'POST':
        request_id = request.POST.get('request_id')
        action = request.POST.get('action')
        req = get_object_or_404(Request, id=request_id)

        if action == 'accept':
            if page_type == 'all':  # only accepting if viewing all the requests
                req.accepted_by = request.user
                req.status = 'accepted'  
                req.save()
                return JsonResponse({'status': 'accepted', 'message': 'Request accepted successfully'})
        elif action == 'retract':
            if req.accepted_by == request.user:  
                req.accepted_by = None #reset it back to the defalts
                req.status = 'pending'  
                req.save()
                return JsonResponse({'status': 'pending', 'message': 'Acceptance retracted successfully'})

    
    return render(request, template, {'requests': requests, 'page_type': page_type})
