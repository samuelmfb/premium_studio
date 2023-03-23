# blue prints are imported 
# explicitly instead of using *
# from .user import user_views
from .index import index_views
from .customer import customer_views
from .project import project_views
from .task import task_views


views = [index_views,customer_views, project_views, task_views] 
# blueprints must be added to this list