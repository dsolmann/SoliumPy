from lib import Connection, world
import random
import pygame
import os
from pprint import pprint

NAME = input("Input username ( admin | admin2 | admin3 ): ")
PW = "1234"
# HOST = input("ip: ")
# PORT = input("port: ")

HOST = "localhost"
PORT = "8956"

DEBUG = True
print(NAME+"  "+PW+"  "+HOST+"  "+PORT)
connection = Connection(total_debug=False,
                        handler=world.handler,
                        auth=(NAME, PW),
                        address=(HOST, int(PORT)))

print(os.getcwd())

pygame.init()
pygame.display.set_caption("Solium")
pygame.font.init()

font = pygame.font.SysFont('Roboto', 30)

winx = 1000
winy = 500
win = pygame.display.set_mode((winx, winy))


def main():
    CameraY = 0
    CameraX = 0
    MixingY = 0
    MixingX = 0
    run = True
    stopped_v = True
    stopped_h = True

    while run:
        c_player = None

        while not world.data:
            pass
        # pprint(world.data)
        for i in world.data["players"]:
            if i["name"] == NAME:
                c_player = i
        CameraX = c_player['x'] - winx / 2 + MixingX
        CameraY = c_player['y'] - winy / 2 + MixingY
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 4:
                    if c_player['active_item'] <= 8:
                        connection.action("active_item_change", data=c_player['active_item'] + 1)
                    else:
                        connection.action("active_item_change", data=0)
                if event.button == 5:
                    if c_player['active_item'] >= 0:
                        connection.action("active_item_change", data=c_player['active_item'] - 1)
                    else:
                        connection.action("active_item_change", data=8)

        keys = pygame.key.get_pressed()

        if pygame.mouse.get_pressed()[0]:
            connection.action("action", data={"x": int(pygame.mouse.get_pos()[0] + CameraX),
                                              "y": int(pygame.mouse.get_pos()[1] + CameraY)})
        if keys[pygame.K_1]:
            connection.action("active_item_change", data=0)
        if keys[pygame.K_2]:
            connection.action("active_item_change", data=1)
        if keys[pygame.K_3]:
            connection.action("active_item_change", data=2)
        if keys[pygame.K_4]:
            connection.action("active_item_change", data=3)
        if keys[pygame.K_5]:
            connection.action("active_item_change", data=4)
        if keys[pygame.K_6]:
            connection.action("active_item_change", data=5)
        if keys[pygame.K_7]:
            connection.action("active_item_change", data=6)
        if keys[pygame.K_8]:
            connection.action("active_item_change", data=7)
        if keys[pygame.K_9]:
            connection.action("active_item_change", data=8)
        if keys[pygame.K_a] and c_player['x'] > 0 and stopped_h:
            connection.action("left")
            stopped_h = False
        if keys[pygame.K_d] and c_player['x'] < winx - 40 and stopped_h:
            connection.action("right")
            stopped_h = False
        if keys[pygame.K_w] and c_player['y'] > 0 and stopped_v:
            connection.action("up")
            stopped_v = False
        if keys[pygame.K_s] and c_player['y'] < winy - 40 and stopped_v:
            connection.action("down")
            stopped_v = False
        if not (keys[pygame.K_w] or keys[pygame.K_s]) and not stopped_v:
            connection.action("stop", "vertical")
            stopped_v = True
        if not (keys[pygame.K_a] or keys[pygame.K_d]) and not stopped_h:
            connection.action("stop", "horizontal")
            stopped_h = True
        i = 0
        while i <= 500:
            pygame.draw.rect(win, (100, 100, 100), (winx / 2 - 225 + i - CameraX, 100 - CameraY+random.randint(0, 3), 50, 50), 2)
            i += 50
        for player in world.data["players"]:
            x = player['x'] - CameraX
            y = player['y'] - CameraY
            image = pygame.transform.scale(pygame.image.load('assets/players/player'+str(+random.randint(1, 4))+'.png').convert_alpha(),
                                           (40, 40))
            win.blit(image, (x, y))
            image = pygame.transform.scale(pygame.image.load("assets/players/eye"+str(random.randint(1, 9))+".png").convert_alpha(), (40, 40))
            win.blit(image, (x, y))
            win.blit(font.render(player['name'], False, (255, 255, 255)), (x, y - 30))
        # pprint(world.data["objects"])
        for block in world.data['objects']:
            x = block['x'] - CameraX
            y = block['y'] - CameraY
            try:
                image = pygame.transform.scale(
                    pygame.image.load("assets/items/" + str(block['id']) + ".png").convert_alpha(), (40, 40))
            except:
                image = pygame.transform.scale(pygame.image.load("assets/items/404.png").convert_alpha(), (40, 40))
            win.blit(image, (x, y))
        interface(c_player)
        pygame.display.update()
        pygame.time.delay(0)
        win.fill((random.randint(0, 100), random.randint(0, 100), random.randint(100, 255)))


def interface(c_player):
    # if DEBUG:
        # win.blit(font.render(f"x: {c_player['x']}; y: {c_player['y']}", False, (255, 255, 255)), (winx - 200, 20))

    pygame.draw.rect(win, (232, 81, 81), (0, int(winy - 20), c_player["hp"]+random.randint(0, 30) / 100 * winx, 20))
    i = 0

    while i <= 8:
        pygame.draw.rect(win, (100, 100, 100), (winx / 2 - 225 + i * 50+random.randint(0, 3), 0+random.randint(0, 30) , 50, 50), 2)
        if i < len(c_player['inventory']):
            try:
                image = pygame.transform.scale(
                    pygame.image.load("assets/items/" + str(c_player['inventory'][i]) + ".png").convert_alpha(),
                    (50, 50))
            except:
                image = pygame.transform.scale(
                    pygame.image.load("assets/items/404.png").convert_alpha(),
                    (50, 50))
        win.blit(image, (winx / 2 - 225 + i * 50, 0+random.randint(0, 10)))
        if i == c_player['active_item']:
            pygame.draw.rect(win, (227, 70, 76), (winx / 2 - 225 + i * 50, 0, 50, 50), 2)
        i += 1
try:
    main()
except Exception as e:
    print(e)
    input()