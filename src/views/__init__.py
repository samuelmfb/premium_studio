# blue prints are imported 
# explicitly instead of using *
# from .user import user_views
from .index import index_views
from .customer import customer_views


views = [index_views,customer_views] 
# blueprints must be added to this list