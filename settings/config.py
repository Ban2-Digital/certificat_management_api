from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

############################ SERVER CONFIG ############################
PROD_SERVER_URL = "https://"
DEV_SERVER_URL = "http://127.0.0.1:8000"
BASE_URL = DEV_SERVER_URL

############################ MEDIAS CONFIG ############################
MEDIA_ROOT = BASE_DIR / "mediafiles/"
# print(MEDIA_ROOT)
MEDIA_URL = "medias/"

############################ DATABASE CONFIG ############################
DATABASE = {
    'ENGINE': "postgresql",
    'NAME': "formation_db",
    'USERNAME': "postgres",
    'PASSWORD': "carmello96",
    'HOST': "localhost",
    'PORT': "5432"
    
}