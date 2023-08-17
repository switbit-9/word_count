import asyncio
from collections import Counter
import aiofiles

class ProcessFiles:

    def __init__(self, path):
        self.path = path
        self.file_content = ''

    async def read_file(self):
        async with aiofiles.open(self.path, mode='r', encoding='utf-8') as f:
            self.file_content = await f.read()
    async def process_file(self):
        await self.read_file()
        words = {}
        for item in self.file_content.split():
            if item in words.keys():
                words[item] += 1
            else:
                words[item] = 1
        return words











