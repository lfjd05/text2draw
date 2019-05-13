from PIL import Image
import matplotlib.pyplot as plt


resize_x = 128
resize_y = 128

img = Image.open('D:/python Programme/text2draw_flod/png_data/棒球棒/4709218089172992.png')
img = img.convert("RGB")
img = img.resize((resize_x, resize_y))
plt.figure("dog")
plt.imshow(img)
plt.show()
