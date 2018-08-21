# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseBadRequest, JsonResponse
from django.db import models
from django.db.models.functions import TruncDay
from django.core.serializers.json import DjangoJSONEncoder
from django.views.decorators.cache import cache_page

from consumption.models import MeterUser, ConsumptionEntry

from statistics import mean
import decimal


def summary(request):
    context = {
        'users': MeterUser.objects.all(),
        'message': 'Hello!',
    }
    return render(request, 'consumption/summary.html', context)


@cache_page(60*60*24*365*100)
def detail(request):
    requested_id = request.GET.get("id", "")
    if requested_id == "Sum":
        query = ConsumptionEntry.objects.annotate(day=TruncDay('datetime')).values('day').annotate(consumption=models.Sum('consumption')) \
                .order_by('day')
        response = {
            'max': max((date['consumption'] for date in query)),
            'avg': mean((date['consumption'] for date in query)),
            'labels': [date['day'] for date in query],
            'data': [date['consumption'] for date in query]
        }
    elif requested_id == "Average":
        query = ConsumptionEntry.objects.annotate(day=TruncDay('datetime')).values('day').annotate(consumption=models.Avg('consumption')) \
                .order_by('day')
        response = {
            'max': max((date['consumption'] for date in query)),
            'avg': mean((date['consumption'] for date in query)),
            'labels': [date['day'] for date in query],
            'data': [date['consumption'] for date in query]
        }
    else:
        try:
            obj_id = request.GET.get("id", "")
        except ValueError:
            raise HttpResponseBadRequest
        obj = get_object_or_404(MeterUser, id=obj_id)

        query = obj.consumptionentry_set.annotate(day=TruncDay('datetime')).values('day').annotate(consumption=models.Avg('consumption')) \
            .order_by('day')

        response = {
            'max': max((date['consumption'] for date in query)),
            'avg': mean((date['consumption'] for date in query)),
            'labels': [date['day'] for date in query],
            'data': [date['consumption'] for date in query]
        }

    # Output decimals to JSON as numbers, not strings
    class DecimalEncoder(DjangoJSONEncoder):
        def default(self, o):
            if isinstance(o, decimal.Decimal):
                return float(o)
            return super(DecimalEncoder, self).default(o)

    print(response)
    return JsonResponse(response, DecimalEncoder)
