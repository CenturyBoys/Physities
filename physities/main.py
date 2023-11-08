# This is a sample Python script.
import time

from physities.src.unit import *


# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.


def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f"Hi, {name}")  # Press Ctrl+F8 to toggle the breakpoint.


# Press the green button in the gutter to run the script.
if __name__ == "__main__":
    c2 = Centimetre*Centimetre
    l = c2(5).convert(unit=Metre2)
    c = Centimetre(10)
    s1 = time.time()
    lala = c*3
    t1 = time.time() - s1
    s2 = time.time()
    lala = 10*3
    t2 = time.time() - s2
    print(f't1: {t1}, t2: {t2}, t2-t1: {t2-t1}, t2/t1: {t2/t1}')

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
