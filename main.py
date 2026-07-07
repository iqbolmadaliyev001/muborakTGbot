import asyncio
import os
from dotenv import load_dotenv
from aiogram import Bot, Dispatcher, F, types
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
GROUP_ID = os.getenv("GROUP_ID")

if not BOT_TOKEN:
    raise RuntimeError(
        "BOT_TOKEN muhit o'zgaruvchisi topilmadi. "
        "Uni deploy platformasi sozlamalarida yoki .env faylida o'rnating."
    )

if not GROUP_ID:
    raise RuntimeError(
        "GROUP_ID muhit o'zgaruvchisi topilmadi. "
        "Uni deploy platformasi sozlamalarida yoki .env faylida o'rnating."
    )

GROUP_ID = int(GROUP_ID)


bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(storage=MemoryStorage())


WELCOME_TEXT = (
    "Assalom alekum! Siz bilan \"SUSAMBIL\" jamoasiga qo'shilish uchun anketa to'ldiramiz.\n\n"
    "Siz \"Boshladik\" tugmasini bosish orqali o'zingiz haqingizdagi ma'lumotlarni biz bilan "
    "o'rtoqlashishga rozilik bildirgan bo'lasiz, e'tibor uchun tashakkur..!"
)


class Form(StatesGroup):
    ism = State()
    telefon = State()
    yosh = State()
    manzil = State()
    soxa = State()
    tajriba = State()
    ish_vaqti = State()
    transport = State()
    maosh = State()
    oilaviy = State()
    farzand = State()
    dam_olish = State()
    maktab = State()
    hozirgi_ish = State()
    oldingi_ish = State()
    rasm = State()
    tayyor = State()


def ha_yoq_markup():
    return ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text="Ha"), KeyboardButton(text="Yo'q")]],
        resize_keyboard=True,
        one_time_keyboard=True
    )


def oilaviy_markup():
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="Ha"), KeyboardButton(text="Yo'q")],
            [KeyboardButton(text="Ajrashganman")]
        ],
        resize_keyboard=True,
        one_time_keyboard=True
    )


def telefon_markup():
    return ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text="📞 Raqamni yuborish", request_contact=True)]],
        resize_keyboard=True,
        one_time_keyboard=True
    )


def boshladik_markup():
    return ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text="Boshladik")]],
        resize_keyboard=True,
        one_time_keyboard=True
    )


@dp.message(CommandStart())
async def start(message: types.Message, state: FSMContext):
    await state.clear()
    await message.answer(WELCOME_TEXT, reply_markup=boshladik_markup())


@dp.message(F.text == "Boshladik")
async def boshladik(message: types.Message, state: FSMContext):
    await state.clear()
    await state.set_state(Form.ism)
    await message.answer(
        "1) Familiya va ismingiz..?",
        reply_markup=ReplyKeyboardRemove()
    )


@dp.message(Form.ism)
async def get_ism(message: types.Message, state: FSMContext):
    await state.update_data(ism=message.text)
    await state.set_state(Form.telefon)
    await message.answer(
        "2) Telefon raqamingiz..? (pastdagi tugma orqali yuborishingiz ham mumkin)",
        reply_markup=telefon_markup()
    )


@dp.message(Form.telefon, F.contact)
async def get_telefon_contact(message: types.Message, state: FSMContext):
    await state.update_data(telefon=message.contact.phone_number)
    await state.set_state(Form.yosh)
    await message.answer("3) Yoshingiz..?", reply_markup=ReplyKeyboardRemove())


@dp.message(Form.telefon)
async def get_telefon_text(message: types.Message, state: FSMContext):
    await state.update_data(telefon=message.text)
    await state.set_state(Form.yosh)
    await message.answer("3) Yoshingiz..?", reply_markup=ReplyKeyboardRemove())


@dp.message(Form.yosh)
async def get_yosh(message: types.Message, state: FSMContext):
    if not message.text.isdigit():
        await message.answer("Iltimos, yoshni faqat raqamda kiriting (masalan: 25):")
        return

    await state.update_data(yosh=message.text)
    await state.set_state(Form.manzil)
    await message.answer("4) Yashash manzilingiz..? (Shaxar-tuman, mahalla, ko'cha, uy manzili)")


@dp.message(Form.manzil)
async def get_manzil(message: types.Message, state: FSMContext):
    await state.update_data(manzil=message.text)
    await state.set_state(Form.soxa)
    await message.answer("5) Susambil choyxonasida sizni qaysi soxadagi ish qiziqtirdi..?")


@dp.message(Form.soxa)
async def get_soxa(message: types.Message, state: FSMContext):
    await state.update_data(soxa=message.text)
    await state.set_state(Form.tajriba)
    await message.answer("6) Bu soxadagi tajribangiz qancha..?(yil yoki oy)")


@dp.message(Form.tajriba)
async def get_tajriba(message: types.Message, state: FSMContext):
    await state.update_data(tajriba=message.text)
    await state.set_state(Form.ish_vaqti)
    await message.answer(
        "7) Soxangizdagi ish vaqti 1 kunda 12 soatni tashkil etishi mumkin. Rozimisiz..?",
        reply_markup=ha_yoq_markup()
    )


@dp.message(Form.ish_vaqti)
async def get_ish_vaqti(message: types.Message, state: FSMContext):
    await state.update_data(ish_vaqti=message.text)
    await state.set_state(Form.transport)
    await message.answer(
        "8) Ishga kelib-ketish uchun transport muammosi bormi..?",
        reply_markup=ha_yoq_markup()
    )


@dp.message(Form.transport)
async def get_transport(message: types.Message, state: FSMContext):
    await state.update_data(transport=message.text)
    await state.set_state(Form.maosh)
    await message.answer(
        "9) Sizni bir oyda qancha maosh qiziqtiradi..?",
        reply_markup=ReplyKeyboardRemove()
    )


@dp.message(Form.maosh)
async def get_maosh(message: types.Message, state: FSMContext):
    await state.update_data(maosh=message.text)
    await state.set_state(Form.oilaviy)
    await message.answer(
        "10) Oilalikmisiz..?(Ha, Yo'q, Ajrashganman)",
        reply_markup=oilaviy_markup()
    )


@dp.message(Form.oilaviy)
async def get_oilaviy(message: types.Message, state: FSMContext):
    await state.update_data(oilaviy=message.text)
    await state.set_state(Form.farzand)
    await message.answer(
        "11) Farzandlaringiz nechta..?",
        reply_markup=ReplyKeyboardRemove()
    )


@dp.message(Form.farzand)
async def get_farzand(message: types.Message, state: FSMContext):
    await state.update_data(farzand=message.text)
    await state.set_state(Form.dam_olish)
    await message.answer(
        "12) Ishxona qoidalaridan kelib chiqqan holda sizda 1 oy davomida \"Dam olish kuni\" "
        "bo'lmasligi mumkin, albatta sizga mexnatingizga yarasha maosh beriladi, rozimisiz..?",
        reply_markup=ha_yoq_markup()
    )


@dp.message(Form.dam_olish)
async def get_dam_olish(message: types.Message, state: FSMContext):
    await state.update_data(dam_olish=message.text)
    await state.set_state(Form.maktab)
    await message.answer(
        "13) Qaysi maktabda taxsil olgansiz..?",
        reply_markup=ReplyKeyboardRemove()
    )


@dp.message(Form.maktab)
async def get_maktab(message: types.Message, state: FSMContext):
    await state.update_data(maktab=message.text)
    await state.set_state(Form.hozirgi_ish)
    await message.answer("14) Hozir qayerda ishlaysiz..?")


@dp.message(Form.hozirgi_ish)
async def get_hozirgi_ish(message: types.Message, state: FSMContext):
    await state.update_data(hozirgi_ish=message.text)
    await state.set_state(Form.oldingi_ish)
    await message.answer("15) Avval qayerda ishlagansiz..?")


@dp.message(Form.oldingi_ish)
async def get_oldingi_ish(message: types.Message, state: FSMContext):
    await state.update_data(oldingi_ish=message.text)
    await state.set_state(Form.rasm)
    await message.answer(
        "16) O'zingiz tushgan selfie yoki shaxsingizni ifodalaydigan biror suratingizni yoboring..!\n\n"
        "(HD bo'lishi shart, makiyaj va effektlar bilan yuborilgan suratlar anketa bekor bo'lishiga "
        "sabab bo'ladi..! Surat bizda maxfiy saqlanadi..!)"
    )


@dp.message(Form.rasm, F.photo)
async def get_photo(message: types.Message, state: FSMContext):
    await state.update_data(photo=message.photo[-1].file_id)
    await state.set_state(Form.tayyor)

    markup = ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text="✅ Yuborish")]],
        resize_keyboard=True
    )
    await message.answer(
        "Barcha ma'lumotlar qabul qilindi. Yuborish uchun tugmani bosing:",
        reply_markup=markup
    )


@dp.message(Form.rasm)
async def get_photo_invalid(message: types.Message, state: FSMContext):
    await message.answer("Iltimos, rasm (surat) yuboring.")


@dp.message(Form.tayyor, F.text == "✅ Yuborish")
async def send_to_group(message: types.Message, state: FSMContext):
    data = await state.get_data()

    caption = (
        "🆕 Yangi anketa! (\"SUSAMBIL\")\n\n"
        f"1) Familiya va ism: {data.get('ism')}\n"
        f"2) Telefon raqam: {data.get('telefon')}\n"
        f"3) Yosh: {data.get('yosh')}\n"
        f"4) Yashash manzili: {data.get('manzil')}\n"
        f"5) Qiziqtirgan soxa: {data.get('soxa')}\n"
        f"6) Tajriba: {data.get('tajriba')}\n"
        f"7) 12 soatlik ish kuniga rozilik: {data.get('ish_vaqti')}\n"
        f"8) Transport muammosi: {data.get('transport')}\n"
        f"9) Kutilayotgan maosh: {data.get('maosh')}\n"
        f"10) Oilaviy holati: {data.get('oilaviy')}\n"
        f"11) Farzandlar soni: {data.get('farzand')}\n"
        f"12) Dam olish kunisiz ishlashga rozilik: {data.get('dam_olish')}\n"
        f"13) Taxsil olgan maktab: {data.get('maktab')}\n"
        f"14) Hozirgi ish joyi: {data.get('hozirgi_ish')}\n"
        f"15) Oldingi ish joyi: {data.get('oldingi_ish')}\n"
        f"🆔 Username: @{message.from_user.username if message.from_user.username else 'mavjud emas'}"
    )

    await bot.send_photo(GROUP_ID, data.get("photo"), caption=caption)

    await message.answer(
        "✅ Anketangiz muvaffaqiyatli yuborildi. Rahmat!",
        reply_markup=ReplyKeyboardRemove()
    )

    await state.clear()


@dp.message(Form.tayyor)
async def tayyor_invalid(message: types.Message, state: FSMContext):
    await message.answer("Yuborish uchun \"✅ Yuborish\" tugmasini bosing.")


async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
