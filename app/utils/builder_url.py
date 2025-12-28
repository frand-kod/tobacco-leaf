from app.core.config import settings

def build_img_url(path:str):
    return f"{settings.BASE_URL}/uploads/{path}"