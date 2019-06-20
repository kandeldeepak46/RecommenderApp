from django import template
import json
import operator

register = template.Library()

@register.filter
def lowerCase(value):
    value = value.replace("\'", "\"")
    value = json.loads(value)
    maxValue = max(value.items(), key=operator.itemgetter(1))[0]
    return maxValue



