from io import BytesIO
from PIL import Image
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from aiogram import Bot, types
from aiogram.types import InputFile
from loader import dp, bot
import os

images = []

@dp.message_handler(content_types=types.ContentType.PHOTO)
async def handle_photo(message: types.Message):
    photo = message.photo[-1]
    file = await bot.download_file_by_id(photo.file_id)
    photo_file = BytesIO(file.read())
    images.append(photo_file)

    await message.reply("Расм муваффакийатли юкланди✅!")


@dp.message_handler(text='PDF килиш')
async def create_pdf(message: types.Message):
    if not images:
        await message.reply("Сиз хали хеч кандай расм юбормадингиз. Илтимос, менга расм юборинг, сизга PDF килиб беришим учун.")
        return

    try:
        if not os.path.exists("temp"):
            os.makedirs("temp")

        pdf_filename = "output.pdf"
        c = canvas.Canvas(pdf_filename, pagesize=letter)

        for idx, image in enumerate(images):
            image_path = f"temp/image{idx}.png"
            with open(image_path, "wb") as f:
                f.write(image.getbuffer())

            try:
                img = Image.open(image_path)
                img_width, img_height = img.size

                # Calculate the scale factors to fit the image within the page dimensions
                scale_x = (letter[0] - 40) / img_width  # Subtracting 40 to account for margins
                scale_y = (letter[1] - 40) / img_height

                # Choose the smaller scale factor to ensure the image fits completely within the page
                scale_factor = min(scale_x, scale_y)

                new_width = img_width * scale_factor
                new_height = img_height * scale_factor

                x = (letter[0] - new_width) / 2
                y = (letter[1] - new_height) / 2

                c.drawInlineImage(image_path, x, y, width=new_width, height=new_height)
                c.showPage()

            except Exception as e:
                print(f"Хатолик расмни олишда: {str(e)}")

        c.save()

        with open(pdf_filename, 'rb') as pdf_file:
            await message.reply_document(InputFile(pdf_file))

    finally:
        images.clear()
