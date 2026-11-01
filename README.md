# Цифровое изображение и цвет (Занятие 2)

Репозиторий содержит выполненные задания к лекции **«Цифровое изображение и цвет»**.  
Скрипт `main.py` последовательно выполняет три практические работы: базовую обработку изображений через **Pillow**, операции с массивами через **NumPy** и построение гистограмм через **Matplotlib**.

## 📋 Содержание работ

### 1. Базовые операции (Pillow)
- вывод формата, размера и режима изображения;
- сохранение `original.png`;
- выделение каналов R, G, B с цветовой визуализацией;
- перевод в оттенки серого (`gray.png`);
- квантование до 8 цветов (`quantized_8.png`).

### 2. ROI и цветовая маска
- выделение прямоугольной области `crop((350, 70, 930, 690))` → `roi.png`;
- маска голубого неба в пространстве HSV (`mask_sky.png`);
- объединение масок через `ImageChops.multiply()`;
- `sky_only.png` (небо на белом фоне) и `object_only.png` (объект без неба);
- инвертированная маска объекта (`mask_object.png`).

### 3. NumPy-операции и гистограммы
- функции `change_brightness`, `change_contrast`, `invert`, `quantize` на массивах NumPy с защитой от переполнения (`np.clip`);
- сохранение результатов: `bright.png`, `contrast.png`, `inverted.png`, `quantized_16_numpy.png`;
- гистограмма яркости (`hist_gray.png`);
- совмещённая гистограмма каналов RGB с легендой (`hist_rgb.png`);
- гистограмма после квантования яркости до 8 уровней (`hist_quantized.png`).

## 📁 Структура проекта

```text
.
├── cow.png                  # исходное изображение
├── main.py                  # все три задания
└── result/                  # результаты, создаётся автоматически
    ├── original.png
    ├── channel_r.png
    ├── channel_g.png
    ├── channel_b.png
    ├── gray.png
    ├── quantized_8.png
    ├── roi.png
    ├── mask_sky.png
    ├── sky_only.png
    ├── mask_object.png
    ├── object_only.png
    ├── bright.png
    ├── contrast.png
    ├── inverted.png
    ├── quantized_16_numpy.png
    ├── hist_gray.png
    ├── hist_rgb.png
    └── hist_quantized.png
```

## 🛠️ Требования

- Python 3.8+
- Библиотеки: `Pillow`, `NumPy`, `Matplotlib`

Установка зависимостей:

```bash
pip install Pillow numpy matplotlib
```

## 🚀 Запуск

```bash
git clone https://github.com/SparrowHawk0087/SEC-visual-ai-lecture-2.git
cd SEC-visual-ai-lecture-2
python main.py
```

Все результаты сохраняются в папку `result/`. Скрипт создаёт её автоматически при отсутствии.

## 📝 Примечания

- `main.py` содержит все три части в одном файле и выполняется последовательно.
- Для корректной работы необходим файл `cow.png` в корневой папке проекта.
- Гистограммы строятся с подписанными осями и сохраняются в разрешении 150 dpi.

---

*Учебный курс « НОК "Визуальный ИИ: начальный практикум"».*
