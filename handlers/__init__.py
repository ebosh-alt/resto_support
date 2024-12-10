from .supports import supports_routers
from .users import users_routers

routers = (*users_routers, *supports_routers)


