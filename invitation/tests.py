from datetime import datetime
from zoneinfo import ZoneInfo
from django.test import TestCase
from django.urls import reverse
from .models import GuestResponse
from .views import EVENT_DATE


class InvitationTests(TestCase):
    def test_prayer_text_uses_reviewed_transliteration(self):
        response = self.client.get(reverse("home"))
        self.assertContains(response, "Allohumma solli ’ala Muhammadiv-va ’ala ali Muhammad.")
        self.assertContains(response, "اللَّهُمَّ صَلِّ عَلَى مُحَمَّدٍ وَعَلَى آلِ مُحَمَّدٍ")
        self.assertContains(response, "ustingizga baraka yog‘dirsin")
        self.assertContains(response, "Nikoh tabrigi duosi mazmunidan")
        self.assertNotContains(response, "va ‘ala oli Muhammad")

    def test_share_preview_is_absolute_and_server_rendered(self):
        response = self.client.get(reverse("home"), secure=True)
        self.assertContains(response, 'property="og:image" content="https://testserver/static/invitation/images/invitation-preview-blue.jpg"')
        self.assertContains(response, 'property="og:url" content="https://testserver/"')
        self.assertContains(response, 'property="og:image:width" content="1200"')
        self.assertContains(response, 'property="og:image:height" content="630"')
        self.assertContains(response, 'name="twitter:card" content="summary_large_image"')

    def test_music_uses_local_trimmed_einaudi_file(self):
        response = self.client.get(reverse("home"))
        self.assertContains(response, '/static/invitation/audio/einaudi-trimmed.m4a')
        self.assertContains(response, 'type="audio/mp4"')
        self.assertNotContains(response, 'una-mattina.mp3')
        self.assertContains(response, 'id="background-audio" loop')
        self.assertNotContains(response, 'sokin-ohang.mp3')
        self.assertNotContains(response, 'youtube')

    def test_invitation_contains_correct_event_and_venue(self):
        response = self.client.get(reverse("home"))
        self.assertContains(response, "Asliddin")
        self.assertContains(response, "Go‘zal")
        self.assertContains(response, '2026-10-26T18:00:00+05:00')
        self.assertContains(response, "Labi hovuz")
        self.assertContains(response, "Karmana tumani, Navoiy viloyati")
        self.assertContains(response, "Dushanba · soat 18:00")
        self.assertContains(response, 'class="wedding-day" aria-label="26-oktyabr, tantanali marosim (To‘qqiz to‘y)">26')
        self.assertNotContains(response, "ODILBEK")
        self.assertNotContains(response, "31-oktyabr")
        self.assertContains(response, "https://www.google.com/maps/search/?api=1&amp;query=Labi+hovuz+to%27yxonasi%2C+Karmana%2C+Navoiy")
        self.assertEqual(EVENT_DATE.astimezone(ZoneInfo("UTC")).hour, 13)

    def test_response_is_persisted_and_private(self):
        guest = GuestResponse.objects.create(name="Avvalgi mehmon", attendance="yes", guests=2, message="Baxtli bo‘ling!")
        self.assertNotContains(self.client.get(reverse("home")), guest.message)
        self.assertRedirects(self.client.get("/admin/invitation/guestresponse/"), "/admin/login/?next=/admin/invitation/guestresponse/", fetch_redirect_response=False)

    def test_calendar_has_correct_utc_and_utf8_folding(self):
        response = self.client.get(reverse("calendar"))
        self.assertEqual(response.status_code, 200)
        payload = response.content.decode("utf-8")
        self.assertIn("DTSTART:20261026T130000Z\r\n", payload)
        self.assertIn("BEGIN:VCALENDAR\r\n", payload)
        self.assertIn('attachment;', response["Content-Disposition"])
        for line in payload.split("\r\n"):
            self.assertLessEqual(len(line.encode("utf-8")), 75)
        self.assertEqual(datetime(2026, 10, 26).weekday(), 0)

    def test_rsvp_rejects_get(self):
        self.assertEqual(self.client.get("/rsvp/").status_code, 404)
