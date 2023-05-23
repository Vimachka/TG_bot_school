import aiomysql
import asyncio
import pymysql
from config.config import Config, load_config

config: Config = load_config('.env')
loop = asyncio.get_event_loop()


async def add_user(id_user: int, *data: dict):
    print(data)
    try:
        con = await aiomysql.connect(user=config.database.user,
                                     password=config.database.password, db=config.database.database, loop=loop)
        async with con.cursor() as cur:
            query = f"INSERT INTO users VALUES(%s, %s," \
                    f"%s, %s, null)"
            await cur.execute(query, (id_user, *data[0].values()))
            await con.commit()
        con.close()
    except Exception as ex:
        print(ex)


async def update_user_bd(id_user: int, *data: dict):
    try:
        con = await aiomysql.connect(user=config.database.user,
                                     password=config.database.password, db=config.database.database, loop=loop)
        async with con.cursor() as cur:
            query = 'UPDATE users SET class=%s, category=%s WHERE id_user=%s;'
            await cur.execute(query, (data[0]['clas'], data[0]['category'], id_user))
            await con.commit()
        con.close()
    except Exception as ex:
        print(ex)


async def is_user(id_user: int) -> bool:
    try:
        con = await aiomysql.connect(user=config.database.user,
                                     password=config.database.password, db=config.database.database, loop=loop)
        print(id_user)
        async with con.cursor() as cur:
            query = 'SELECT COUNT(*) FROM users WHERE id_user=%s;'
            await cur.execute(query, (id_user, ))
            result = await cur.fetchone()
        print(result[0])
        return True if int(result[0]) else False
    except Exception as ex:
        print(ex)
        return False


async def add_solution(*data: dict):
    try:
        con = await aiomysql.connect(user=config.database.user,
                                     password=config.database.password, db=config.database.database, loop=loop)
        async with con.cursor() as cur:
            query = '''
            INSERT INTO quests(text, solution, class, category)
            VALUES (%s, %s, %s, %s);
            '''
            await cur.execute(query, (data[0]['text'], data[0]['solution'], data[0]['clas'], data[0]['category']))
            await con.commit()
        con.close()
    except Exception as ex:
        print(ex)


async def add_rating(id_user: int):
    try:
        con = await aiomysql.connect(user=config.database.user,
                                     password=config.database.password, db=config.database.database, loop=loop)
        async with con.cursor() as cursor:
            query = 'INSERT INTO rating(count, id_user)' \
                    'VALUES (%s, %s);'
            await cursor.execute(query, (0, id_user))
            await con.commit()
        con.close()
    except Exception as ex:
        print(ex)


async def id_solution(id_user: int):
    try:
        con = await aiomysql.connect(user=config.database.user,
                                     password=config.database.password, db=config.database.database, loop=loop)
        async with con.cursor() as cursor:
            query = '''
                SELECT q.id, q.text FROM quests q
                WHERE class = (SELECT class FROM users WHERE id_user=%s)
                AND category = (SELECT category FROM users WHERE id_user=%s)
                AND q.id NOT IN (SELECT id_quest FROM test WHERE id_user=%s AND is_suc=True)
                ORDER BY RAND()
                LIMIT 1;
            '''
            await cursor.execute(query, (id_user, id_user, id_user))
            return await cursor.fetchone()
    except Exception as ex:
        print(ex)


async def update_id_solution(id_user: int, id_solution: int) -> None:
    try:
        con = await aiomysql.connect(user=config.database.user,
                                     password=config.database.password, db=config.database.database, loop=loop)
        async with con.cursor() as cur:
            query = '''
                UPDATE users SET id_solution=%s
                WHERE id_user=%s;
            '''
            await cur.execute(query, (id_solution, id_user))
            await con.commit()
        con.close()
    except Exception as ex:
        print(ex)


async def is_test(id_user: int) -> bool:
    try:
        con = await aiomysql.connect(user=config.database.user,
                                     password=config.database.password, db=config.database.database, loop=loop)
        async with con.cursor() as cur:
            query = '''
                SELECT count(*) FROM test WHERE id_user=%s AND id_quest=(SELECT id_solution FROM users WHERE id_user=%s);
            '''
            await cur.execute(query, (id_user, id_user))
            return (await cur.fetchone())[0]
    except Exception as ex:
        print(ex)


async def add_test(id_user: int, id_solution: int, answer: str, is_suc: bool):
    try:
        con = await aiomysql.connect(user=config.database.user,
                                     password=config.database.password, db=config.database.database, loop=loop)
        async with con.cursor() as cur:
            query = '''
                INSERT INTO test (id_user, id_quest, answer, is_suc, attempt)
                VALUES (%s, %s, %s, %s, 1);
            '''
            await cur.execute(query, (id_user, id_solution, answer, is_suc))
            await con.commit()
            print('hi')
        con.close()
    except Exception as ex:
        print(ex)


async def answer_test(id_solution: int) -> str:
    try:
        con = await aiomysql.connect(user=config.database.user,
                                     password=config.database.password, db=config.database.database, loop=loop)
        async with con.cursor() as cur:
            query = '''
            SELECT solution FROM quests WHERE id=%s;
            '''
            await cur.execute(query, (id_solution,))
            return (await cur.fetchone())[0]
    except Exception as ex:
        print(ex)


async def update_test(id_user: int, id_solution: int, success: bool, answer: str):
    try:
        con = await aiomysql.connect(user=config.database.user,
                                     password=config.database.password, db=config.database.database, loop=loop)
        async with con.cursor() as cur:
            query = '''
                UPDATE test SET
                is_suc=%s, answer=%s, attempt=attempt + 1
                WHERE id_user=%s AND id_quest=%s;
            '''
            await cur.execute(query, (success, answer, id_user, id_solution))
            await con.commit()
        con.close()
    except Exception as ex:
        print(ex)


async def return_attempts(id_user: int, id_solution: int):
    try:
        con = await aiomysql.connect(user=config.database.user,
                                     password=config.database.password, db=config.database.database, loop=loop)
        async with con.cursor() as cur:
            query = '''
                SELECT attempt FROM test WHERE id_user=%s AND id_quest=%s;
            '''
            await cur.execute(query, (id_user, id_solution))
            return (await cur.fetchone())[0]
    except Exception as ex:
        print(ex)


async def update_rating(id_user: int, score: int):
    try:
        con = await aiomysql.connect(user=config.database.user,
                                     password=config.database.password, db=config.database.database, loop=loop)
        async with con.cursor() as cur:
            query = '''
                UPDATE rating SET count=count + %s
                WHERE id_user=%s;
            '''
            await cur.execute(query, (score, id_user))
            await con.commit()
        con.close()
    except Exception as ex:
        print(ex)


async def return_rating():
    try:
        con = await aiomysql.connect(user=config.database.user,
                                     password=config.database.password, db=config.database.database, loop=loop)
        async with con.cursor() as cur:
            query = '''
                SELECT r.count, u.name FROM rating r
                INNER JOIN users u ON u.id_user = r.id_user
                ORDER BY count DESC
                LIMIT 10;
            '''
            await cur.execute(query)
            return await cur.fetchall()
    except Exception as ex:
        print(ex)