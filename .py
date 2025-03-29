import curses
import random
import time

# Game map dimensions
MAP_HEIGHT = 20
MAP_WIDTH = 40

# Player properties
player_x = MAP_WIDTH // 2
player_y = MAP_HEIGHT - 2  # Start near the bottom
player_icon = '^'  # Spaceship icon

# Enemy properties
enemy_icon = 'V'
enemies = []

# Bullet properties
bullet_icon = '|'
bullets = []

# Game map
game_map = [[' ' for _ in range(MAP_WIDTH)] for _ in range(MAP_HEIGHT)]

def initialize_game(stdscr):
    curses.curs_set(0)
    stdscr.nodelay(1)
    stdscr.timeout(50)  # Reduced delay for more responsiveness
    stdscr.clear()

def draw_map(stdscr):
    for y in range(MAP_HEIGHT):
        for x in range(MAP_WIDTH):
            stdscr.addch(y, x, game_map[y][x])

def draw_player(stdscr):
    stdscr.addch(player_y, player_x, player_icon)

def draw_enemies(stdscr):
    for ex, ey in enemies:
        stdscr.addch(ey, ex, enemy_icon)

def draw_bullets(stdscr):
    for bx, by in bullets:
        stdscr.addch(by, bx, bullet_icon)

def move_player(key):
    global player_x
    if key == curses.KEY_LEFT and player_x > 0:
        player_x -= 1
    elif key == curses.KEY_RIGHT and player_x < MAP_WIDTH - 1:
        player_x += 1

def shoot_bullet():
    bullets.append((player_x, player_y - 1))

def move_bullets():
    global bullets
    new_bullets = []
    for bx, by in bullets:
        if by > 0:
            new_bullets.append((bx, by - 1))
    bullets = new_bullets

def spawn_enemy():
    ex = random.randint(0, MAP_WIDTH - 1)
    ey = 0  # Spawn at the top
    enemies.append((ex, ey))

def move_enemies():
    global enemies
    new_enemies = []
    for ex, ey in enemies:
        if ey < MAP_HEIGHT - 1:
            new_enemies.append((ex, ey + 1))
    enemies = new_enemies

def main(stdscr):
    initialize_game(stdscr)

    # Main game loop
    while True:
        stdscr.clear()
        draw_map(stdscr)
        draw_player(stdscr)
        draw_enemies(stdscr)
        draw_bullets(stdscr)
        stdscr.refresh()

        key = stdscr.getch()
        if key == ord('q'):
            break
        elif key == ord(' '):
            shoot_bullet()
        else:
            move_player(key)

        move_bullets()
        move_enemies()

        # Spawn a new enemy occasionally
        if random.randint(1, 10) == 1:
            spawn_enemy()

        # Check for collisions
        for bx, by in bullets:
            for ex, ey in enemies:
                if bx == ex and by == ey:
                    enemies.remove((ex, ey))
                    bullets.remove((bx, by))
                    break

        time.sleep(0.05)

curses.wrapper(main)
