import asyncio
import logging
from aiogram import Bot, Dispatcher, types, F
from aiogram.client.default import DefaultBotProperties
from aiogram.filters.command import Command
from aiogram.types import ContentType, FSInputFile, URLInputFile
import numpy as np
import matplotlib.pyplot as plt
from sympy import symbols, Eq, solve, lambdify

logging.basicConfig(level=logging.INFO)
bot_properties = DefaultBotProperties(parse_mode="HTML")
bot = Bot("BOT_Token")
dp = Dispatcher()





@dp.message(Command('start'))
async def start(message: types.Message):

    photo1 = FSInputFile("photo/photo1.png")
    await bot.send_photo(message.from_user.id,
                         photo=photo1,
                         caption='''Hello! 👋 I’m <b>iConic Bot</b>, your personal math companion designed to make learning about <b>parabolas</b>, <b>ellipses</b>, and <b>hyperbolas</b> both fun and interactive! 🚀\n\n <b>Write</b> /function to draw function.''',
                         parse_mode='HTML')


@dp.message(Command('parabola'))
async def handle_function(message: types.Message):
    await message.reply_photo(
        caption="""<b>What is a Parabola?</b>\nA <b>parabola</b> is a <b>U-shaped</b> curve in mathematics. It can be wide, narrow, or even upside down, but it’s always perfectly symmetrical, like a mirror""",
        parse_mode='HTML',
        photo=FSInputFile("photo/parabola.png"))


@dp.message(Command('ellipse'))
async def handle_function(message: types.Message):
    await message.reply_photo(
        caption="""Imagine you have a flat piece of paper. Draw a <b>circle</b> on it. A circle is special because it’s perfectly round, and every point on its edge is the same distance from the center.\n\nBut what happens if you take that circle and gently <b>squish it</b> from the top and bottom? Now it looks like an oval shape. That squished circle is called an <b>ellipse!</b>""",
        parse_mode='HTML',
        photo=FSInputFile("photo/ellipse.png"))


@dp.message(Command('hyperbola'))
async def handle_function(message: types.Message):
    await message.reply_photo(
        caption="""<b>What is a Hyperbola?</b>\nA <b>hyperbola</b> is a special type of curve in math. It looks like two opposite, mirror-like curves that never touch. It’s like a pair of infinity symbols split in half!""",
        parse_mode='HTML',
        photo=FSInputFile("photo/hyperbola.png"))


@dp.message(Command('circle'))
async def handle_function(message: types.Message):
    await message.reply_photo(
        caption="""<b>What is a Circle?</b>\nA <b>circle</b> is a special type of shape in math. It looks like a perfectly round loop where every point on the curve is the exact same distance from the center. It’s like a never-ending ring!""",
        parse_mode='HTML',
        photo=FSInputFile("photo/circle.png"))


@dp.message(Command('books'))
async def handle_function(message: types.Message):
    await bot.send_message(message.from_user.id,
                           "Choose one of the books:",
                           reply_markup=types.InlineKeyboardMarkup(
                               inline_keyboard=[
                                   [types.InlineKeyboardButton(text="Математика ИЗ  А.П Ряушка",
                                                               callback_data="book1")],
                                   [types.InlineKeyboardButton(text="Humble Pie by Matt Parker",
                                                               callback_data="book2")],
                                   [types.InlineKeyboardButton(text="Linear Algebra by Sheldon Axler",
                                                               callback_data="book3")],
                                   [types.InlineKeyboardButton(text="MATH Mindsets by Jo Boaler",
                                                               callback_data="book4")],
				   [types.InlineKeyboardButton(text="Precalculus",
                                                               callback_data="book5")]
                               ]

                           ))


@dp.callback_query(F.data == "book1")
async def callback_book1(callback: types.CallbackQuery):
    await bot.send_document(callback.from_user.id,
                            document=FSInputFile("document/d1.pdf"),
                            caption="""<b>Математика ИЗ  А.П Ряушка</b>""",
                            parse_mode="HTML")

@dp.callback_query(F.data == "book5")
async def callback_book1(callback: types.CallbackQuery):
    await bot.send_document(callback.from_user.id,
                            document=FSInputFile("document/d5.pdf"),
                            caption="""<b>Precalculus</b>""",
                            parse_mode="HTML")
@dp.callback_query(F.data == "book2")
async def callback_book1(callback: types.CallbackQuery):
    await bot.send_document(callback.from_user.id,
                            document=FSInputFile("document/d2.pdf"),
                            caption="""<b>Humble Pie by Matt Parker</b>""",
                            parse_mode="HTML")


@dp.callback_query(F.data == "book3")
async def callback_book1(callback: types.CallbackQuery):
    await bot.send_document(callback.from_user.id,
                            document=FSInputFile("document/d3.pdf"),
                            caption="""<b>Linear Algebra by Sheldon Axler</b>""",
                            parse_mode="HTML")


@dp.callback_query(F.data == "book4")
async def callback_book1(callback: types.CallbackQuery):
    await bot.send_document(callback.from_user.id,
                            document=FSInputFile("document/d4.pdf"),
                            caption="""<b>MATH Mindsets by Jo Boaler</b>""",
                            parse_mode="HTML")


@dp.message(Command('function'))
async def handle_function(message: types.Message):
    await message.reply("Send me the equation of the function (e.g., `x^2 + y^2 - 16 = 0`) or with photo.")


@dp.message(F.content_type == ContentType.TEXT)
async def process_equation(message: types.Message):
    try:
        equation_input = message.text
        equation_input = equation_input.replace('^', '**')
        variables = sorted({char for char in equation_input if char.isalpha()})
        if len(variables) != 2:
            raise ValueError("The equation must have exactly two variables.")
        var1, var2 = symbols(variables)
        parsed_equation = Eq(
            *map(lambda s: eval(s, {variables[0]: var1, variables[1]: var2}), equation_input.split('=')))
        solutions = solve(parsed_equation, var2)
        functions = [lambdify(var1, sol, "numpy") for sol in solutions]
        var1_vals = np.linspace(-10, 10, 1000)
        plt.figure(figsize=(8, 8))
        for func in functions:
            try:
                var2_vals = func(var1_vals)
                plt.plot(var1_vals, var2_vals, label=f"{variables[1]} = {func}")
            except Exception as e:
                print(f"Error plotting function: {e}")
        plt.axhline(0, color='black', linewidth=0.5, linestyle='--')
        plt.axvline(0, color='black', linewidth=0.5, linestyle='--')
        plt.grid(color='gray', linestyle='--', linewidth=0.5)
        plt.title(f"Graph of: {equation_input}")
        plt.xlabel(variables[0])
        plt.ylabel(variables[1])
        plt.legend()
        file_path = "photo/function_plot.png"
        plt.savefig(file_path)
        plt.close()
        await bot.send_photo(message.from_user.id,
                             photo=FSInputFile(file_path))

    except Exception as e:
        await bot.send_message(message.from_user.id,
                               "You have written the function <b>incorrectly.</b> Check the values of <b>x</b>, <b>y</b>, or <b>both</b>.",
                               parse_mode='HTML')


async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
