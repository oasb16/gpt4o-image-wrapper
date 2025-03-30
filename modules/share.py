def generate_instagram_share_link(img_url):
    return f"https://www.instagram.com/create/story/?image_url={img_url}"

def generate_download_link(img_url):
    return f'<a href="{img_url}" download="gpt4o_image.png" target="_blank">📥 Download Image</a>'
