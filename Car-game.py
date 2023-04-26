
import random
from ursina import *

app = Ursina()
camera.orthographic = True
camera.fov = 13

car = Entity(
    model='quad',
    texture='assets/car.png',
    collider='box',
    scale=(2, 1),
    rotation_z=-90
)

road1 = Entity(
    model='quad',
    texture='assets/road.png',
    scale=15,
    z=1
)

road2 = duplicate(road1, y=15)
pair = [road1, road2]

enemies = []
score = 0

score_text = Text(text=f"Score: {score}", origin=(0, -4), scale=2)

def new_enemy():
    val = random.uniform(-2, 2)
    new = duplicate(
        car,
        texture='assets/enemy.png',
        x=2*val,
        y=25,
        color=color.random_color(),
        rotation_z=90 if val < 0 else -90
    )
    enemies.append(new)
    invoke(new_enemy, delay=0.5)

def increase_score():
    global score
    score += 5  # increment the score by 5
    score_text.text = f"Score: {score}"  # update the score text
    invoke(increase_score, delay=5)  # call this function again after 5 seconds

def update():
    global enemies
    car.x -= held_keys['a'] * 5 * time.dt
    car.x += held_keys['d'] * 5 * time.dt
    car.y -= held_keys['s'] * 5 * time.dt
    car.y += held_keys['w'] * 5 * time.dt
    for road in pair:
        road.y -= 6 * time.dt
        if road.y < -15:
            road.y += 30
    for enemy in enemies:
        if enemy.x < 0:
            enemy.y -= 10 * time.dt
        else:
            enemy.y -= 5 * time.dt
        if car.intersects(enemy).hit:
            print("Game Over!")
            destroy(enemy)
            enemies.remove(enemy)
            app.quit()

            # terminate the game by stopping the app
            application.quit()

invoke(new_enemy, delay=0.5)  # invoke the new_enemy function to start creating enemies
invoke(increase_score, delay=5)  # invoke the increase_score function after 5 seconds

app.run()
