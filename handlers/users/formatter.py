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
        await message.reply(
            "Сиз хали хеч кандай расм юбормадингиз. Илтимос, менга расм юборинг, сизга PDF килиб беришим учун.")
        return

    if not os.path.exists("temp"):
        os.makedirs("temp")

    image_paths = []
    for idx, image in enumerate(images):
        image_path = f"temp/image{idx}.png"
        with open(image_path, "wb") as f:
            f.write(image.getbuffer())
        image_paths.append(image_path)

    pdf_filename = "output.pdf"
    c = canvas.Canvas(pdf_filename, pagesize=letter)
    max_width, max_height = 400, 250
    spacing = 20

    def calculate_new_dimensions(img, max_width, max_height):
        width, height = img.size
        aspect_ratio = width / height
        if aspect_ratio > max_width / max_height:
            new_width = max_width
            new_height = int(max_width / aspect_ratio)
        else:
            new_width = int(max_height * aspect_ratio)
            new_height = max_height
        return new_width, new_height

    x = (letter[0] - max_width) / 2
    y = 500

    for image_path in image_paths:
        try:
            img = Image.open(image_path)
            new_width, new_height = calculate_new_dimensions(img, max_width, max_height)
            c.drawInlineImage(image_path, x, y, width=new_width, height=new_height)
            y -= new_height + spacing
            if y < 100:
                c.showPage()
                y = 500
        except Exception as e:
            print(f"Хатолик расмни олишда: {str(e)}")
    c.save()

    with open(pdf_filename, 'rb') as pdf_file:
        await message.reply_document(InputFile(pdf_file))






