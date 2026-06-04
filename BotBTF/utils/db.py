import aiosqlite
import os

DB_PATH = 'database/btf_bot.db'

async def init_db():
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute('''
            CREATE TABLE IF NOT EXISTS users (
                user_id INTEGER,
                guild_id INTEGER,
                xp INTEGER DEFAULT 0,
                level INTEGER DEFAULT 1,
                PRIMARY KEY (user_id, guild_id)
            )
        ''')
        await db.commit()

async def get_user_data(user_id, guild_id):
    async with aiosqlite.connect(DB_PATH) as db:
        async with db.execute('SELECT xp, level FROM users WHERE user_id = ? AND guild_id = ?', (user_id, guild_id)) as cursor:
            return await cursor.fetchone()

async def update_user_xp(user_id, guild_id, xp_to_add):
    async with aiosqlite.connect(DB_PATH) as db:
        row = await get_user_data(user_id, guild_id)
        if row:
            current_xp, current_level = row
            new_xp = current_xp + xp_to_add
            # Simples lógica de level: level = sqrt(xp) / 5 (ajustável)
            new_level = int((new_xp ** 0.5) / 5) + 1
            
            await db.execute('UPDATE users SET xp = ?, level = ? WHERE user_id = ? AND guild_id = ?', 
                           (new_xp, new_level, user_id, guild_id))
            leveled_up = new_level > current_level
        else:
            new_xp = xp_to_add
            new_level = 1
            await db.execute('INSERT INTO users (user_id, guild_id, xp, level) VALUES (?, ?, ?, ?)', 
                           (user_id, guild_id, new_xp, new_level))
            leveled_up = False
        
        await db.commit()
        return leveled_up, new_level

async def get_leaderboard(guild_id, limit=10):
    async with aiosqlite.connect(DB_PATH) as db:
        async with db.execute('SELECT user_id, xp, level FROM users WHERE guild_id = ? ORDER BY xp DESC LIMIT ?', 
                           (guild_id, limit)) as cursor:
            return await cursor.fetchall()
