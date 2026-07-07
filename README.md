# SUSAMBIL — Ish uchun anketa Telegram boti

"SUSAMBIL" jamoasiga qo'shilish uchun 15 ta savoldan iborat anketani qabul qiladigan
va yakunda javoblarni surat bilan birga belgilangan guruhga yuboradigan Telegram bot.

## Ishlash tartibi

1. Foydalanuvchi `/start` yuboradi — botga xush kelibsiz matni va **"Boshladik"** tugmasi chiqadi.
2. "Boshladik" bosilgach, bot ketma-ket 15 ta savol beradi:
   - Familiya-ism, yosh, manzil, soxa, tajriba, ish vaqti, transport, maosh,
     oilaviy holat, farzandlar soni, dam olish kuni, maktab, hozirgi/oldingi ish joyi, surat.
3. Surat yuborilgach, **"✅ Yuborish"** tugmasi chiqadi.
4. Tugma bosilgach, barcha javoblar surat bilan birga `GROUP_ID` guruhiga yuboriladi.

## O'rnatish (lokal kompyuterda)

```bash
git clone <yangi_repo_manzili>
cd muborakTGbot

python3 -m venv venv
source venv/bin/activate      # Windows: venv\Scripts\activate

pip install -r requirements.txt
```

## Sozlash

`.env.example` faylidan nusxa oling va `.env` deb nomlang:

```bash
cp .env.example .env
```

`.env` faylini oching va o'z ma'lumotlaringizni kiriting:

```
BOT_TOKEN=sizning_bot_tokeningiz
GROUP_ID=-100xxxxxxxxxx
```

> ⚠️ `.env` fayli `.gitignore` orqali repoga tushmaydi — tokeningiz xavfsiz qoladi.
> Botni GitHub'ga yuklashdan oldin tokenni hech qachon to'g'ridan-to'g'ri kodga yozmang.

## Ishga tushirish

```bash
python main.py
```

Terminal osilib qolsa — bu normal holat, bot polling rejimida ishlamoqda.
To'xtatish uchun `Ctrl + C` bosing.

## Serverga (masalan VPS, Railway, Render) joylashda

Deploy platformasining "Environment Variables" bo'limiga quyidagilarni qo'shing:

- `BOT_TOKEN`
- `GROUP_ID`

Kod hech qanday o'zgarishsiz ishlayveradi.

## Talablar

- Python 3.9+
- aiogram 3.15.0
- python-dotenv 1.0.1
