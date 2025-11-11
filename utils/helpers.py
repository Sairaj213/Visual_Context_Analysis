from PIL import Image

def combine_images(image_a_bytes, image_b_bytes):

    img_a = Image.open(image_a_bytes)
    img_b = Image.open(image_b_bytes)

    h_a, h_b = img_a.height, img_b.height
    new_h = min(h_a, h_b)

    img_a = img_a.resize((int(img_a.width * new_h / h_a), new_h))
    img_b = img_b.resize((int(img_b.width * new_h / h_b), new_h))

    dst = Image.new('RGB', (img_a.width + img_b.width, new_h))
    dst.paste(img_a, (0, 0))
    dst.paste(img_b, (img_a.width, 0))

    return dst
