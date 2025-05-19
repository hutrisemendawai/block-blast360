import pygame, random
pygame.init()

# Configuration
WIDTH, HEIGHT = 400, 400
ROWS, COLS = 10, 10
BLOCK_SIZE = WIDTH // COLS

# Pygame setup
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Block Blast")
clock = pygame.time.Clock()

# Load sound effects
try:
    clear_sound = pygame.mixer.Sound('clear.wav')
    powerup_sound = pygame.mixer.Sound('powerup.wav')
    game_over_sound = pygame.mixer.Sound('gameover.wav')
except FileNotFoundError:
    print("Sound files not found. Add 'clear.wav', 'powerup.wav', 'gameover.wav' to directory.")
    clear_sound = powerup_sound = game_over_sound = None

# High score persistence
high_score_file = 'highscore.txt'
try:
    with open(high_score_file, 'r') as f:
        high_score = int(f.read())
except:
    high_score = 0

# Game variables
base_colors = [(255, 0, 0), (0, 255, 0), (0, 0, 255), (255, 255, 0), (255, 0, 255), (0, 255, 255)]
colors = base_colors[:4]  # Start with 4 colors
score = 0
level = 1
time_limit = 120
moves_left = 10
bonus_time = 0
start_time = pygame.time.get_ticks() // 1000
font = pygame.font.SysFont('arial', 24)
game_over = False
particles = []
falling_blocks = []
power_ups = {}  # (r, c): type
locked_blocks = set()  # (r, c)
active_power_up = None
swap_first = None

class Particle:
    def __init__(self, x, y, color):
        self.x, self.y = x, y
        self.color = color
        self.vx = random.uniform(-2, 2)
        self.vy = random.uniform(-2, 2)
        self.lifetime = 30

    def update(self):
        self.x += self.vx
        self.y += self.vy
        self.lifetime -= 1

    def draw(self, surface):
        if self.lifetime > 0:
            pygame.draw.circle(surface, self.color, (int(self.x), int(self.y)), 3)

class FallingBlock:
    def __init__(self, r, c, color, target_r):
        self.r = r * BLOCK_SIZE
        self.c = c * BLOCK_SIZE
        self.color = color
        self.target_r = target_r * BLOCK_SIZE
        self.speed = 10

    def update(self):
        if self.r < self.target_r:
            self.r += self.speed
            return False
        return True

    def draw(self, surface):
        rect = pygame.Rect(self.c, int(self.r), BLOCK_SIZE, BLOCK_SIZE)
        pygame.draw.rect(surface, self.color, rect)
        pygame.draw.rect(surface, (255, 255, 255), rect, 1)

# Generate grid with power-ups and locked blocks
def generate_grid():
    global power_ups, locked_blocks
    grid = [[random.choice(colors) for _ in range(COLS)] for _ in range(ROWS)]
    power_ups.clear()
    locked_blocks.clear()
    for r in range(ROWS):
        for c in range(COLS):
            if random.random() < 0.05:
                power_ups[(r, c)] = random.choice(['bomb', 'swap', 'extra_moves'])
            if random.random() < 0.1:
                locked_blocks.add((r, c))
    while not has_moves(grid):
        grid = [[random.choice(colors) for _ in range(COLS)] for _ in range(ROWS)]
    return grid

# Find connected same-color group
def get_group(r, c, color, grid):
    stack = [(r, c)]
    group = set()
    while stack:
        x, y = stack.pop()
        if (x, y) in group:
            continue
        if 0 <= x < ROWS and 0 <= y < COLS and grid[x][y] == color:
            group.add((x, y))
            stack.extend([(x+1, y), (x-1, y), (x, y+1), (x, y-1)])
    return group

# Check valid moves
def has_moves(grid):
    for r in range(ROWS):
        for c in range(COLS):
            if grid[r][c] and len(get_group(r, c, grid[r][c], grid)) > 1:
                return True
    return False

# Apply power-up
def apply_power_up(power_type, r, c):
    global moves_left, grid
    if power_type == 'bomb':
        for dr in [-1, 0, 1]:
            for dc in [-1, 0, 1]:
                nr, nc = r + dr, c + dc
                if 0 <= nr < ROWS and 0 <= nc < COLS:
                    grid[nr][nc] = None
                    locked_blocks.discard((nr, nc))
                    power_ups.pop((nr, nc), None)
    elif power_type == 'swap':
        return 'swap'
    elif power_type == 'extra_moves':
        moves_left += 5
    if powerup_sound:
        powerup_sound.play()
    return None

# Initialize grid
grid = generate_grid()

running = True
level_threshold = level * 500

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN and not game_over:
            mx, my = pygame.mouse.get_pos()
            r, c = my // BLOCK_SIZE, mx // BLOCK_SIZE
            if 0 <= r < ROWS and 0 <= c < COLS and grid[r][c]:
                if active_power_up == 'swap':
                    if swap_first is None:
                        swap_first = (r, c)
                    else:
                        r2, c2 = swap_first
                        grid[r][c], grid[r2][c2] = grid[r2][c2], grid[r][c]
                        active_power_up = None
                        swap_first = None
                        if powerup_sound:
                            powerup_sound.play()
                else:
                    group = get_group(r, c, grid[r][c], grid)
                    if len(group) > 1 and moves_left > 0:
                        moves_left -= 1
                        score += len(group) * 10
                        if clear_sound:
                            clear_sound.play()
                        collected_power = None
                        if (r, c) in power_ups:
                            collected_power = power_ups.pop((r, c))
                        for x, y in group:
                            for _ in range(5):
                                particles.append(Particle(
                                    y * BLOCK_SIZE + BLOCK_SIZE // 2,
                                    x * BLOCK_SIZE + BLOCK_SIZE // 2,
                                    grid[x][y]
                                ))
                        for x, y in group:
                            if (x, y) in locked_blocks:
                                locked_blocks.remove((x, y))
                            else:
                                grid[x][y] = None
                        if collected_power:
                            active_power_up = apply_power_up(collected_power, r, c)
                        # Apply gravity with animation
                        falling_blocks.clear()
                        for col_idx in range(COLS):
                            col_data = [(r_, grid[r_][col_idx]) for r_ in range(ROWS) if grid[r_][col_idx] is not None]
                            for r_ in range(ROWS):
                                grid[r_][col_idx] = None
                            for i, (old_r, color) in enumerate(col_data):
                                new_r = ROWS - len(col_data) + i
                                grid[new_r][col_idx] = color
                                if old_r != new_r:
                                    falling_blocks.append(FallingBlock(old_r, col_idx, color, new_r))
                        # Shift non-empty columns left
                        cols_nonempty = [
                            [grid[r_][c_] for r_ in range(ROWS)]
                            for c_ in range(COLS)
                            if any(grid[r_][c_] is not None for r_ in range(ROWS))
                        ]
                        cols_nonempty += [[None] * ROWS for _ in range(COLS - len(cols_nonempty))]
                        for c_ in range(COLS):
                            for r_ in range(ROWS):
                                grid[r_][c_] = cols_nonempty[c_][r_]
                        # Level-up logic
                        if score >= level_threshold:
                            level += 1
                            level_threshold = level * 500
                            bonus_time += 30
                            moves_left += 10
                            # Add new row
                            for r_ in range(ROWS-1, 0, -1):
                                for c_ in range(COLS):
                                    grid[r_][c_] = grid[r_-1][c_]
                            for c_ in range(COLS):
                                grid[0][c_] = random.choice(colors)
                            # Add new color every 3 levels
                            if level % 3 == 0 and len(colors) < len(base_colors):
                                colors.append(base_colors[len(colors)])
                            # Add power-up and locked block
                            c_ = random.randint(0, COLS-1)
                            power_ups[(0, c_)] = random.choice(['bomb', 'swap', 'extra_moves'])
                            locked_blocks.add((0, random.randint(0, COLS-1)))
                        if not has_moves(grid) or moves_left <= 0:
                            game_over = True
                            if game_over_sound:
                                game_over_sound.play()
                    else:
                        score = max(0, score - 10)
                        time_limit = max(10, time_limit - 5)
        elif event.type == pygame.KEYDOWN and game_over:
            if event.key == pygame.K_r:
                grid = generate_grid()
                score = 0
                level = 1
                moves_left = 10
                bonus_time = 0
                time_limit = 120
                start_time = pygame.time.get_ticks() // 1000
                level_threshold = level * 500
                colors = base_colors[:4]
                game_over = False
                particles.clear()
                falling_blocks.clear()
                active_power_up = None
                swap_first = None

    # Update particles and falling blocks
    particles = [p for p in particles if p.lifetime > 0]
    for p in particles:
        p.update()
    falling_blocks = [fb for fb in falling_blocks if not fb.update()]

    # Draw game
    screen.fill((0, 0, 0))
    for r in range(ROWS):
        for c in range(COLS):
            colr = grid[r][c]
            if colr:
                rect = pygame.Rect(c * BLOCK_SIZE, r * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE)
                pygame.draw.rect(screen, colr, rect)
                pygame.draw.rect(screen, (255, 255, 255), rect, 1)
                if (r, c) in power_ups:
                    txt = font.render(power_ups[(r, c)][0].upper(), True, (255, 255, 0))
                    screen.blit(txt, (c * BLOCK_SIZE + 10, r * BLOCK_SIZE + 10))
                if (r, c) in locked_blocks:
                    pygame.draw.rect(screen, (128, 128, 128), rect, 3)
    for fb in falling_blocks:
        fb.draw(screen)
    for p in particles:
        p.draw(screen)

    # Timer and HUD
    current = pygame.time.get_ticks() // 1000
    time_left = time_limit + bonus_time - (current - start_time)
    if time_left <= 0 and not game_over:
        game_over = True
        if game_over_sound:
            game_over_sound.play()

    screen.blit(font.render(f'Score: {score}', True, (215, 55, 255)), (10, 10))
    screen.blit(font.render(f'Level: {level}', True, (215, 55, 255)), (10, 40))
    screen.blit(font.render(f'Moves: {moves_left}', True, (215, 55, 255)), (10, 70))
    screen.blit(font.render(f'Time: {time_left}', True, (215, 255, 55)), (250, 10))
    screen.blit(font.render(f'High Score: {high_score}', True, (215, 55, 255)), (250, 40))
    if active_power_up:
        screen.blit(font.render(f'Power-Up: {active_power_up}', True, (255, 255, 0)), (10, 100))

    # Game over display
    if game_over:
        if score > high_score:
            high_score = score
            with open(high_score_file, 'w') as f:
                f.write(str(high_score))
        go_txt = font.render('Game Over! Press R to Restart', True, (255, 0, 0))
        screen.blit(go_txt, (WIDTH // 2 - go_txt.get_width() // 2, HEIGHT // 2))

    pygame.display.flip()
    clock.tick(30)

pygame.quit()