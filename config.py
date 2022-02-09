import os

from dotenv import load_dotenv


################################################################################

# Loading environment configuration variables
load_dotenv(".config")

TOKEN = os.getenv("TOKEN")

# CHANNELS
CHANNEL_LA_CARTE_ID = int(os.getenv("CHANNEL_LA_CARTE_ID"))

# MESSAGES
CHOOSE_THEMES_MESSAGE_ID = int(os.getenv("CHOOSE_THEMES_MESSAGE_ID"))

# ROLES
# Ranking
ROLE_CLIENT_DE_PASSAGE_ID = int(os.getenv("CLIENT_DE_PASSAGE_ID"))

# Themes
ROLE_DESSINATEUR_ID = int(os.getenv("ROLE_DESSINATEUR_ID"))
ROLE_GRAPHISTE_3D_ID = int(os.getenv("ROLE_GRAPHISTE_3D_ID"))
ROLE_GAME_DESIGNER_ID = int(os.getenv("ROLE_GAME_DESIGNER_ID"))
ROLE_PHOTOGRAPHE_ID = int(os.getenv("ROLE_PHOTOGRAPHE_ID"))
ROLE_VIDEASTE_ID = int(os.getenv("ROLE_VIDEASTE_ID"))
ROLE_MUSICIEN_ID = int(os.getenv("ROLE_MUSICIEN_ID"))
ROLE_BRICOLEUR_ID = int(os.getenv("ROLE_BRICOLEUR_ID"))
ROLE_ECRIVAIN_ID = int(os.getenv("ROLE_ECRIVAIN_ID"))


################################################################################