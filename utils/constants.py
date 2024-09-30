# utils/constants.py

# Define role constants
ROLE_JANITOR = 'janitor'
ROLE_MODERATOR = 'moderator'
ROLE_ADMIN = 'admin'

# Define Redis key patterns
REDIS_KEY_USER = "user:{}"
REDIS_KEY_ROOM = "room:{}"
REDIS_KEY_MESSAGE = "room:{}:messages:{}"
REDIS_KEY_MUTED = "room:{}:muted:{}"
REDIS_KEY_BANNED = "room:{}:banned:{}"
REDIS_KEY_GLOBAL_BANNED = "global_banned:{}"