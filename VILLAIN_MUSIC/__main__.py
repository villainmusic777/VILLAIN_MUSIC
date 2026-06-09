import asyncio
from VILLAIN_MUSIC import app
from VILLAIN_MUSIC.misc import sudo

async def init():
    await app.start()
    await sudo()
    await asyncio.Event().wait()

asyncio.get_event_loop().run_until_complete(init())
