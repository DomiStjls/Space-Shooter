from PIL import Image

for i in range(1, 61):
    img = Image.new('RGB', (100, 100), (int(255 / 60 * i), int(255 / 60 * i), int(255 / 60 * i)))
    img.save(f"{i}.png")
