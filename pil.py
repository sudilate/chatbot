from PIL import Image

# Open the image
image = Image.open("/Users/amitsarang/Downloads/istockphoto-1495736381-1024x1024.jpg")

# Convert the image to GIF format
image.save("/Users/amitsarang/Desktop/my_chatenv/background_image.gif", "GIF")
