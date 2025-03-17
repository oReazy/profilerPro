
# ——————————————————————————————————————————————————————————————————————————————————————————————————————————————————————

import reflex as rx
import json, ast, datetime, time

from rxconfig import config

# ——————————————————————————————————————————————————————————————————————————————————————————————————————————————————————

import profiler.database as database
from profiler.states.localStorage import Storage as LS

# ——————————————————————————————————————————————————————————————————————————————————————————————————————————————————————

import profiler.components.auth as auth
import profiler.components.registration as registration

# ——————————————————————————————————————————————————————————————————————————————————————————————————————————————————————

class header(LS):
    tLogo = '/logo_alt.png'

    def onMouse(self):
        self.tLogo = '/logo.png'

    def unMouse(self):
        self.tLogo = '/logo_alt.png'

# ——————————————————————————————————————————————————————————————————————————————————————————————————————————————————————

def index():
    return rx.flex(
        rx.image(header.tLogo, on_mouse_enter=header.onMouse, on_mouse_leave=header.unMouse, width='35px', on_click=rx.redirect('/')),
        rx.cond(
            LS.HASH == '0',
            rx.flex(
                auth.index('2'),
                registration.index('2'),
                spacing='2',
                align='center',
            ),
            rx.flex(
                rx.button('Мои страницы', font_family='SFProDisplayBold', on_click=rx.redirect('/mypages')),
                rx.button("Выйти", color_scheme='tomato', on_click=[rx.clear_local_storage(), rx.redirect('/')], font_family='SFProDisplayBold'),
                spacing='2',
                align='center',
            ),
        ),
        justify='between',
        align='center',
        spacing='2',
    )