from datetime import datetime
from zoneinfo import ZoneInfo
from django.http import HttpResponse
from django.shortcuts import render
from django.templatetags.static import static
from django.urls import reverse
from django.utils import timezone
from django.views.decorators.http import require_GET
from django.views.decorators.cache import never_cache

EVENT_DATE = datetime(2026, 10, 31, 17, 0, tzinfo=ZoneInfo("Asia/Tashkent"))
MAP_URL = "https://maps.app.goo.gl/iJbevmkV5SUXWaeW6"


def page_context():
    return {
        "event_iso": EVENT_DATE.isoformat(),
        "map_url": MAP_URL,
        "calendar_days": range(1, 32),
        "calendar_blanks": range(3),
    }


@require_GET
@never_cache
def home(request):
    context = page_context()
    context.update({
        "share_url": request.build_absolute_uri(reverse("home")),
        "share_image_url": request.build_absolute_uri(static("invitation/images/invitation-preview-anvar.jpg")),
    })
    return render(request, "invitation/home.html", context)


@require_GET
def calendar_event(request):
    # RFC 5545: fold UTF-8 lines at 75 octets, never splitting a code point.
    lines = [
        "BEGIN:VCALENDAR", "VERSION:2.0", "PRODID:-//Anvarjon Jasminaxon//Wedding//UZ",
        "CALSCALE:GREGORIAN", "METHOD:PUBLISH", "BEGIN:VEVENT",
        "UID:anvarjon-jasminaxon-20261031@wedding-day-31-10.uz",
        "DTSTAMP:" + timezone.now().strftime("%Y%m%dT%H%M%SZ"),
        "DTSTART:20261031T120000Z",
        "SUMMARY:Anvarjon va Jasminaxon — nikoh to‘yi",
        "LOCATION:Ratana Restaurant to‘yxonasi\\, Pastdarg‘om tumani\\, Samarqand viloyati",
        "DESCRIPTION:Sizni nikoh to‘yimizga lutfan taklif etamiz.\\nManzil: " + MAP_URL,
        "URL:" + MAP_URL,
        "BEGIN:VALARM", "TRIGGER:-P1D", "ACTION:DISPLAY",
        "DESCRIPTION:Ertaga Anvarjon va Jasminaxonning nikoh to‘yi", "END:VALARM",
        "END:VEVENT", "END:VCALENDAR",
    ]
    folded = []
    for line in lines:
        part = ""
        for char in line:
            if len((part + char).encode("utf-8")) > 75:
                folded.append(part)
                part = " "
            part += char
        folded.append(part)
    result = HttpResponse("\r\n".join(folded) + "\r\n", content_type="text/calendar; charset=utf-8")
    result["Content-Disposition"] = 'attachment; filename="Anvarjon-Gozal.ics"'
    return result
