from .app import Base
from sqlalchemy.orm import relationship
from sqlalchemy import *
from datetime import date
from flask_login import UserMixin
from .app import login, session

# тянем таблицы из базы и делаем по ним модели
class User(Base, UserMixin):
    __table__ = Base.metadata.tables['user']
    group = relationship("Group", backref="user")
    permission_group = relationship("PermissionGroup", backref="user")
    def __str__(self):
        return self.first_name+' '+self.last_name

# функция логина
@login.user_loader
def load_user(id):
    return session.query(User).get(int(id))

class Group(Base):
    __table__ = Base.metadata.tables['group']
    reports = relationship('Report', backref='group')
    def __str__(self):
        return self.name

class PermissionGroup(Base):
    __table__ = Base.metadata.tables['permission_group']
    def __str__(self):
        return self.name

# модель для замечаний
class Report(Base):
    __tablename__ = "report"
    __table_args__ = {'extend_existing': True}
    id = Column(Integer, primary_key=True, autoincrement=True)
    date = Column(Date, default=date.today())
    comment = Column(Text)
    status = Column(String(30), CheckConstraint("status IN ('Выполнено', 'Подтверждение', 'Исправить')"))
    pages = Column(String(20))
    id_group = Column(Integer, ForeignKey('group.id'))
    id_controller = Column(Integer, ForeignKey('user.id'))
    id_teacher = Column(Integer, ForeignKey('user.id'))
    controller = relationship('User', foreign_keys=[id_controller])
    teacher = relationship('User', foreign_keys=[id_teacher])
    def __str__(self):
        return self.status