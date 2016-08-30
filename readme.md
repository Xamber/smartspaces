Тестовое задание. (:snale: Python 3.5.1)

Чтобы запустить:

`python server.py`

**Коментарии:**

- т.к. одно из требований - большое количество пользователей, решил сделать на асинхронном фреймворке
- в процессе подумал о том, что было бы логично вынести переменные количества пользователей и суммы в Redis,
но потом решил, что перебор. Но при надобности, добавить это легко: 

    `app['database'] = await aioredis.create_redis(('localhost', 6379), db=0, encoding='utf-8')`
    
    `db = self.request.app['database']`
    
    `await db.get('online')`
    
    `await db.set('online')`
    
- Можно запустить через Docker - `docker-compose up`




