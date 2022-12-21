import time

from common.DBAdapter import DBSession
from entity.Entity import User


class EntityHome(DBSession):

    def __init__(self, model):
        DBSession.__init__(self, model)

    def query_by_cond(self, cond):
        try:
            session = self.session
            query = session.query(session.module).filter(cond)

            results = query.all()
            return results
        except Exception as e:
            print(e)
        finally:
            self.close()

    def query_one(self, cond):
        try:
            session = self.session
            result = session.query(session.module).filter(cond).one()
            return result
        except Exception as e:
            print(e)
        finally:
            self.close()

    def query(self):
        try:
            session = self.session
            query = session.query(session.module)

            results = query.all()
            return results
        except Exception as e:
            print(e)
        finally:
            self.close()

    def get(self, id):
        try:
            session = self.session
            query = session.query(session.module)

            results = query.get(id)
            return results
        except Exception as e:
            print(e)
        finally:
            self.close()

    def add(self, instance):
        id = -1
        session = self.session
        try:
            session.add(instance)
            session.flush()
            if hasattr(instance, 'id'):
                id = instance.id
            session.commit()
        except Exception as e:
            session.rollback()
            print(e)
        finally:
            self.close()
        return id

    def update(self, instance):
        id = -1
        session = self.session
        try:
            instance.utime = time.strftime(
                "%Y-%m-%d %H:%M:%S", time.localtime())
            session.merge(instance)
            session.commit()
            if hasattr(instance, 'id'):
                id = instance.id
        except Exception as e:
            session.rollback()
            print(e)
        finally:
            self.close()
        return id

    def empty(self):
        id = -1
        session = self.session
        try:
            query = session.query(session.module)
            query.delete()
            session.commit()
            id = 0
        except Exception as e:
            session.rollback()
            print(e)
        finally:
            self.close()
        return id

    def delete(self, id):
        rtn = -1
        session = self.session
        try:
            q = session.query(session.module).filter_by(id=id)
            rtn = q.delete()
            session.commit()
        except Exception as e:
            session.rollback()
            print(e)
        finally:
            self.close()
        return rtn


class UserEntityHome(EntityHome):
    def __init__(self):
        EntityHome.__init__(self, User)

    def get_by_name(self, name: str):
        e = self.query_one(User.name == name)
        return e

    # Do not delete user
    def delete(self, id):
        e = self.get(id)
        e.deleted = 1
        self.update(e)


'''
# Testing codes:
home = UserEntityHome()
user = User()
user.id = 1
user.name = "admin"
user.password = "$2y$12$9X/Ts9dpj/TGuDAOl75KKeSdW1AFg6YcEyisGQuz.37q3gv9h1vdS"
home.add(user)

home = EntityHome(Memo)
home.empty()
memo = Memo()
memo.id = 1
memo.title = "first memo"
memo.uid = user.id;
home.add(memo)
memo = Memo()
memo.id = 2
memo.title = "first memo2"
memo.uid = user.id;
home.add(memo)

l = home.query()
for i in l:
    print(i.id, '    ', i.title, i.uid)

memo = Memo()
memo.id = 1
memo.title = "second memo"
home.update(memo)

l = home.query()
for i in l:
    print(i.id, '    ', i.title, i.uid)

home.delete(1)

'''

# home = EntityHome(User)
# home.empty()
# user = User()
# user.id = 1
# user.name = "cxb"
# home.add(user)
# u = home.query()
# for user in u:
#     print(user.id, '    ', user.name)
# user.id = 1
# user.name = "lsz"
# home.update(user)
# u = home.query()
# for user in u:
#     print(user.id, '    ', user.name)
# home.delete(1)
