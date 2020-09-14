from db.mongo_db import client
from bson.objectid import ObjectId


class MongoNewsDao:
    # 往MongoDB中添加新闻正文记录
    def insert(self, title, content):
        try:
            client.vega.news.insert_one({'title': title, 'content': content})
        except Exception as e:
            print(e)

    # 根据新闻标题查找正文ID
    def search_id(self, title):
        try:
            news = client.vega.news.find_one({'title': title})
            return str(news['_id'])
        except Exception as e:
            print(e)

    def update(self, id, title, content):
        try:
            client.vega.news.update_one({'_id': ObjectId(id)},
                                        {'$set': {'title': title, 'content': content}}
                                        )
        except Exception as e:
            print(e)

    def search_content_by_id(self, id):
        try:
            news = client.vega.news.find_one({'_id': ObjectId(id)})
            return news['content']
        except Exception as e:
            print(e)

    def delete_by_id(self, id):
        try:
            client.vega.news.delete_one({'_id': ObjectId(id)})
        except Exception as e:
            print(e)

# if __name__ == '__main__':
#     k = MongoNewsDao()
#     k.update('5f2fb736b9b218f753e95979', 'TikTok新闻2', '123')
