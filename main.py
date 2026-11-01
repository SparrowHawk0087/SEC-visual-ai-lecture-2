from PIL import Image, ImageOps, ImageChops
import numpy as np
from pathlib import Path
import matplotlib.pyplot as plt 


# яркость и контраст через NumPy
def change_brightness(array, delta):
    work = array.astype(np.int16)
    work += delta
    return np.clip(work, 0, 255).astype(np.uint8)


def change_contrast(array, factor):
    work = array.astype(np.float32)
    work = (work - 128) * factor + 128
    return np.clip(work, 0, 255).astype(np.uint8)


# инверсия и квантизация через NumPy
def invert(array):
    return 255 - array


def quantize(array, levels):
    if levels < 2:
        raise ValueError("Количество уровней должно быть >= 2")

    work = array.astype(np.float32)
    work = np.round((work / 255) * (levels - 1))
    work = (work / (levels - 1)) * 255
    return work.astype(np.uint8)


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

# -------- Часть 3. Сравнение изображений --------

# переход от Pillow к NumPy
image_array = np.array(image)
print(image_array.shape)  # (height, width, channels)
print(image_array.dtype)  # uint8
print(image_array.min(), image_array.max())

pixel = image_array[100, 200]   # [R, G, B]

# возврат массива в Pillow
bright = change_brightness(image_array, 50)
contrast = change_contrast(image_array, 1.4)
inverted = invert(image_array)
quantized_pt3 = quantize(image_array, 16)

# гистограмма яркости
gray_array = np.array(gray)

fig, ax = plt.subplots(figsize=(8, 5))
ax.hist(gray_array.ravel(), bins=256, range=(0, 256))
ax.set_xlabel("Значение яркости")
ax.set_ylabel("Число пикселей")
fig.savefig("result/hist_gray.png", dpi=150)
plt.close(fig)

# гистограммы каналов RGB
fig, ax = plt.subplots(figsize=(8, 5))
colors = ["red", "green", "blue"]
labels = ["R", "G", "B"]

for channel in range(3):
    values = image_array[:, :, channel]
    ax.hist(values.ravel(), bins=256, range=(0, 256),
            histtype="step", color=colors[channel],
            label=labels[channel])

ax.legend()
fig.savefig("result/hist_rgb.png", dpi=150)
plt.close(fig)

# гистограмма после квантизации яркости
gray_array = np.array(image.convert("L"))
levels = 8

indices = np.rint(
    gray_array.astype(np.float32) * (levels - 1) / 255
)
quantized_array = np.rint(
    indices * 255 / (levels - 1)
).astype(np.uint8)

values, counts = np.unique(quantized_array, return_counts=True)
fig, ax = plt.subplots(figsize=(8, 5))
ax.bar(values, counts, width=18, color="#E25E28")
ax.set_xticks(values)
ax.set_xlim(0, 255)
ax.set_xlabel("Значение яркости")
ax.set_ylabel("Число пикселей")
fig.savefig("result/hist_quantized.png", dpi=150)
plt.close(fig)


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

# по части 3
Image.fromarray(bright).save(result_dir/"bright.png")
Image.fromarray(contrast).save(result_dir/"contrast.png")
Image.fromarray(inverted).save(result_dir/"inverted.png")
Image.fromarray(quantized_pt3).save(result_dir/"quantized_16_numpy.png")