import asyncio
import json
import os
from typing import Dict, List, Tuple

import aiofiles
import aiohttp
from aiogram import Bot, Dispatcher, Router, F, types
from aiogram.filters import CommandStart, Command
from aiogram.types import (
    InlineKeyboardMarkup, InlineKeyboardButton,
    ReplyKeyboardMarkup, KeyboardButton,
    Message, CallbackQuery
)
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.storage.memory import MemoryStorage

# ================== НАСТРОЙКИ ==================
LASTFM_API_KEY = "8ebef8e66cfa80440fa674a4377d0f06"   # ВСТАВЬ КЛЮЧ
BOT_TOKEN = "8599346365:AAGWxz95TGmfvsfDGCpz5L_VVruNrqo-pdM"        # ВСТАВЬ ТОКЕН

DATA_FILE = "user_favorites.json"

# ================== ИНИЦИАЛИЗАЦИЯ ==================
bot = Bot(token=BOT_TOKEN)
storage = MemoryStorage()
dp = Dispatcher(storage=storage)
router = Router()
dp.include_router(router)

# Глобальные данные (загрузим в main)
user_data: Dict[str, List[str]] = {}

# ================== ХРАНЕНИЕ ИЗБРАННОГО ==================
async def load_data() -> Dict[str, List[str]]:
    if not os.path.exists(DATA_FILE):
        return {}
    try:
        async with aiofiles.open(DATA_FILE, "r", encoding="utf-8") as f:
            content = await f.read()
            if not content.strip():
                return {}
            data = json.loads(content)
            # гарантия типа
            if isinstance(data, dict):
                return {str(k): list(v) for k, v in data.items()}
    except Exception as e:
        print(f"Ошибка загрузки данных: {e}")
    return {}

async def save_data(data: Dict[str, List[str]]):
    try:
        async with aiofiles.open(DATA_FILE, "w", encoding="utf-8") as f:
            await f.write(json.dumps(data, ensure_ascii=False, indent=2))
    except Exception as e:
        print(f"Ошибка сохранения данных: {e}")

# ================== КЛАВИАТУРЫ ==================
def get_main_keyboard() -> ReplyKeyboardMarkup:
    kb = [
        [KeyboardButton(text="🔍 Поиск песни"),
         KeyboardButton(text="⭐️ Рейтинг песни")],
        [KeyboardButton(text="❤️ Добавить в избранное"),]
    ]
    return ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)

def get_inline_buttons() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="🔍 Поиск", callback_data="search_song"),
            InlineKeyboardButton(text="⭐️ Рейтинг", callback_data="get_rating")
        ],
        [
            InlineKeyboardButton(text="❤️ В избранное", callback_data="save_favorite"),
        ],
        [
            InlineKeyboardButton(text="❌ Очистить избранное", callback_data="clear_favorites"),
            InlineKeyboardButton(text="ℹ️ Помощь", callback_data="show_help")
        ]
    ])

# ================== СОСТОЯНИЯ (FSM) ==================
class SongStates(StatesGroup):
    waiting_for_song = State()

# ================== ПОМОЩНИКИ ==================
async def lastfm_request(method: str, **params) -> dict:
    url = "https://ws.audioscrobbler.com/2.0/"
    payload = {
        "method": method,
        "api_key": LASTFM_API_KEY,
        "format": "json",
        **params
    }
    async with aiohttp.ClientSession() as session:
        async with session.get(url, params=payload, timeout=15) as resp:
            resp.raise_for_status()
            return await resp.json()

def parse_artist_track(text: str) -> Tuple[str, str]:
    """
    Возвращает (artist, track)
    Форматы:
      - "Артист - Трек"
      - "Трек - Артист" (если так ввели — всё равно попробуем)
      - "Трек Артист" (последнее слово артист)
      - "Только трек" -> artist="Various Artists"
    """
    text = (text or "").strip()
    if not text:
        return "Various Artists", ""

    if " - " in text:
        left, right = text.split(" - ", 1)
        left = left.strip()
        right = right.strip()
        # Считаем что чаще пишут "Артист - Трек"
        if left and right:
            return left, right

    words = text.split()
    if len(words) >= 2:
        artist = words[-1]
        track = " ".join(words[:-1])
        return artist.strip(), track.strip()

    return "Various Artists", text

async def show_favorites(message: Message):
    user_id = str(message.from_user.id)
    favs = user_data.get(user_id, [])

    if not favs:
        text = "📭 У вас пока нет сохранённых песен.\n\nДобавьте песни через ❤️ В избранное."
    else:
        lines = [f"{i}. {song}" for i, song in enumerate(favs, 1)]
        text = f"❤️ <b>Ваши любимые песни ({len(favs)}):</b>\n\n" + "\n".join(lines)

    await message.answer(text, parse_mode="HTML", reply_markup=get_inline_buttons())

# ================== КОМАНДЫ ==================
@router.message(CommandStart())
async def cmd_start(message: Message):
    await message.answer(
        "🎵 <b>Добро пожаловать в Music Info Bot!</b>\n\n"
        "Я помогу найти информацию о песнях через Last.fm.\n"
        "Выберите действие:",
        parse_mode="HTML",
        reply_markup=get_main_keyboard()
    )
    await message.answer("Или используйте кнопки:", reply_markup=get_inline_buttons())

@router.message(Command("help"))
async def cmd_help(message: Message):
    help_text = (
        "📋 <b>Доступные команды:</b>\n\n"
        "<b>Основные:</b>\n"
        "• /start — старт\n"
        "• /help — помощь\n"
        "• /search — поиск\n"
        "• /rating — рейтинг\n"
        "• /favorites — избранное\n"
        "• /clear — очистить избранное\n\n"
        "<b>Формат ввода:</b>\n"
        "• Артист - Песня (Queen - Bohemian Rhapsody)\n"
        "• Песня Артист (Bohemian Rhapsody Queen)\n"
        "• Просто название песни\n"
    )
    await message.answer(help_text, parse_mode="HTML", reply_markup=get_inline_buttons())

@router.message(Command("search"))
async def cmd_search(message: Message, state: FSMContext):
    await message.answer("Введите название песни и артиста (пример: Queen - Bohemian Rhapsody):")
    await state.set_state(SongStates.waiting_for_song)
    await state.update_data(action="search_song")

@router.message(Command("rating"))
async def cmd_rating(message: Message, state: FSMContext):
    await message.answer("Введите название песни и артиста для рейтинга:")
    await state.set_state(SongStates.waiting_for_song)
    await state.update_data(action="get_rating")

@router.message(Command("favorites"))
async def cmd_favorites(message: Message):
    await show_favorites(message)

@router.message(Command("clear"))
async def cmd_clear(message: Message):
    user_id = str(message.from_user.id)
    if user_data.get(user_id):
        user_data[user_id] = []
        await save_data(user_data)
        await message.answer("✅ Избранное очищено!", reply_markup=get_inline_buttons())
    else:
        await message.answer("📭 В избранном ничего нет.", reply_markup=get_inline_buttons())

# ================== ReplyKeyboard ==================
@router.message(F.text == "🔍 Поиск песни")
async def kb_search_song(message: Message, state: FSMContext):
    await message.answer("Введите название песни и артиста (пример: Queen - Bohemian Rhapsody):")
    await state.set_state(SongStates.waiting_for_song)
    await state.update_data(action="search_song")

@router.message(F.text == "⭐️ Рейтинг песни")
async def kb_get_rating(message: Message, state: FSMContext):
    await message.answer("Введите название песни и артиста:")
    await state.set_state(SongStates.waiting_for_song)
    await state.update_data(action="get_rating")

@router.message(F.text == "❤️ Добавить в избранное")
async def kb_save_favorite(message: Message, state: FSMContext):
    await message.answer("Введите песню для добавления (можно просто текст):")
    await state.set_state(SongStates.waiting_for_song)
    await state.update_data(action="save_favorite")


# ================== Inline-кнопки ==================
@router.callback_query(F.data == "search_song")
async def cb_search_song(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    await callback.message.answer("Введите название песни и артиста:")
    await state.set_state(SongStates.waiting_for_song)
    await state.update_data(action="search_song")

@router.callback_query(F.data == "get_rating")
async def cb_get_rating(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    await callback.message.answer("Введите название песни и артиста:")
    await state.set_state(SongStates.waiting_for_song)
    await state.update_data(action="get_rating")

@router.callback_query(F.data == "save_favorite")
async def cb_save_favorite(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    await callback.message.answer("Введите песню для добавления (можно просто текст):")
    await state.set_state(SongStates.waiting_for_song)
    await state.update_data(action="save_favorite")

@router.callback_query(F.data == "my_favorites")
async def cb_my_favorites(callback: CallbackQuery):
    await callback.answer()
    await show_favorites(callback.message)

@router.callback_query(F.data == "clear_favorites")
async def cb_clear_favorites(callback: CallbackQuery):
    await callback.answer()
    user_id = str(callback.from_user.id)
    if user_data.get(user_id):
        user_data[user_id] = []
        await save_data(user_data)
        await callback.message.answer("✅ Избранное очищено!", reply_markup=get_inline_buttons())
    else:
        await callback.message.answer("📭 В избранном ничего нет.", reply_markup=get_inline_buttons())

@router.callback_query(F.data == "show_help")
async def cb_show_help(callback: CallbackQuery):
    await callback.answer()
    await cmd_help(callback.message)

# ================== ОБРАБОТКА ВВОДА ПЕСНИ ==================
@router.message(SongStates.waiting_for_song)
async def process_song_input(message: Message, state: FSMContext):
    user_input = (message.text or "").strip()
    st = await state.get_data()
    action = st.get("action")

    try:
        if not user_input:
            await message.answer("❌ Пустой запрос. Попробуйте ещё раз.", reply_markup=get_inline_buttons())
            return

        # 1) Сохранение в избранное (как ввели)
        if action == "save_favorite":
            user_id = str(message.from_user.id)
            user_data.setdefault(user_id, [])
            if user_input in user_data[user_id]:
                await message.answer(f"ℹ️ Уже есть в избранном: <b>{user_input}</b>",
                                     parse_mode="HTML", reply_markup=get_inline_buttons())
            else:
                user_data[user_id].append(user_input)
                await save_data(user_data)
                await message.answer(f"✅ Добавлено в избранное: <b>{user_input}</b>",
                                     parse_mode="HTML", reply_markup=get_inline_buttons())
            return

        # 2) Поиск / рейтинг через Last.fm
        artist, track = parse_artist_track(user_input)
        if not track:
            await message.answer("❌ Не понял название песни. Пример: Queen - Bohemian Rhapsody",
                                 reply_markup=get_inline_buttons())
            return

        data = await lastfm_request("track.getInfo", artist=artist, track=track, autocorrect=1)

        # если ошибка или нет трека — пробуем поиск
        if data.get("error") or "track" not in data:
            search_data = await lastfm_request("track.search", track=user_input, limit=3)
            tracks = search_data.get("results", {}).get("trackmatches", {}).get("track", [])
            if tracks:
                suggestions = []
                for t in tracks[:3]:
                    n = t.get("name", "")
                    a = t.get("artist", "")
                    suggestions.append(f"• {a} - {n}")
                await message.answer(
                    "❌ Точного совпадения не найдено.\n\n"
                    "<b>Возможно, вы имели в виду:</b>\n"
                    + "\n".join(suggestions),
                    parse_mode="HTML",
                    reply_markup=get_inline_buttons()
                )
            else:
                await message.answer(
                    "❌ Песня не найдена. Проверьте написание.\n"
                    "Формат: <i>Артист - Песня</i> или <i>Песня Артист</i>",
                    parse_mode="HTML",
                    reply_markup=get_inline_buttons()
                )
            return

        song = data["track"]
        name = song.get("name", "—")
        artist_name = song.get("artist", {}).get("name", "—")
        listeners = int(song.get("listeners", 0) or 0)
        playcount = int(song.get("playcount", 0) or 0)
        album = song.get("album", {}).get("title", "неизвестный альбом")

        tags_data = song.get("toptags", {}).get("tag", [])
        if isinstance(tags_data, dict):  # иногда бывает не список
            tags_data = [tags_data]
        tags = ", ".join([t.get("name", "") for t in tags_data[:5] if t.get("name")]) or "нет тегов"

        if action == "search_song":
            text = (
                f"🎵 <b>{name}</b>\n"
                f"👤 <b>Артист:</b> {artist_name}\n"
                f"💿 <b>Альбом:</b> {album}\n"
                f"👂 <b>Слушателей:</b> {listeners:,}\n"
                f"▶️ <b>Прослушиваний:</b> {playcount:,}\n"
                f"🏷 <b>Теги:</b> {tags}\n"
            )

            add_kb = InlineKeyboardMarkup(inline_keyboard=[
                [InlineKeyboardButton(
                    text="❤️ Добавить эту песню в избранное",
                    callback_data=f"add_current:{artist_name} - {name}"
                )],
                [InlineKeyboardButton(text="⬅️ Меню", callback_data="show_help")]
            ])

            await message.answer(text, parse_mode="HTML", reply_markup=add_kb)

        elif action == "get_rating":
            rating_score = min(10, listeners // 10000) if listeners > 0 else 0
            stars = "⭐️" * int(rating_score)

            text = (
                f"📊 <b>Рейтинг песни</b>\n\n"
                f"🎵 <b>{name}</b>\n"
                f"👤 <b>Артист:</b> {artist_name}\n\n"
                f"👂 <b>Слушателей:</b> {listeners:,}\n"
                f"▶️ <b>Прослушиваний:</b> {playcount:,}\n"
                f"🎯 <b>Оценка популярности:</b> {rating_score}/10 {stars}\n"
            )
            await message.answer(text, parse_mode="HTML", reply_markup=get_inline_buttons())
        else:
            await message.answer("Нажмите кнопку действия ещё раз.", reply_markup=get_inline_buttons())

    except aiohttp.ClientError:
        await message.answer(
            "⚠️ Ошибка подключения к Last.fm API. Проверьте интернет.",
            reply_markup=get_inline_buttons()
        )
    except Exception as e:
        await message.answer(f"❌ Ошибка: {str(e)}", reply_markup=get_inline_buttons())
    finally:
        await state.clear()

# ================== ДОБАВИТЬ ТЕКУЩУЮ ПЕСНЮ ==================
@router.callback_query(F.data.startswith("add_current:"))
async def add_current_song(callback: CallbackQuery):
    await callback.answer()
    song_text = callback.data.replace("add_current:", "", 1).strip()

    user_id = str(callback.from_user.id)
    user_data.setdefault(user_id, [])

    if song_text in user_data[user_id]:
        await callback.message.answer(
            f"ℹ️ Уже есть в избранном: <b>{song_text}</b>",
            parse_mode="HTML",
            reply_markup=get_inline_buttons()
        )
    else:
        user_data[user_id].append(song_text)
        await save_data(user_data)
        await callback.message.answer(
            f"✅ Добавлено в избранное: <b>{song_text}</b>",
            parse_mode="HTML",
            reply_markup=get_inline_buttons()
        )

# ================== ОБРАБОТКА ЛЮБЫХ ТЕКСТОВ (НЕ МЕШАЕМ FSM) ==================
@router.message(F.text)
async def handle_any_text(message: Message, state: FSMContext):
    # Если есть активное состояние — НЕ трогаем, чтобы FSM-хэндлеры работали
    if await state.get_state() is not None:
        return

    if not (message.text or "").startswith("/"):
        await message.answer(
            "🤔 <b>Что вы хотите сделать?</b>\n\n"
            "Используйте кнопки ниже или команды:\n"
            "• /search — найти песню\n"
            "• /rating — рейтинг\n"
            "• /favorites — избранное\n"
            "• /help — помощь",
            parse_mode="HTML",
            reply_markup=get_inline_buttons()
        )

# ================== ЗАПУСК ==================
async def main():
    global user_data
    user_data = await load_data()

    print("=" * 50)
    print("🎵 Last.fm Music Bot запущен!")
    print("=" * 50)
    print(f"📊 Загружено пользователей: {len(user_data)}")
    print(f"💾 Файл данных: {DATA_FILE}")
    print("=" * 50)

    try:
        await dp.start_polling(bot)
    finally:
        await save_data(user_data)
        print("📁 Данные сохранены при завершении.")

if __name__ == "__main__":
    asyncio.run(main())