# MuborakTGbot — SUSAMBIL anketa boti

## O'rnatish

1. Kerakli kutubxonalarni o'rnating:
   ```
   pip install -r requirements.txt
   ```

2. `main.py` faylini oching va yuqori qismidagi quyidagi qatorlarni o'zingizning ma'lumotlaringiz bilan to'ldiring:
   ```python
   BOT_TOKEN = "sizning-bot-tokeningiz"
   GROUP_ID = -100xxxxxxxxxx
   ```

   **GROUP_ID'ni qanday topish mumkin:**
   - Botni guruhga qo'shing (u yerda a'zo bo'lishi shart).
   - Guruhda istalgan xabar yozing.
   - Botni ishga tushiring (`py main.py`) — terminalda quyidagicha qator chiqadi:
     ```
     [INFO] Guruhdan xabar keldi -> chat_id=-1001234567890, turi=supergroup, nomi=...
     ```
   - Shu `chat_id` qiymatini `main.py` ichidagi `GROUP_ID`ga yozing.

3. Botni ishga tushiring:
   ```
   py main.py
   ```

## Muhim eslatmalar

- ⚠️ Bot tokeni endi kodning ichida ochiq turibdi. Agar bu loyihani **ochiq (public) GitHub repository**ga yuklasangiz, tokeningizni istalgan kishi ko'rib, botingizni o'zlashtirib olishi mumkin. Repository'ni **private** qiling yoki tokenni @BotFather orqali muntazam yangilab turing (`/revoke`).
- Botni ishga tushirganda u avtomatik ravishda `GROUP_ID` to'g'riligini tekshiradi va natijasini terminalga chiqaradi — agar xatolik bo'lsa, sababi aniq yoziladi.
- Bir vaqtning o'zida botni faqat **bitta joyda** (yoki faqat lokal, yoki faqat serverda) ishga tushiring — aks holda `TelegramConflictError` xatoligi chiqadi.