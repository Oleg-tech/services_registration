import datetime

from clients.models import Procedure


def main():
    for p in Procedure.objects.all():
        if p.day != datetime.datetime.now().strftime("%d"):
            Procedure.objects.filter(id=p.id).delete()

