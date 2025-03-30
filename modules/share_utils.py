# modules/share_utils.py

def generate_download_link(image_url: str) -> str:
    """
    Generates a direct download link for the generated image.
    """
    return f'<a href="{image_url}" download="ghibli-style.png" target="_blank">📥 Download Image</a>'


def generate_instagram_link(image_url: str) -> str:
    """
    Provides a CTA for users to share the image on Instagram manually.
    (Due to Instagram API limitations, we can't auto-post — only pre-share).
    """
    return (
        f'<a href="{image_url}" target="_blank" rel="noopener noreferrer">'
        f'📸 Share this image on Instagram manually</a><br><small>*Open this link in your Instagram mobile app to share as story or post*</small>'
    )
