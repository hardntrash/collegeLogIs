from .app import Base
from sqlalchemy.orm import relationship
from sqlalchemy import *
from datetime import date
from flask_login import UserMixin
from .app import login, session


# тянем таблицы из базы и делаем по ним модели
class User(Base, UserMixin):
    __table__ = Base.metadata.tables['g4er6y_users']
    users_group_map = relationship("UserUsergroupMap", backref="user")

    @staticmethod
    def get_group_parent_id(usr):
        group_id = session.query(UserUsergroupMap).filter_by(user_id=usr.id).first().group_id
        parent_id = session.query(UserGroup).filter_by(id=group_id).first().parent_id
        return parent_id
    def __str__(self):
        return self.name

# функция логина
@login.user_loader
def load_user(id):
    return session.query(User).get(int(id))

class UserGroup(Base):
    __table__ = Base.metadata.tables['g4er6y_usergroups']
    users_group_map = relationship("UserUsergroupMap", backref="user_group")
    def __str__(self):
        return self.title

class UserUsergroupMap(Base):
    __table__ = Base.metadata.tables['g4er6y_user_usergroup_map']
    __table_args__ = {'autoload': True}
    def __str__(self):
        return str(self.user_id) + ' ' +str(self.group_id)

# # модель для замечаний
class Report(Base):
    __tablename__ = "report"
    __table_args__ = {'extend_existing': True}
    id = Column(Integer, primary_key=True, autoincrement=True)
    date = Column(Date, default=date.today())
    comment = Column(Text)
    status = Column(String(30), default="Исправить")
    pages = Column(String(20))
    group = Column(String(30))
    id_controller = Column(Integer, ForeignKey('g4er6y_users.id'))
    id_teacher = Column(Integer, ForeignKey('g4er6y_users.id'))
    controller = relationship(User, foreign_keys=[id_controller])
    teacher = relationship(User, foreign_keys=[id_teacher])
    def __str__(self):
        return self.status