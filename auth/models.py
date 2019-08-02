from bson.objectid import ObjectId
from main.settings import USER_COLLECTION


class User:
    def __init__(self, db, data):
        self.db = db
        self.collection = self.db[USER_COLLECTION]
        self.login = data.get('login')
        self.password = data.get('password')
        self.id = data.get('id')

    async def check_user(self):
        return await self.collection.find_one({'login': self.login, 'password': self.password})

    async def get_login(self):
        user = await self.collection.find_one({'_id': ObjectId(self.id)})
        return user.get('login')

    async def create_user(self):
        user = await self.check_user()
        if not user:
            result = await self.collection.insert_one({'login': self.login, 'password': self.password})
        else:
            result = user
        return result
