import matplotlib.pyplot as plt
import numpy as np
from matplotlib.animation import FuncAnimation
from scipy import interpolate

from terrain import terrain


WIDTH = 1024
SCREEN_HIGHT = 768
TER_HIGHT = 300
YZOOM = 100
ASPECT = SCREEN_HIGHT / WIDTH
XZOOM = YZOOM / ASPECT
g = -1
a = 1
dt = 0.05



octagon_x = np.array([-1, 1, 1 + np.sqrt(2), 1 + np.sqrt(2), 1, -1, -1 - np.sqrt(2), -1 - np.sqrt(2), -1])
octagon_y = np.array([-1 - np.sqrt(2),-1 - np.sqrt(2), -1, 1, 1 + np.sqrt(2), 1 + np.sqrt(2), 1, -1,-1 - np.sqrt(2)])

rectangle_x = np.array([-1 - np.sqrt(2), 1 + np.sqrt(2), 1 + np.sqrt(2), -1 - np.sqrt(2), -1 - np.sqrt(2)])
rectangle_y = np.array([-1 - np.sqrt(2), -1 - np.sqrt(2), -1 - 1.5 * np.sqrt(2), -1 - 1.5 * np.sqrt(2), -1 - np.sqrt(2)])

trapezium_x = np.array([-1, -1 - 1 * 0.75 * np.sqrt(2), 1 + 0.75 * np.sqrt(2), 1])
trapezium_y = np.array([-1 - 1.5 * np.sqrt(2), -2 - 2.3 * np.sqrt(2), -2 - 2.3 * np.sqrt(2), -1 - 1.5 * np.sqrt(2)])

leg_x = np.array([-1 - np.sqrt(2), -1 - 1.75 * np.sqrt(2)])
leg_y = np.array([-1 - 1.5 * np.sqrt(2), -2 - 2.5 * np.sqrt(2)])

foot_x = np.array([-1 - 2.1 * np.sqrt(2), -1 - 1.5 * np.sqrt(2)])
foot_y = np.array([-2 - 2.5 * np.sqrt(2), -2 - 2.5 * np.sqrt(2)])

fire_x = np.array([-1 - 1 * 0.75 * np.sqrt(2), 0, 1 + 0.75 * np.sqrt(2)])
fire_y = np.array([-2 - 2.3 * np.sqrt(2), -2 - 2.3 * np.sqrt(2), -2 - 2.3 * np.sqrt(2)])

lander_x = [octagon_x, rectangle_x, trapezium_x, leg_x, -leg_x, foot_x, -foot_x, fire_x]
lander_y = [octagon_y, rectangle_y, trapezium_y, leg_y, leg_y, foot_y, foot_y, fire_y]


rectangle_explode_x = np.array([(-1 - 1 * np.sqrt(2)) / 3, -1 - np.sqrt(2), -1 - np.sqrt(2), (2 + 2 * np.sqrt(2)) / 3])
rectangle_explode_y = np.array([0, 0, -0.5 * np.sqrt(2), -0.5 * np.sqrt(2)])

trapezium_explode_x = np.array([-1, -1 - 1 * 0.75 * np.sqrt(2), (1 + 0.75 * np.sqrt(2)) * 0.3])
trapezium_explode_y = np.array([0, -1 - 0.8 * np.sqrt(2), -1 - 0.8 * np.sqrt(2)])

lander_explode_x = [octagon_x, rectangle_explode_x, -rectangle_explode_x, trapezium_explode_x, -trapezium_explode_x, leg_x, -leg_x, foot_x, -foot_x]
lander_explode_y = [octagon_y, rectangle_explode_y, -rectangle_explode_y, trapezium_explode_y, trapezium_explode_y, leg_y + 1 + 1.5 * np.sqrt(2), leg_y + 1 + 1.5 * np.sqrt(2), foot_y + 1 + 1.5 * np.sqrt(2), foot_y + 1 + 1.5 * np.sqrt(2)]

game_data = np.zeros(24)
explode_data = np.zeros(27)

def press(event):
    if game_data[20] > 0:
        if event.key == 'up':
            if game_data[1] < 10:
                game_data[1] += 1
                lander_y[7][1] -= 1
        if event.key == 'left':
            game_data[0] += 0.03
        if event.key == 'right':
            game_data[0] -= 0.03
        
class fake_event:
    key = 'up'

def release(event):
    if event.key == 'up':
        game_data[1] = 0
        lander_y[7][1] = lander_y[7][0]
 
        
        
def rotate(x, y, angle):
    return x * np.cos(angle) - y * np.sin(angle), x * np.sin(angle) + y * np.cos(angle)

xt = 0
yt = 0

y0 = 450
x0 = 300
rot0 = -np.pi / 2
vx0 = 30
vy0 = -10
game_data[3] = y0#185
game_data[5] = x0#389
game_data[0] = rot0
game_data[2] = vy0
game_data[4] = vx0
game_data[9] = 1
game_data[17] = 1
game_data[20] = 10000
game_data[22] = 22

plt.rcParams.update({'font.size': 16, 'font.family' : 'monospace'})
fig = plt.figure(facecolor='k',edgecolor='k')
fig.canvas.mpl_connect('key_press_event', press)
fig.canvas.mpl_connect('key_release_event', release)
plt.style.use('dark_background')
bg, = plt.plot(terrain[0] * WIDTH, terrain[1] * TER_HIGHT, color='white')
#plt.get_current_fig_manager().full_screen_toggle()#.resize(1920, 1080)
plt.get_current_fig_manager().resize(1920, 1080)
#fig.canvas.header_visible = True
#fig.canvas.footer_visible = False
#fig.canvas.statusBar().setVisible(False)
alti_template = 'ALTITUDE               '
vx_template   = 'HORIZONTAL SPEED       '
vy_template   = 'VERTICAL SPEED         '
alti_template_num = '%i'
vx_template_num   = '%i'
vy_template_num   = '%i'
time_template   = 'TIME     %02i:%02i'
fuel_template   = 'FUEL     %04i'
score_template  = 'SCORE    %04i'

crash_template = "YOU'VE ONLY GONE AND DIED \n\n\n AND LOST %i OF FUEL"
landed_template = "LANDED... WHAT YOU WANT A MEDAL OR SOMETHING"
hard_land_template = "LANDED... BUT IT'S A ONE WAY TRIP"

plt.gca().set_aspect(ASPECT)


#plt.gca().set_aspect('equal')
plt.axis('off')
plt.tight_layout()
plt.xlim(0, WIDTH)
plt.ylim(0, SCREEN_HIGHT)

ax = plt.gca()

alti_text = plt.text(0.6, 0.99, '', color='w', ha="left", transform=ax.transAxes)
vx_text = plt.text(0.6, 0.95, '', color='w', ha="left", transform=ax.transAxes)
vy_text = plt.text(0.6, 0.91, '', color='w', ha="left", transform=ax.transAxes)

alti_text_num = plt.text(0.8, 0.99, '', color='w', ha="right", transform=ax.transAxes)
vx_text_num = plt.text(0.8, 0.95, '', color='w', ha="right", transform=ax.transAxes)
vy_text_num = plt.text(0.8, 0.91, '', color='w', ha="right", transform=ax.transAxes)

score_text = plt.text(0.1, 0.99, '', color='w', ha="left", transform=ax.transAxes)
time_text = plt.text(0.1, 0.95, '', color='w', ha="left", transform=ax.transAxes)
fuel_text = plt.text(0.1, 0.91, '', color='w', ha="left", transform=ax.transAxes)

alti_text.set_text(alti_template)
vx_text.set_text(vx_template)
vy_text.set_text(vy_template)
alti_text.set_text(alti_template_num % (0))
vx_text.set_text(vx_template_num % (0))
vy_text.set_text(vy_template_num % (0))
fuel_text.set_text(fuel_template % (game_data[20]))
score_text.set_text(score_template % (game_data[21]))
time_text.set_text(time_template % (0, 0))

vx_arrow = plt.arrow(0.9, 0.958, 0.02, 0, head_width=0.02, head_length=0.01, fc='w', ec='w', transform=ax.transAxes)
vy_arrow = plt.arrow(0.825, 0.93, 0, -0.025, head_width=0.0115, head_length=0.015, fc='w', ec='w', transform=ax.transAxes)

crash_text = plt.text(0.5, 0.5, '', color='w', ha="center", transform=ax.transAxes)



lander = []
for i in range(len(lander_x)):
    x, y = rotate(lander_x[i], lander_y[i], 0)
    line, = plt.plot(x + xt, y + yt, color='white', linewidth=1)
    lander.append(line)

lander_explode = []
for i in range(len(lander_explode_x)):
    line, = plt.plot([], [], color='white', linewidth=1)
    lander_explode.append(line)


ter_x = np.copy(terrain[0] * WIDTH)
ter_xy = np.copy(terrain[1] * TER_HIGHT)
current_ter_y = np.concatenate([ter_xy, ter_xy])
current_ter_x = np.concatenate([ter_x, ter_x + WIDTH])
#print(len(ter_xy))

#i = 13 # first pad
#i = 45 # pad 2
#i = 63 # pad 3
#i = 132 # pad 4
pad_pos = np.array([13, 45, 63, 132])
multis = ['X3', 'X2', 'X5', 'X2']
multis *= 2
score_multiplier = np.array([3, 2, 5, 2])
#pad_pos = np.concatenate((pad_pos, pad_pos + 159))
landing_pads = []
pad_text = []
for i, pad in enumerate(pad_pos):
    line, = plt.plot(current_ter_x[pad:pad+2], current_ter_y[pad:pad+2], color='w', linewidth=2)
    mul_text = plt.text(np.mean(current_ter_x[pad:pad+2]), current_ter_y[pad] - game_data[22], multis[i], ha='center')
    landing_pads.append(line)
    pad_text.append(mul_text)


def run(data):
    if game_data[8]:
        if not game_data[19]:
            game_data[19] = 1
            lx = []
            for j in range(len(lander_x) - 1):
                lx.append(lander[j].get_data()[0])
            lx = np.concatenate(lx)
            for i in range(len(landing_pads)):
                px0, px1 = landing_pads[i].get_data()[0]
                if np.all(np.logical_and(px0 < lx, px1 > lx)):
                    game_data[19] = score_multiplier[i]      
        if game_data[2] < -15 or abs(game_data[0]) > 0.03 or abs(game_data[4]) > 31:
            if not game_data[18]:
                lost_fuel = np.random.randint(185, 285)
                crash_text.set_text(crash_template % lost_fuel)
                game_data[20] -= lost_fuel
                fuel_text.set_text(fuel_template % (game_data[20]))
                game_data[21] += 5 * game_data[19]
                score_text.set_text(score_template % game_data[21])
                explode_data[0:9] = game_data[5]
                explode_data[9:18] = game_data[3] + 5
                for i in range(len(lander_x)):
                    lander[i].set_data([], [])
                game_data[18] = 1
            for i in range(len(lander_explode_x)):
                x, y = rotate(lander_explode_x[i], lander_explode_y[i], explode_data[i + 18])
                lander_explode[i].set_data(x * ASPECT + explode_data[i], y + explode_data[i + 9])
            
            # octagon
            explode_data[9] += 0.4
            explode_data[18] -= 0.5
            # rectangle
            explode_data[1] -= 0.2
            explode_data[10] += 0.2
            explode_data[2] += 0.2
            explode_data[11] += 0.5
            # trap
            explode_data[3] -= 0.1
            explode_data[12] += 0.5
            explode_data[4] += 0.1
            explode_data[13] += 0.5
            # left leg
            explode_data[5] -= 0.2
            explode_data[14] += 0.1
            explode_data[7] -= 0.2
            explode_data[16] += 0.1
            # right leg
            explode_data[6] += 0.2
            explode_data[15] += 0.18
            explode_data[8] += 0.2
            explode_data[17] += 0.18

        elif game_data[2] < -5:
            if not game_data[18]:
                crash_text.set_text(hard_land_template)
                game_data[21] += 15 * game_data[19]
                score_text.set_text(score_template % game_data[21])
                game_data[18] = 1
        elif game_data[2] > -5:
            if not game_data[18]:
                crash_text.set_text(landed_template)
                game_data[21] += 50 * game_data[19]
                score_text.set_text(score_template % game_data[21])
                game_data[20] += 50
                fuel_text.set_text(fuel_template % game_data[20])
                game_data[18] = 1

        if game_data[-1] == 100:
            for i in range(len(lander_explode_x)):
                lander_explode[i].set_data([], [])
            crash_text.set_text('')
            game_data[0:15] = 0
            game_data[17:20] = 0
            game_data[22] = 22
            game_data[3] = y0#185
            game_data[5] = x0#389
            game_data[0] = rot0
            game_data[2] = vy0
            game_data[4] = vx0
            game_data[9] = 1
            game_data[17] = 1
            game_data[-1] = 0
        game_data[-1] += 1

        return game_data
    
    game_data[2] += game_data[1] * a * np.cos(game_data[0]) * dt + g * dt
    game_data[4] -= game_data[1] * a * np.sin(game_data[0]) * dt
    game_data[3] += game_data[2] * dt
    
    if game_data[5] < WIDTH * 0.2 and game_data[4] < 0:
        if game_data[6] <= 0:
            game_data[6] = WIDTH
        game_data[6] += game_data[4] * dt  
        game_data[7] = 1   
    elif game_data[5] > WIDTH * 0.8 and game_data[4] > 0:
        if game_data[6] >= WIDTH:
            game_data[6] = 0
        game_data[6] += game_data[4] * dt
        game_data[7] = -1   
    else:
        game_data[5] += game_data[4] * dt
        game_data[7] = 0

    current_ter_x[:159] = ter_x - game_data[6]
    current_ter_x[159::] = ter_x - game_data[6] + WIDTH
    bg.set_data(current_ter_x, current_ter_y)
    for i in range(len(landing_pads)):
        landing_pads[i].set_data(current_ter_x[pad_pos[i] : pad_pos[i] + 2], current_ter_y[pad_pos[i] : pad_pos[i] + 2])
        pad_text[i].set_position((np.mean(current_ter_x[pad_pos[i] : pad_pos[i] + 2]), current_ter_y[pad_pos[i]] - game_data[22]))
    f = interpolate.interp1d(current_ter_x, current_ter_y)
    for i in range(len(lander_x)):
        x, y = rotate(lander_x[i], lander_y[i], game_data[0])
        lander[i].set_data(x * ASPECT + game_data[5], y + game_data[3])
        if i != 7:
            ter_y = f(lander[i].get_data()[0])
            lan_y = lander[i].get_data()[1]
            if any(lan_y <= ter_y):
                game_data[8] = 1
                return game_data

###################### this bit is a total bodge, don't look it'll make you sad #######################
    if game_data[3] < f(game_data[5]) + 100:                                                          #
        if game_data[9]:                                                                              #
            game_data[22] = 7                                                                         #
            game_data[10] = game_data[5] - XZOOM                                                      #
            game_data[11] = game_data[5] + XZOOM                                                      #
            game_data[12] = game_data[3] - YZOOM                                                      #
            game_data[13] = game_data[3] + YZOOM                                                      #
            plt.xlim(game_data[10], game_data[11])                                                    #
            plt.ylim(game_data[12], game_data[13])                                                    #
            game_data[9] = 0                                                                          #
        elif game_data[3] <= game_data[12] + YZOOM * 0.5:                                             #
            if not game_data[14]:                                                                     #
                game_data[14] = game_data[3] - game_data[12]                                          #
            plt.xlim(game_data[10], game_data[11])                                                    #
            plt.ylim(game_data[3] - YZOOM + game_data[14], game_data[3] + YZOOM + game_data[14])      #
            if game_data[5] <= game_data[10] + XZOOM * 0.5:                                           #
                if not game_data[15]:                                                                 #
                    game_data[15] = game_data[5] - game_data[10]                                      #
                plt.xlim(game_data[5] - XZOOM + game_data[15], game_data[5] + XZOOM + game_data[15])  #
            elif game_data[5] >= game_data[11] - XZOOM * 0.5:                                         #
                if not game_data[15]:                                                                 #
                    game_data[15] = game_data[5] - game_data[11]                                      #
                plt.xlim(game_data[5] - XZOOM + game_data[15], game_data[5] + XZOOM + game_data[15])  #
    else:                                                                                             #
        if not game_data[9]:                                                                          #
            game_data[22] = 22                                                                        #
        plt.xlim(0, WIDTH)                                                                            #
        plt.ylim(0, SCREEN_HIGHT)                                                                     #
        game_data[9] = 1                                                                              #
        game_data[14] = 0                                                                             #
        game_data[15] = 0                                                                             #
#######################################################################################################
    alti_text.set_text(alti_template)
    vx_text.set_text(vx_template)
    vy_text.set_text(vy_template)   
    alti_text_num.set_text(alti_template_num % (lander[-2].get_data()[1].min() - f(game_data[5])))
    if game_data[4] >= 0:
        vx_arrow.set_data(x=0.81, dx=0.02)
    else:
        vx_arrow.set_data(x=0.84, dx=-0.02)
    vx_text_num.set_text(vx_template_num % (abs(game_data[4])))
    if game_data[2] >= 0:
        vy_arrow.set_data(y=0.90, dy=0.025)
    else:
        vy_arrow.set_data(y=0.937, dy=-0.025)
    vy_text_num.set_text(vy_template_num % (abs(game_data[2])))
    time_text.set_text(time_template % (divmod(game_data[16], 60)))
    if game_data[1] and game_data[20] > 0:
        game_data[20] -= 1
        fuel_text.set_text(fuel_template % (game_data[20]))
    elif game_data[20] == 0:
        release(fake_event)
    game_data[16] += dt
    #print(game_data[16] % 0.8)
    if game_data[16] % 0.8 < 0.5:
        bg.set_linewidth(1)
        bg.set_color('w')
        for i in range(len(landing_pads)):
            landing_pads[i].set_linewidth(2)
            pad_text[i].set_text(multis[i])
    else:
        bg.set_linewidth(0.6)
        bg.set_color('whitesmoke')
        for i in range(len(landing_pads)):
            landing_pads[i].set_linewidth(0)
            pad_text[i].set_text('')

    return game_data


ani = FuncAnimation(fig, run, interval=dt * 1000, cache_frame_data=False)
plt.show()
