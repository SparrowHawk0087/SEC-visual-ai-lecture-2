from PIL import Image, ImageOps, ImageChops
import numpy as np
from pathlib import Path

# ------------ Часть 1. Работа с изображениями ------------

# информация о фото
image = Image.open("cow.png")

print("=== Информация о фото ===")
print(f"Формат: {image.format}")
print(f"Размер: {image.size}")
print(f"Режим: {image.mode}\n")

# конвертируем RGBA изображение в RGB
image = image.convert('RGB')
#image.show()

"""print(image.getpixel((300, 150)))

arr = np.asarray(image)
print(arr[150, 300])"""

# через split получаем три режима L (уровней) 
r, g, b = image.split()

# формируем по уровням цветов новые изображения, не изменяя исходное
red = ImageOps.colorize(r, black="white", white="red")
green = ImageOps.colorize(g, black="white", white="green")
blue = ImageOps.colorize(b, black="white", white="blue")

# преобразование в оттенки серого
gray = image.convert("L")
print("=== Преобразование в оттенки серого ===")
print("Режим gray:", gray.mode)  # L
#gray.show()

# квантизация
quantized = image.quantize(colors=8)
quantized = quantized.convert("RGB")
print("\n=== Квантизация ===")
print("Размер:", quantized.size)
print("Режим:", quantized.mode)

# ------- Часть 2. Область интереса и маска по цвету --------

# область интереса (ROI)
box = (350, 70, 930, 690)
roi = image.crop(box)

# маска голубого неба
h, s, v = image.convert("HSV").split()

mask_h = h.point(
    lambda p: 255 if 125 <= p <= 190 else 0
)
mask_s = s.point(
    lambda p: 255 if p >= 35 else 0
)
mask_v = v.point(
    lambda p: 255 if p >= 120 else 0
)

# объединение условий маски
mask = ImageChops.multiply(mask_h, mask_s)
mask = ImageChops.multiply(mask, mask_v)

sky_only = Image.new("RGB", image.size, "white")    # создаем белый фон
sky_only.paste(image, mask=mask)                  # накладываем маску на фото

# инверсия маски
object_mask = ImageOps.invert(mask)

object_only = Image.new("RGB", image.size, "white")    # создаем белый фон
object_only.paste(image, mask=object_mask)             # накладываем маску на фото

# ------ Сохранение файлов по всем частям --------

# coхранение файлов
result_dir = Path("result")
result_dir.mkdir(exist_ok=True)

# по части 1
image.save(result_dir/"original.png")
red.save(result_dir/"channel_r.png")
green.save(result_dir/"channel_g.png")
blue.save(result_dir/"channel_b.png")
gray.save(result_dir/"gray.png")
quantized.save(result_dir/"quantized_8.png")

# по части 2
roi.save(result_dir/"roi.png")
mask.save(result_dir/"mask_sky.png")
sky_only.save(result_dir/"sky_only.png")
object_mask.save(result_dir/"mask_object.png")
object_only.save(result_dir/"object_only.png")

