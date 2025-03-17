
# ——————————————————————————————————————————————————————————————————————————————————————————————————————————————————————

import reflex as rx
from rxconfig import config

# ——————————————————————————————————————————————————————————————————————————————————————————————————————————————————————

import profiler.database as database
from profiler.states.localStorage import Storage as LS

# ——————————————————————————————————————————————————————————————————————————————————————————————————————————————————————

class State(LS):
    tCountPages = 0
    tPages: list[list[list[str]]]

    async def onStart(self):
        self.tCountPages = await database.getDataMultiCount('pages', 'idAuthor', f"'{self.USER[0]}'")
        if self.tCountPages > 0:
            pages = await database.getDataMulti('pages', 'idAuthor', f"'{self.USER[0]}'")
            massive = []
            line = []
            count = 0
            for NAME in pages:
                if count > 2:
                    massive.append(line)
                    count = 0
                    line = []
                    count = count + 1
                    MASSIVE_ITEM = [NAME[0], NAME[1], NAME[2], NAME[3], NAME[4], NAME[5], NAME[6], NAME[7], NAME[8], NAME[9], NAME[10], NAME[11], NAME[12], NAME[13], NAME[14], NAME[15], NAME[16]]
                    line.append(MASSIVE_ITEM)
                else:
                    count = count + 1
                    MASSIVE_ITEM = [NAME[0], NAME[1], NAME[2], NAME[3], NAME[4], NAME[5], NAME[6], NAME[7], NAME[8], NAME[9], NAME[10], NAME[11], NAME[12], NAME[13], NAME[14], NAME[15], NAME[16]]
                    line.append(MASSIVE_ITEM)
            massive.append(line)
            self.tPages = massive