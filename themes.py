from discord import PartialEmoji

import config

################################################################################
DICT_THEME_2D = {"theme": "2d",
                 "role_id": config.ROLE_DESSINATEUR_ID}

DICT_THEME_3D = {"theme": "3d",
                 "role_id": config.ROLE_GRAPHISTE_3D_ID}

DICT_THEME_JEUX = {"theme": "jeux",
                   "role_id": config.ROLE_GAME_DESIGNER_ID}

DICT_THEME_PHOTO = {"theme": "photo",
                    "role_id": config.ROLE_PHOTOGRAPHE_ID}

DICT_THEME_VIDEO = {"theme": "vidéo",
                    "role_id": config.ROLE_VIDEASTE_ID}

DICT_THEME_MUSIQUE = {"theme": "musique",
                      "role_id": config.ROLE_MUSICIEN_ID}

DICT_THEME_DIY = {"theme": "diy",
                  "role_id": config.ROLE_BRICOLEUR_ID}

DICT_THEME_ECRITURE = {"theme": "écriture",
                       "role_id": config.ROLE_ECRIVAIN_ID}

DICT_THEMES_EMOJI = {PartialEmoji(name="🎨"): DICT_THEME_2D,
                     PartialEmoji(name="💻"): DICT_THEME_3D,
                     PartialEmoji(name="🎮"): DICT_THEME_JEUX,
                     PartialEmoji(name="📷"): DICT_THEME_PHOTO,
                     PartialEmoji(name="🎥"): DICT_THEME_VIDEO,
                     PartialEmoji(name="🎵"): DICT_THEME_MUSIQUE,
                     PartialEmoji(name="🛠️"): DICT_THEME_DIY,
                     PartialEmoji(name="✍️"): DICT_THEME_ECRITURE}
################################################################################
