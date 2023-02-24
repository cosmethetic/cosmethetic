import datetime
from makeups.models import Makeup

def find_total_reserve_fee(start_time, end_time, pk):
    days = start_time - end_time
    seconds = days.seconds
    hours = seconds//3600

    makeup = Makeup.objects.get(pk=pk)
    total = abs(hours * makeup.price)
    return total