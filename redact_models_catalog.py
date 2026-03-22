from PIL import Image, ImageDraw

# Load the image
img = Image.open(r'images\04-workbench\01-models-catalog.png')

# Create a drawing context
draw = ImageDraw.Draw(img)

# Get the background color from the top-right area (dark theme)
# Sample a pixel from the header area
bg_color = img.getpixel((550, 8))
print(f"Background color sampled: {bg_color}")

# Redact the name "Umar, Matt" in the upper right corner
# This should be around x: 520-560, y: 4-14
draw.rectangle(
    [(520, 4), (560, 14)],
    fill=bg_color
)

# Save the modified image
img.save(r'images\04-workbench\01-models-catalog.png')
print("Personal information redacted from 01-models-catalog.png")
