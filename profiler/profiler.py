"""

Profiler — сервис для создания резюме и портфолио в лаконичном стиле

"""

# ————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————

import reflex as rx

import profiler.states.page
# ————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————

from .pages import index, mypages, edit, page
from .states import index, mypages, edit, page

# ————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————

app = rx.App(
    stylesheets=[
        "/fonts/SFProText.css",
        "/fonts/SFMono.css",
        "/fonts/SFCompact.css",
        "/fonts/SFProDisplay.css",
        "/fonts/SFProRounded.css",
    ],
)

app.add_page(
    profiler.pages.page.index,
    route="/p/[url]",
    on_load=profiler.states.page.State.checkPageUrl,
)