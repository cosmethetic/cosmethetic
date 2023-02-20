from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from .forms import AvailabilityForm
from makeups.models import Makeup
from reservations.models import Reservation
from .reserve_functions.cal_reserve_fee import find_total_reserve_fee
from .reserve_functions.availability import check_availability
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView, View

@method_decorator(login_required, name="dispatch")
class MakeupDetailView(View):
    def get(self, request, *args, **kwargs):
        makeup = get_object_or_404(Makeup, pk=self.kwargs['pk'])
        products = makeup.products.all()
        form = AvailabilityForm()

        if makeup.author != self.request.user:
            context = {
                'makeup': makeup,
                'products': products, 
                'form': form,
            }

        else:
            context = {
                'makeup': makeup,
            }
        
        return render(request, 'makeups/makeup_detail.html', context)

    def post(self, request, *args, **kwargs):
        makeup = get_object_or_404(Makeup, pk=self.kwargs['pk'])
        form = AvailabilityForm(request.POST)

        if form.is_valid():
            data = form.cleaned_data
            if check_availability(makeup.author, data['start_time'], data['end_time']):
                total_fee = find_total_reserve_fee(data['start_time'], data['end_time'], self.kwargs['pk'])
                reservation = Reservation.objects.create(
                    user = request.user,
                    makeup = makeup,
                    status='r',
                    start_time=data['start_time'],
                    end_time=data['end_time'],
                    total_fee = total_fee,
                )
                reservation.save()
                # return redirect('reserevations:reservation_detail', pk=reservation.pk)
                return redirect('/')
            else:
                return HttpResponse(
                    "<script>alert('해당 아티스트는 이미 예약되었습니다! 다른 아티스트로 시도해주세요. :)');location.href='/makeups/';</script>")

        return HttpResponse(
            "<script>alert('유효하지 않은 전송입니다. :(');location.href='/';</script>")
