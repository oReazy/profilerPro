"""

[ PAGES ]

Главная страница проекта

"""

# ——————————————————————————————————————————————————————————————————————————————————————————————————————————————————————

import reflex as rx
import json, ast, datetime, time

from rxconfig import config

# ——————————————————————————————————————————————————————————————————————————————————————————————————————————————————————

import profiler.database as database
from profiler.states.localStorage import Storage as LS

import profiler.components.header as header
import profiler.components.newPortfolioItem as newPortfolioItem
import profiler.components.newLinkItem as newLinkItem
import profiler.components.editName as editName
from profiler.states.edit import State as State

# ——————————————————————————————————————————————————————————————————————————————————————————————————————————————————————

style = {"text-decoration": "none !important",  # Убираем подчёркивание
         "color": "inherit !important",  # Цвет наследуется от родителя
         "cursor": "hover",  # Убираем указатель на ссылке
        }
hover = {"color": "inherit !important",  # Цвет не меняется при наведении
        "text-decoration": "none !important",  # Подчёркивание не появляется
        "background-color": "transparent !important",  # Чтобы исключить изменения фона
        }
style2 = {
            "object-fit": "cover",  # Покрытие всей области
            "object-position": "center",  # Центровка изображения
         }

# ——————————————————————————————————————————————————————————————————————————————————————————————————————————————————————

@rx.page(route="/page/edit/[id]", title="«Profiler» — Редактирование страницы", on_load=[LS.onLoad, State.checkPage])
def index():
    return rx.container(
        rx.cond(
            rx.State.is_hydrated,
            rx.flex(
                header.index(),
                rx.cond(
                    State.tErrorVisible == False,
                    rx.flex(
                        rx.flex(
                            # rx.image(rx.get_upload_url(f'{State.tImages[1]}')),
                            rx.cond(
                                (State.tImages[1] == '/images/pages/wallpaper.png') | (State.tImages[1] == '/images/pages/wallpaper_alt.png'),
                                rx.upload(rx.center(rx.image(State.tImages[1], border_radius='12px', on_mouse_enter=State.onMouseWallpaper, on_mouse_leave=State.unMouseWallpaper)), id="upload_wallpaper", max_files=1, max_size=10000000, accept={"image/png": [".png"], "image/jpeg": [".jpg", ".jpeg"]}, on_drop=State.handle_upload_wallpaper(rx.upload_files(upload_id="upload_wallpaper")), padding='-40px', margin_left='117px', margin_right='117px', border='0px'),
                                rx.upload(rx.center(rx.image(rx.get_upload_url(f'{State.tImages[1]}'), style=LS.style2, width='900px', height='160px', border_radius='12px', on_mouse_enter=State.onMouseWallpaper, on_mouse_leave=State.unMouseWallpaper)), id="upload_wallpaper", max_files=1, max_size=10000000, accept={"image/png": [".png"], "image/jpeg": [".jpg", ".jpeg"]}, on_drop=State.handle_upload_wallpaper(rx.upload_files(upload_id="upload_wallpaper")), border='0px', padding='-40px', margin_left='117px', margin_right='117px'),
                            ),
                            # margin_top='-100px', margin_left='-721px'
                            rx.cond(
                                (State.tImages[0] == '/images/pages/avatar.png') | (State.tImages[0] == '/images/pages/avatar_alt.png'),
                                rx.upload(rx.center(rx.image(State.tImages[0], width='140px', height='140px', border="4px solid #FFFFFF", border_radius='12px', on_mouse_enter=State.onMouseAvatar, on_mouse_leave=State.unMouseAvatar)), id="upload_wallpaper", max_files=1, max_size=10000000, accept={"image/png": [".png"], "image/jpeg": [".jpg", ".jpeg"]}, on_drop=State.handle_upload_avatar2(rx.upload_files(upload_id="upload_avatar")), padding='-40px', margin_left='137px', margin_right='857px', margin_top='-100px' , border='0px'),
                                rx.upload(rx.center(rx.image(rx.get_upload_url(f'{State.tImages[0]}'), style=LS.style2, width='140px', height='140px', border="4px solid #FFFFFF", border_radius='12px', on_mouse_enter=State.onMouseAvatar, on_mouse_leave=State.unMouseAvatar)), id="upload_wallpaper", max_files=1, max_size=10000000, accept={"image/png": [".png"], "image/jpeg": [".jpg", ".jpeg"]}, on_drop=State.handle_upload_avatar2(rx.upload_files(upload_id="upload_avatar")), padding='-40px', margin_left='137px', margin_right='857px', margin_top='-100px' , border='0px'),
                            ),
                            rx.tabs.root(
                                rx.tabs.list(
                                    rx.tabs.trigger("Главная", value="tab1", font_family='SFProDisplayBold'),
                                    rx.tabs.trigger("Настройки", value="tab2", font_family='SFProDisplayBold'),
                                    margin_top='-52px',
                                    margin_left='278px',
                                    width='740px'
                                ),
                                rx.tabs.content(
                                    rx.flex(
                                        rx.card(
                                            rx.flex(
                                                rx.flex(
                                                    rx.text('Имя', font_family='SFProDisplayBold', color_scheme='gray', size='2'),
                                                    rx.input(
                                                        rx.input.slot(
                                                            rx.icon('user', size=17, color=rx.color('gray', 9))
                                                        ),
                                                        value=State.tName,
                                                        on_change=[State.set_tName],
                                                        font_family='SFProDisplayBold',
                                                        placeholder='Введите имя',
                                                    ),
                                                    direction='column',
                                                    spacing='1',
                                                ),
                                                rx.flex(
                                                    rx.text('Фамилия', font_family='SFProDisplayBold', color_scheme='gray', size='2'),
                                                    rx.input(
                                                        rx.input.slot(
                                                            rx.icon('user', size=17, color=rx.color('gray', 9))
                                                        ),
                                                        value=State.tSurname,
                                                        on_change=[State.set_tSurname],
                                                        font_family='SFProDisplayBold',
                                                        placeholder='Введите фамилию',
                                                    ),
                                                    direction='column',
                                                    spacing='1',
                                                ),
                                                direction='row',
                                                spacing='2',
                                            ),
                                            rx.flex(
                                                rx.text('О себе', font_family='SFProDisplayBold', color_scheme='gray', size='2'),
                                                rx.text_area(
                                                    value=State.tAbout,
                                                    on_change=[State.set_tAbout],
                                                    font_family='SFProDisplayBold',
                                                    placeholder='Расскажите о себе',
                                                    height='127px'
                                                ),
                                                direction='column',
                                                margin_top='12px',
                                                spacing='1',
                                            ),
                                            rx.flex(
                                                rx.text('Ссылка', font_family='SFProDisplayBold', color_scheme='gray', size='2'),
                                                rx.flex(
                                                    rx.input(
                                                        rx.input.slot(
                                                            rx.text('https//profiler.io/p/'),
                                                            margin_right='-8px',
                                                        ),
                                                        value=State.tUrl,
                                                        on_change=[State.set_tUrl],
                                                        font_family='SFProDisplayBold',
                                                        width='100%'
                                                    ),
                                                    rx.button(rx.icon('copy', size=20), on_click=[rx.set_clipboard(f"https//profiler.io/p/{State.tUrl}"), rx.toast.info("Ссылка скопирована в буфер обмена")]),
                                                    direction='row',
                                                    spacing='2'
                                                ),
                                                padding_top='8px',
                                                direction='column',
                                                spacing='1',
                                            ),
                                            rx.button('Сохранить', font_family='SFProDisplayBold', on_click=State.save, margin_top='8px')
                                        ),
                                        rx.card(
                                            rx.flex(
                                                rx.text('ВИДИМОСТЬ БЛОКОВ', font_family='SFMonoBold', size='2', color_scheme='gray', margin_bottom='8px'),
                                                rx.flex(
                                                    rx.flex(
                                                        rx.image('/images/pages/info.png', width='26px'),
                                                        rx.text('Показывать блок "О себе"', font_family='SFProDisplayMedium', size='2'),
                                                        direction='row',
                                                        spacing='2',
                                                        align='center',
                                                    ),
                                                    rx.switch(default_checked=State.tVision1, on_change=State.set_tVision1),
                                                    align='center',
                                                    direction='row',
                                                    justify='between'
                                                ),
                                                rx.divider(),
                                                rx.flex(
                                                    rx.flex(
                                                        rx.image('/images/pages/portfolio.png', width='26px'),
                                                        rx.text('Показывать блок "Портфолио"', font_family='SFProDisplayMedium', size='2'),
                                                        direction='row',
                                                        spacing='2',
                                                        align='center',
                                                    ),
                                                    rx.switch(default_checked=State.tVision2, on_change=State.set_tVision2),
                                                    align='center',
                                                    direction='row',
                                                    spacing='2',
                                                    justify='between'
                                                ),
                                                rx.divider(),
                                                rx.flex(
                                                    rx.flex(
                                                        rx.image('/images/pages/companys_alt.png', width='26px'),
                                                        rx.text('Показывать блок "Опыт работы"', font_family='SFProDisplayMedium', size='2', color_scheme='gray'),
                                                        direction='row',
                                                        spacing='2',
                                                        align='center',
                                                    ),
                                                    rx.switch(default_checked=State.tVision3, on_change=State.set_tVision3, disabled=True),
                                                    align='center',
                                                    direction='row',
                                                    spacing='2',
                                                    justify='between'
                                                ),
                                                rx.divider(),
                                                rx.flex(
                                                    rx.flex(
                                                        rx.image('/images/pages/links.png', width='26px'),
                                                        rx.text('Показывать блок "Ссылки"', font_family='SFProDisplayMedium', size='2'),
                                                        direction='row',
                                                        spacing='2',
                                                        align='center',
                                                    ),
                                                    rx.switch(default_checked=State.tVision4, on_change=State.set_tVision4),
                                                    align='center',
                                                    direction='row',
                                                    spacing='2',
                                                    justify='between'
                                                ),
                                                rx.divider(),
                                                rx.flex(
                                                    rx.flex(
                                                        rx.image('/images/pages/menu.png', width='26px'),
                                                        rx.text('Показывать блок "Меню"', font_family='SFProDisplayMedium', size='2'),
                                                        direction='row',
                                                        spacing='2',
                                                        align='center',
                                                    ),
                                                    rx.switch(default_checked=State.tVision5, on_change=State.set_tVision5),
                                                    align='center',
                                                    direction='row',
                                                    spacing='2',
                                                    justify='between'
                                                ),
                                                rx.divider(),
                                                rx.flex(
                                                    rx.text('Видимость страницы', font_family='SFProDisplayMedium', size='2'),
                                                    rx.select(
                                                        ["Открыта", "Закрыта"],
                                                        default_value=State.tPrivate,
                                                        on_change=State.set_tPrivate
                                                    ),
                                                    align='center',
                                                    direction='row',
                                                    spacing='2',
                                                    justify='between'
                                                ),
                                                direction='column',
                                                spacing='2'
                                            ),
                                            rx.flex(
                                                rx.button('Сохранить', font_family='SFProDisplayBold', on_click=State.save, margin_top='8px'),
                                                direction='row',
                                                justify='end'
                                            ),
                                            width='500px'
                                        ),
                                        spacing='2',
                                        align='start',
                                        width='900px',
                                        margin_top='12px'
                                    ),
                                    rx.flex(
                                        rx.card(
                                            rx.flex(
                                                rx.flex(
                                                    rx.flex(
                                                        rx.cond(
                                                            State.tVision2,
                                                            rx.image('/images/pages/portfolio.png', width='26px'),
                                                            rx.image('/images/pages/portfolio_alt.png', width='26px'),
                                                        ),
                                                        rx.cond(
                                                            State.tVision2,
                                                            rx.text('Портфолио', font_family='SFProDisplayBold', size='2'),
                                                            rx.text('Портфолио (скрыто)', font_family='SFProDisplayBold', size='2', color_scheme='gray'),
                                                        ),
                                                        align='center',
                                                        spacing='2',
                                                        direction='row'
                                                    ),
                                                    rx.flex(
                                                        rx.cond(
                                                            State.tVision2,
                                                            rx.button('Изменить вид', font_family='SFProDisplayBold', size='1'),
                                                            rx.button('Изменить вид', font_family='SFProDisplayBold', size='1', disabled=True),
                                                        ),
                                                        rx.cond(
                                                            State.tVision2,
                                                            newPortfolioItem.index(),
                                                            rx.button('Добавить работу', font_family='SFProDisplayBold', size='1', disabled=True),
                                                        ),
                                                        direction='row',
                                                        align='center',
                                                        spacing='2'
                                                    ),
                                                    direction='row',
                                                    spacing='2',
                                                    justify='between',
                                                    align='center'
                                                ),
                                                rx.cond(
                                                    LS.tPortfolioCount != 0,
                                                    rx.cond(
                                                        State.tVision2,
                                                        rx.foreach(
                                                            LS.tPortfolio, lambda item:
                                                            rx.flex(
                                                                rx.divider(),
                                                                rx.flex(
                                                                    newPortfolioItem.openItem(item),
                                                                    rx.flex(
                                                                        rx.button(rx.icon('trash-2', size=18), color_scheme='tomato', size='1', on_click=newPortfolioItem.newPortfolioItem.delete(item)),
                                                                        direction='row',
                                                                        spacing='2'
                                                                    ),
                                                                    spacing='2',
                                                                    direction='row',
                                                                    align='center',
                                                                    justify='between'
                                                                ),
                                                                direction='column',
                                                                spacing='2'
                                                            )
                                                        ),
                                                    ),
                                                ),
                                                width='100%',
                                                direction='column',
                                                spacing='2',
                                            ),
                                            width='100%'
                                        ),
                                        spacing='2',
                                        align='start',
                                        width='900px',
                                        margin_top='8px'
                                    ),
                                    rx.flex(
                                        rx.card(
                                            rx.flex(
                                                rx.flex(
                                                    rx.flex(
                                                        rx.cond(
                                                            State.tVision4,
                                                            rx.image('/images/pages/links.png', width='26px'),
                                                            rx.image('/images/pages/links_alt.png', width='26px'),
                                                        ),
                                                        rx.cond(
                                                            State.tVision4,
                                                            rx.text('Ссылки', font_family='SFProDisplayBold', size='2'),
                                                            rx.text('Ссылки (скрыто)', font_family='SFProDisplayBold', size='2', color_scheme='gray'),
                                                        ),
                                                        align='center',
                                                        spacing='2',
                                                        direction='row'
                                                    ),
                                                    rx.flex(
                                                        rx.cond(
                                                            State.tVision4,
                                                            newLinkItem.index(),
                                                            rx.button('Добавить ссылку', font_family='SFProDisplayBold', size='1', disabled=True),
                                                        ),
                                                        direction='row',
                                                        align='center',
                                                        spacing='2'
                                                    ),
                                                    direction='row',
                                                    spacing='2',
                                                    justify='between',
                                                    align='center'
                                                ),
                                                rx.cond(
                                                    LS.tLinksCount != 0,
                                                    rx.cond(
                                                        State.tVision4,
                                                        rx.foreach(
                                                            LS.tLinks, lambda item:
                                                            rx.flex(
                                                                rx.divider(),
                                                                rx.flex(
                                                                    newLinkItem.openItem(item),
                                                                    rx.flex(
                                                                        rx.button(rx.icon('trash-2', size=18), color_scheme='tomato', size='1', on_click=newLinkItem.newLinkItem.delete(item)),
                                                                        direction='row',
                                                                        spacing='2'
                                                                    ),
                                                                    spacing='2',
                                                                    direction='row',
                                                                    align='center',
                                                                    justify='between'
                                                                ),
                                                                direction='column',
                                                                spacing='2'
                                                            )
                                                        ),
                                                    ),
                                                ),
                                                width='100%',
                                                direction='column',
                                                spacing='2',
                                            ),
                                            width='100%'
                                        ),
                                        spacing='2',
                                        align='start',
                                        width='900px',
                                        margin_top='8px'
                                    ),
                                    value="tab1",
                                    margin_left='117px',
                                ),

                                rx.tabs.content(
                                    rx.flex(
                                        rx.card(
                                            rx.flex(
                                                rx.text('ОСНОВНЫЕ НАСТРОЙКИ', font_family='SFMonoBold', size='2', color_scheme='gray', margin_bottom='8px'),
                                                rx.flex(
                                                    rx.text('Название страницы', font_family='SFProDisplayBold', color_scheme='gray', size='2'),
                                                    rx.input(
                                                        rx.input.slot(
                                                            rx.icon('user', size=17, color=rx.color('gray', 9))
                                                        ),
                                                        value=State.tNamePage,
                                                        on_change=[State.set_tNamePage],
                                                        font_family='SFProDisplayBold',
                                                        placeholder='Видно только вам',
                                                    ),
                                                    direction='column',
                                                    spacing='1',
                                                ),
                                                rx.flex(
                                                    rx.button('Сохранить', font_family='SFProDisplayBold', on_click=State.save, size='1'),
                                                    direction='row',
                                                    justify='end'
                                                ),
                                                rx.divider(),
                                                rx.flex(
                                                    rx.flex(
                                                        rx.image('/images/pages/trash.png', width='26px'),
                                                        rx.text('Удаление страницы', font_family='SFProDisplayMedium', size='2'),
                                                        direction='row',
                                                        spacing='2',
                                                        align='center',
                                                    ),
                                                    rx.dialog.root(
                                                        rx.dialog.trigger(rx.button('Удалить', font_family='SFProDisplayBold', color_scheme='tomato', size='1')),
                                                        rx.dialog.content(
                                                            rx.flex(
                                                                rx.flex(
                                                                    rx.flex(
                                                                        rx.image('/icons/icons8-remove.svg', width='25px'),
                                                                        rx.flex(
                                                                            rx.text('Удаление страницы', font_family='SFProDisplayBold', size='3'),
                                                                            rx.text('Вы уверены, что желаете удалить страницу?', font_family='SFProDisplayMedium', size='2'),
                                                                            direction='column'
                                                                        ),
                                                                        spacing='2',
                                                                        direction='row',
                                                                        align='center'
                                                                    ),
                                                                    rx.flex(
                                                                        rx.badge('Esc', color_scheme='gray', variant="soft", font_family='SFProDisplayBold'),
                                                                        spacing='2',
                                                                        direction='row',
                                                                        align='center'
                                                                    ),
                                                                    spacing='2',
                                                                    direction='row',
                                                                    align='center',
                                                                    justify='between'
                                                                ),
                                                                rx.divider(margin_top='12px'),
                                                                rx.flex(
                                                                    rx.dialog.close(rx.button('Отмена', font_family='SFProDisplayBold', variant='surface', size='2')),
                                                                    rx.button('Удалить страницу', font_family='SFProDisplayBold', color_scheme='tomato', size='2', on_click=State.deletePage),
                                                                    direction='row',
                                                                    justify='end',
                                                                    spacing='2'
                                                                ),
                                                                direction='column',
                                                                spacing='2'
                                                            ),
                                                        ),
                                                    ),
                                                    align='center',
                                                    direction='row',
                                                    justify='between'
                                                ),
                                                direction='column',
                                                spacing='2'
                                            ),
                                            width='100%'
                                        ),
                                        rx.card(
                                            rx.flex(
                                                rx.text('ДОПОЛНИТЕЛЬНЫЕ НАСТРОЙКИ', font_family='SFMonoBold', size='2', color_scheme='gray'),
                                                direction='column',
                                                spacing='2'
                                            ),
                                            width='100%'
                                        ),
                                        align='start',
                                        width='900px',
                                        direction='row',
                                        spacing='2'
                                    ),
                                    value="tab2",
                                    margin_left='117px',
                                    margin_top='12px'
                                ),
                                rx.tabs.content(
                                    rx.text("item on tab 2", font_family='SFProDisplayBold'),
                                    value="tab3",
                                    margin_left='117px',
                                ),
                                default_value="tab1",
                                orientation="horizontal",
                            ),
                            direction='column',
                            spacing='2',
                            margin_top='60px'
                        ),
                        spacing='2',
                        direction='column'
                    ),
                    rx.flex(
                        rx.card(
                            rx.flex(
                                rx.center(
                                    rx.icon('circle-x', color=rx.color('tomato', 9), size=40),
                                ),
                                rx.center(
                                    rx.text('Ошибка', font_family='SFProDisplayBold', size='5'),
                                ),
                                rx.center(
                                    rx.text(State.tErrorText, font_family='SFProDisplayMedium', margin_bottom='16px', size='2'),
                                ),
                                direction='column',
                                spacing='1'
                            ),
                            width='100%'
                        ),
                        margin_top='12px'
                    ),
                ),
                direction='column'
            ),
            rx.center(
                rx.spinner(),
                height="100vh",  # Высота экрана
            )
        ),
        size='4'
    )