# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from meetingservices.utils import build_worklist_csv

from meetingservices.models import EventDetails
import django

django.setup()

event_details = EventDetails.objects.all()

if __name__ == '__main__':
    import cProfile
    cProfile.run(
        'build_worklist_csv(event_details)', filename='csv.profile')
