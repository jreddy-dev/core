from app.db import SessionLocal, Base, engine
from app.models import User, Experiment, Video
from app.models_extra import Project, Node

Base.metadata.create_all(bind=engine)

session = SessionLocal()
# create demo user
u = User(email='demo@example.com', name='Demo')
session.add(u)
session.commit()

# create demo project
p = Project(owner_id=u.id, title='Demo Project', description='Demo')
session.add(p)
session.commit()

# create node + experiment
n = Node(project_id=p.id, type='experiment', title='Demo Experiment', metadata={})
session.add(n)
session.commit()
exp = Experiment(node_id=n.id, title='Demo Experiment', description='A demo')
session.add(exp)
session.commit()

print('seed complete', p.id, n.id, exp.id)
