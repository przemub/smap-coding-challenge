# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseBadRequest, JsonResponse
from django.db import models

from consumption.models import MeterUser, ConsumptionEntry

from statistics import mean


def summary(request):
    context = {
        'users': MeterUser.objects.all(),
        'message': 'Hello!',
    }
    return render(request, 'consumption/summary.html', context)


def detail(request):
    requested_id = request.GET.get("id", "")
    if requested_id == "sum":
        query = ConsumptionEntry.objects.values('datetime').annotate(consumption=models.Sum('consumption')) \
                .order_by('datetime')
        response = {
            'max': max((date['consumption'] for date in query)),
            'avg': mean((date['consumption'] for date in query)),
            'entries': [date for date in query]
        }
    elif requested_id == "avg":
        query = ConsumptionEntry.objects.values('datetime').annotate(consumption=models.Avg('consumption')) \
                .order_by('datetime')
        response = {
            'max': max((date['consumption'] for date in query)),
            'avg': mean((date['consumption'] for date in query)),
            'entries': [date for date in query]
        }
    else:
        try:
            obj_id = request.GET.get("id", "")
        except ValueError:
            raise HttpResponseBadRequest
        obj = get_object_or_404(MeterUser, id=obj_id)

        response = {
            'max': obj.cache_max,
            'avg': obj.cache_avg,
            'entries': [{'datetime': entry.datetime,
                         'consumption': entry.consumption}
                        for entry in obj.consumptionentry_set.all()]
        }
    return JsonResponse(response)
