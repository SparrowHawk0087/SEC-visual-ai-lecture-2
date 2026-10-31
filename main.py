from PIL import Image, ImageOps
import numpy as np
from pathlib import Path

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


# coхранение файлов
result_dir = Path("result")
result_dir.mkdir(exist_ok=True)

image.save(result_dir/"original.png")
red.save(result_dir/"channel_r.png")
green.save(result_dir/"channel_g.png")
blue.save(result_dir/"channel_b.png")
gray.save(result_dir/"gray.png")
quantized.save(result_dir/"quantized_8.png")

