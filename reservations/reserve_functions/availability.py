import datetime
from reservations.models import Reservation
from makeups.models import Makeup

def check_availability(author, start_time, end_time):
    available_list = []
    reservation_list =  Reservation.objects.filter(makeup__author=author)
    for reservation in reservation_list:
        if reservation.start_time > end_time or reservation.end_time < start_time:
            available_list.append(True)
        else:
            available_list.append(False)
    return all(available_list)