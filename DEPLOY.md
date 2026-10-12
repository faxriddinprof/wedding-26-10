# wedding-day-31-10.uz — alohida Eskiz hosting

Bu taklifnoma `wedding-26-10` repositorysining `anvar` branchida.
Yangi hostingga aynan shu branchni klonlang:

```bash
mkdir -p /home/host9550/apps
cd /home/host9550/apps
git clone --branch anvar --single-branch https://github.com/faxriddinprof/wedding-26-10.git wedding
```

Keyingi yangilashlar ham `anvar` branchidan olinadi. Alohida yangi baza va
SECRET_KEY ishlating.

Avval yangi hosting terminalida `whoami` va `pwd` bilan hisobni tekshiring.
Buyurtma skrinshotida yangi hisob `host9550`; `host9489` eski saytga tegishli.

cPanel → Setup Python App → Create Application:

- Python: 3.12
- Application root: `apps/wedding`
- Application URL: `wedding-day-31-10.uz`, yo‘l bo‘sh
- Startup file: `passenger_wsgi.py`
- Entry point: `application`

Repo fayllarini shu hisobning `apps/wedding` papkasiga joylang. cPanel ko‘rsatgan
virtual muhitni faollashtirish buyrug‘idan foydalaning.

Environment variables:

```text
DJANGO_DEBUG=0
DJANGO_ALLOWED_HOSTS=wedding-day-31-10.uz,www.wedding-day-31-10.uz
DJANGO_CSRF_TRUSTED_ORIGINS=https://wedding-day-31-10.uz,https://www.wedding-day-31-10.uz
DJANGO_SECURE_SSL_REDIRECT=1
```

`DJANGO_SECRET_KEY` uchun yangi tasodifiy qiymat yarating; eski sayt kalitini
ishlatmang. Terminaldagi management buyruqlari uchun ham shu o‘zgaruvchilar
eksport qilinishi kerak. `.env` avtomatik o‘qilmaydi.

`whoami` **host9550** ekanini tasdiqlagach:

```bash
source /home/host9550/virtualenv/apps/wedding/3.12/bin/activate
cd /home/host9550/apps/wedding
python -m pip install -r requirements.txt
python manage.py check
python manage.py migrate
python manage.py collectstatic --noinput
mkdir -p /home/host9550/public_html/static
cp -R /home/host9550/apps/wedding/staticfiles/. /home/host9550/public_html/static/
mkdir -p /home/host9550/apps/wedding/tmp
touch /home/host9550/apps/wedding/tmp/restart.txt
```

Domain document root `public_html` ekanini cPanel → Domains orqali tekshiring;
boshqa papka bo‘lsa, statik fayllarni shu papkaning `static/` katalogiga nusxalang.
HTTPS sertifikati va DNS shu yangi hostingga mos bo‘lishi kerak.

Sana: 31-oktyabr 2026, shanba, 17:00 (Asia/Tashkent).
Manzil: Ratana Restaurant to‘yxonasi, Pastdarg‘om tumani, Samarqand viloyati.
Aniq Google Maps havolasi: https://maps.app.goo.gl/iJbevmkV5SUXWaeW6
Musiqa: `static/invitation/audio/kokun-trimmed.mp3` — original `Kokun.mp3`
faylining dastlabki 17 soniyasi kesilgan; original saqlangan.

Telegram preview: `/static/invitation/images/invitation-preview-anvar.jpg`.
