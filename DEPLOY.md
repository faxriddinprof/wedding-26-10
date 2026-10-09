# wedding-26-10.uz — alohida Eskiz hosting

Yangi loyiha uchun alohida GitHub repository ishlating. Eski loyiha bazasi,
`.env`, virtual muhit va Git tarixi ko‘chirilmagan.

Avval yangi hosting terminalida `whoami` va `pwd` bilan hisobni tekshiring.
Buyurtma skrinshotida yangi hisob `host9534`; `host9489` eski saytga tegishli.

cPanel → Setup Python App → Create Application:

- Python: 3.12
- Application root: `apps/wedding`
- Application URL: `wedding-26-10.uz`, yo‘l bo‘sh
- Startup file: `passenger_wsgi.py`
- Entry point: `application`

Repo fayllarini shu hisobning `apps/wedding` papkasiga joylang. cPanel ko‘rsatgan
virtual muhitni faollashtirish buyrug‘idan foydalaning.

Environment variables:

```text
DJANGO_DEBUG=0
DJANGO_ALLOWED_HOSTS=wedding-26-10.uz,www.wedding-26-10.uz
DJANGO_CSRF_TRUSTED_ORIGINS=https://wedding-26-10.uz,https://www.wedding-26-10.uz
DJANGO_SECURE_SSL_REDIRECT=1
```

`DJANGO_SECRET_KEY` uchun yangi tasodifiy qiymat yarating; eski sayt kalitini
ishlatmang. Terminaldagi management buyruqlari uchun ham shu o‘zgaruvchilar
eksport qilinishi kerak. `.env` avtomatik o‘qilmaydi.

`whoami` **host9534** ekanini tasdiqlagach:

```bash
source /home/host9534/virtualenv/apps/wedding/3.12/bin/activate
cd /home/host9534/apps/wedding
python -m pip install -r requirements.txt
python manage.py check
python manage.py migrate
python manage.py collectstatic --noinput
mkdir -p /home/host9534/public_html/static
cp -R /home/host9534/apps/wedding/staticfiles/. /home/host9534/public_html/static/
mkdir -p /home/host9534/apps/wedding/tmp
touch /home/host9534/apps/wedding/tmp/restart.txt
```

Domain document root `public_html` ekanini cPanel → Domains orqali tekshiring;
boshqa papka bo‘lsa, statik fayllarni shu papkaning `static/` katalogiga nusxalang.
HTTPS sertifikati va DNS shu yangi hostingga mos bo‘lishi kerak.

Sana: 26-oktyabr 2026, dushanba, 18:00 (Asia/Tashkent).
Manzil: Labi hovuz to‘yxonasi, Karmana tumani, Navoiy viloyati.
Xarita hozircha manzil bo‘yicha qidiruv: aniq Google Maps pin havolasi berilganda
`invitation/views.py` ichidagi `MAP_URL` yangilanadi.

Telegram preview: `/static/invitation/images/invitation-preview-blue.jpg`.
