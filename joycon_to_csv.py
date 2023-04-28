from time import sleep

from pyjoycon import PythonicJoyCon, get_R_id

joycon_id = get_R_id()
joycon = PythonicJoyCon(*joycon_id)

MIN_X = 650
MAX_X = 3105
NEUTRAL_X = (1976 - MIN_X) / (MAX_X - MIN_X)
NEUTRAL_Y = 1983
MIN_Y = 850
MAX_Y = 3100
NEUTRAL_Y = (1983 - MIN_Y) / (MAX_Y - MIN_Y)
size = 1.0
while 1:
    x = (joycon.get_stick_right_horizontal() - MIN_X)/(MAX_X - MIN_X) - NEUTRAL_X
    y = (joycon.get_stick_right_vertical() - MIN_Y)/(MAX_Y - MIN_Y) - NEUTRAL_Y
    if abs(x) < 0.1:
        x = 0.0
    else:
        x = 5*x
    if abs(y) < 0.05:
        y = 0.0
    else:
        y = 25*y
    
    lw, rw = y+x, y-x

    f = open("remote_control.txt", "w")
    f.write(str(lw)+","+str(rw)+"\n")
    f.close()

    if joycon.get_button_a():
        size += 0.5
        if size >= 3.0:
            size = 3.
    if joycon.get_button_b():
        size -= 0.5
        if size <= 0.:
            size = 0.5

    with open('size.txt', "w") as s:
        s.write(str(size).replace(".", ","))
    sleep(0.2)