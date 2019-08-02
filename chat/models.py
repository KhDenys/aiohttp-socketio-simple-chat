from main.settings import MESSAGE_COLLECTION


class Message:
    def __init__(self, db):
        self.collection = db[MESSAGE_COLLECTION]

    async def save(self, **kw):
        result = await self.collection.insert_one({'username': kw['username'], 'msg': kw['msg'], 'time': kw['time']})
        return result

    async def get_messages(self):
        messages = self.collection.find().sort([('time', 1)])
        return await messages.to_list(length=None)
