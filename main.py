import dearpygui.dearpygui as dpg
import win32api
import win32con
import win32gui

import string
import time
from threading import Thread
import os

def disable_maximize():
    if os.name == 'nt':
        time.sleep(0.002)
        hwnd = win32gui.GetForegroundWindow()
        win32api.SetWindowLong(hwnd, win32con.GWL_STYLE,
                            win32api.GetWindowLong(hwnd, win32con.GWL_STYLE) & ~win32con.WS_MAXIMIZEBOX)

BUTTON_WIDTH = 98
BUTTON_HEIGHT = 60
ALIAS_VALUES = {
    "÷": "/",
    "×": "*",
}

OPS = ["+", "-", "/", "*"]

expression = ""
has_dot = False

dpg.create_context()
dpg.create_viewport()
dpg.setup_dearpygui()

with dpg.font_registry():
    default_font = dpg.add_font("./SegUIVar.ttf", 30)
    small_font = dpg.add_font("./SegUIVar.ttf", 20)


with dpg.theme() as primarybtn_blue_theme:
    with dpg.theme_component(dpg.mvButton):
        dpg.add_theme_style(dpg.mvStyleVar_FrameRounding, 5, category=dpg.mvThemeCat_Core)
        dpg.add_theme_color(dpg.mvThemeCol_Button, (52, 103, 179), category=dpg.mvThemeCat_Core)
        dpg.add_theme_color(dpg.mvThemeCol_ButtonHovered, (44, 89, 156), category=dpg.mvThemeCat_Core)

with dpg.theme() as primarybtn_red_theme:
    with dpg.theme_component(dpg.mvButton):
        dpg.add_theme_style(dpg.mvStyleVar_FrameRounding, 5, category=dpg.mvThemeCat_Core)
        dpg.add_theme_color(dpg.mvThemeCol_Button, (252, 3, 74), category=dpg.mvThemeCat_Core)
        dpg.add_theme_color(dpg.mvThemeCol_ButtonHovered, (214, 4, 64), category=dpg.mvThemeCat_Core)

with dpg.theme() as global_theme:
    with dpg.theme_component(dpg.mvAll):
        dpg.add_theme_color(dpg.mvThemeCol_FrameBg, (255, 140, 23), category=dpg.mvThemeCat_Core)
        dpg.add_theme_style(dpg.mvStyleVar_FrameRounding, 5, category=dpg.mvThemeCat_Core)
        dpg.add_theme_style(dpg.mvStyleVar_WindowBorderSize, 0, category=dpg.mvThemeCat_Core)
        dpg.add_theme_color(dpg.mvThemeCol_ButtonHovered, (44, 89, 156), category=dpg.mvThemeCat_Core)

def safe_eval(exprs: str) -> tuple[str, bool]:
    '''Not so safe eval'''
    if exprs == "":
        return "0", False
    if exprs in string.ascii_letters:
        return "0", False
    try:
        return str(eval(exprs)), True
    except Exception as e:
        print(e.msg)
        return "0", False

def is_num(s) -> bool:
    try:
        float(s)
        return True
    except ValueError:
        return False

def btn_clicked(sender, app_data, user_data):
    global expression
    global has_dot
    
    val: str = dpg.get_value("input")
    val_or_alias: str = ALIAS_VALUES.get(user_data, user_data)

    if user_data == "AC":
        expression = ""
        dpg.set_value("input", "0")
        has_dot = False
        return
    elif user_data == "C":
        dpg.set_value("input", "0")
        return
    elif user_data == "DEL":
        length = len(val)
        if length > 0 and val != "0":
            if length == 1:
                dpg.set_value("input", "0")
            else:
                dpg.set_value("input", val[:-1])
        return
    elif user_data == "=":
        res, success = safe_eval(expression)
        if success:
            dpg.set_value("input", res)
        return
    elif user_data == "+/-":
        if is_num(expression) and val != "0":
            if expression.startswith('-'):
                expression = expression[1:]
            else:
                expression = "-" + expression
            dpg.set_value("input", expression)
        return
    elif user_data == "%": 
        if is_num(expression):
            expression = str(float(expression) / 100)
            dpg.set_value("input", expression)
        return

    if val == "0" and user_data != ".":
        if val_or_alias in OPS:
            expression += "0" + val_or_alias
            dpg.set_value("input", "0" + user_data)
            return

        dpg.set_value("input", user_data)
        expression = val_or_alias
        return

    if val_or_alias in OPS:
        has_dot = False
        if len(expression) > 0 and expression[-1] in OPS:
            prev_expr = expression[:-1]
            expression = prev_expr + val_or_alias
            dpg.set_value("input", prev_expr + user_data)
            return

    if val_or_alias == ".":
        if has_dot:
            return
        has_dot = True
        expression += "."
        dpg.set_value("input", val + user_data)
        return


    dpg.set_value("input", val + user_data)
    expression = expression + val_or_alias



with dpg.window() as main_window:
    dpg.bind_font(default_font)

    dpg.add_text("0", tag="input")
    dpg.add_spacer(height=10)

    with dpg.group(horizontal=True):
        ce_btn = dpg.add_button(label="AC", width=BUTTON_WIDTH, height=BUTTON_HEIGHT, callback=btn_clicked, user_data="AC")
        dpg.bind_item_theme(ce_btn, primarybtn_red_theme)
        c_btn = dpg.add_button(label="C", width=BUTTON_WIDTH, height=BUTTON_HEIGHT, callback=btn_clicked, user_data="C")
        dpg.bind_item_theme(c_btn, primarybtn_blue_theme)
        del_btn = dpg.add_button(label="DEL", width=BUTTON_WIDTH, height=BUTTON_HEIGHT, callback=btn_clicked, user_data="DEL")
        dpg.bind_item_theme(del_btn, primarybtn_blue_theme)
        dpg.add_button(label="%", width=BUTTON_WIDTH, height=BUTTON_HEIGHT, callback=btn_clicked, user_data="%")
    
    dpg.add_spacer(height=2)

    with dpg.group(horizontal=True):
        dpg.add_button(label="7", width=BUTTON_WIDTH, height=BUTTON_HEIGHT, callback=btn_clicked, user_data="7")
        dpg.add_button(label="8", width=BUTTON_WIDTH, height=BUTTON_HEIGHT, callback=btn_clicked, user_data="8")
        dpg.add_button(label="9", width=BUTTON_WIDTH, height=BUTTON_HEIGHT, callback=btn_clicked, user_data="9")
        dpg.add_button(label="÷", width=BUTTON_WIDTH, height=BUTTON_HEIGHT, callback=btn_clicked, user_data="÷")
    
    dpg.add_spacer(height=2)
    
    with dpg.group(horizontal=True):
        dpg.add_button(label="4", width=BUTTON_WIDTH, height=BUTTON_HEIGHT, callback=btn_clicked, user_data="4")
        dpg.add_button(label="5", width=BUTTON_WIDTH, height=BUTTON_HEIGHT, callback=btn_clicked, user_data="5")
        dpg.add_button(label="6", width=BUTTON_WIDTH, height=BUTTON_HEIGHT, callback=btn_clicked, user_data="6")
        dpg.add_button(label="×", width=BUTTON_WIDTH, height=BUTTON_HEIGHT, callback=btn_clicked, user_data="×")
    
    dpg.add_spacer(height=2)

    with dpg.group(horizontal=True):
        dpg.add_button(label="1", width=BUTTON_WIDTH, height=BUTTON_HEIGHT, callback=btn_clicked, user_data="1")
        dpg.add_button(label="2", width=BUTTON_WIDTH, height=BUTTON_HEIGHT, callback=btn_clicked, user_data="2")
        dpg.add_button(label="3", width=BUTTON_WIDTH, height=BUTTON_HEIGHT, callback=btn_clicked, user_data="3")
        dpg.add_button(label="-", width=BUTTON_WIDTH, height=BUTTON_HEIGHT, callback=btn_clicked, user_data="-")
        

    dpg.add_spacer(height=2)

    with dpg.group(horizontal=True):
        dpg.add_button(label="+/-", width=BUTTON_WIDTH, height=BUTTON_HEIGHT, callback=btn_clicked, user_data="+/-")
        dpg.add_button(label="0", width=BUTTON_WIDTH, height=BUTTON_HEIGHT, callback=btn_clicked, user_data="0")
        dpg.add_button(label=".", width=BUTTON_WIDTH, height=BUTTON_HEIGHT, callback=btn_clicked, user_data=".")
        dpg.add_button(label="+", width=BUTTON_WIDTH, height=BUTTON_HEIGHT, callback=btn_clicked, user_data="+")

    dpg.add_spacer(height=1)

    equal = dpg.add_button(label="=", width=-1, height=BUTTON_HEIGHT, callback=btn_clicked, user_data="=")
    dpg.bind_item_theme(equal, primarybtn_blue_theme)


dpg.bind_theme(global_theme)
dpg.set_viewport_title("DPG Calculator")
dpg.set_primary_window(main_window, True)
dpg.set_viewport_resizable(False)
dpg.set_viewport_width(450)
dpg.set_viewport_height(520)
dpg.show_viewport()
Thread(target=disable_maximize).start()
dpg.start_dearpygui()
dpg.destroy_context()

