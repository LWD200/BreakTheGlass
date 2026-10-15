# Imports
import pygame
import os
from os import listdir
from os.path import isfile, join
import math
import time
import random
from pathlib import Path

# Pygame Inits
pygame.font.init()
pygame.init()
pygame.mixer.init()

# Window Setup
WIDTH, HEIGHT = 1280, 720
pygame.init()
fullscreen = False
screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE | pygame.SCALED)
pygame.display.set_caption("LWD200 presents...")
ASSET_DIR = Path(__file__).resolve().parent / "assets"
VIDEO = ASSET_DIR / "Videos" / "Ending.mp4"

def toggle_fullscreen():
    global screen, fullscreen

    next_fullscreen = not fullscreen
    flags = pygame.SCALED | (pygame.FULLSCREEN if next_fullscreen else pygame.RESIZABLE)
    screen = pygame.display.set_mode((WIDTH, HEIGHT), flags)
    fullscreen = next_fullscreen

# Music Setup
music_enabled = True
sound_enabled = True
MUSIC_VOLUME = 0.3
pygame.mixer.music.load(ASSET_DIR / "Music" / "Music.wav")
pygame.mixer.music.set_volume(MUSIC_VOLUME)
pygame.mixer.music.play(-1)

# Sound Effects
JUMP_SFX = pygame.mixer.Sound(str(ASSET_DIR / "Music" / "jump.wav"))
BLOCK_FALL_SFX = pygame.mixer.Sound(str(ASSET_DIR / "Music" / "blockfall.wav"))

icon = pygame.image.load(str(ASSET_DIR / "Window" / "Image.jpg")).convert_alpha()
pygame.display.set_icon(icon)

# Background Setup
BG = pygame.transform.scale(
    pygame.image.load(str(ASSET_DIR / "Backgrounds" / "MenuBG.jpg")),
    (WIDTH, HEIGHT),
)

# GlowSquad27712
GLOW_HEIGHT = 300
GLOW = pygame.Surface((WIDTH, GLOW_HEIGHT), pygame.SRCALPHA)
for glow_y in range(GLOW_HEIGHT):
    glow_alpha = int(110 * (1 - glow_y / GLOW_HEIGHT))
    pygame.draw.line(GLOW, (0, 0, 0, glow_alpha), (0, glow_y), (WIDTH, glow_y))
pygame.draw.line(GLOW, (0, 0, 0, 255), (0, 0), (WIDTH, 0), 3)

# FreakingParticlesOmgggggg
PARTICLE_AREA_HEIGHT = 180
PARTICLE_SPAWN_INTERVAL = 0.04
PARTICLE_LAYER = pygame.Surface((WIDTH, PARTICLE_AREA_HEIGHT), pygame.SRCALPHA)
particles = []
particle_spawn_timer = 0

# Side Note - When editing numbers in terms of location on the screen
    # Bigger Number = Lower on screen + right
    # Smaller = Higher + Left

# Game Settings
PLAYER_WIDTH = 20
PLAYER_HEIGHT = 20
FPS = 60
VIDEO_FPS = 60
PLAYER_VEL = 5
GRAVITY = 1
JUMP_STRENGTH = -17 # Lower Number = Higher Jump -_-
GROUND_HEIGHT = 60
GROUND_Y = HEIGHT - GROUND_HEIGHT
FALLING_BLOCK_MIN_SIZE = 10
FALLING_BLOCK_MAX_SIZE = 75
FALLING_BLOCK_SPEED = 700
FALLING_BLOCK_SPAWN_INTERVAL = 1

# Instructions Message
INSTRUCTIONS_MESSAGE = "Reach the top. Break the glass."
INSTRUCTIONS_MESSAGE_DURATION = 10.0
INSTRUCTIONS_MESSAGE_FADE_DURATION = 2.0
instructions_message_timer = 0.0
INSTRUCTIONS_MESSAGE_LEFT = 30
INSTRUCTIONS_MESSAGE_BOTTOM = 15
INSTRUCTIONS_MESSAGE_MAX_WIDTH = WIDTH - 2 * INSTRUCTIONS_MESSAGE_LEFT
INSTRUCTIONS_MESSAGE_LINE_GAP = 6
INSTRUCTIONS_MESSAGE_FONT_SIZE = 20

# Death Animation
DEATH_ANIMATION_DURATION = 0.45
DEATH_PLAYER_COLOR = (0, 0, 0)
DEATH_BLOCK_COLOR = (255, 255, 255)

# Player Settings
player = pygame.Rect(
    (WIDTH - PLAYER_WIDTH) // 2,
    (HEIGHT - PLAYER_HEIGHT) // 2,
    PLAYER_WIDTH,
    PLAYER_HEIGHT,
)
player_vel_y = 0
on_ground = False

# Falling Blocks
falling_blocks = []
settled_blocks = []
spawn_timer = 0

# Menu/Button Visuals
FONT = pygame.font.SysFont("Arial", 60)
BUTTON_FONT = pygame.font.SysFont("Arial", 40)
INSTRUCTIONS_MESSAGE_FONT = pygame.font.SysFont("Arial", INSTRUCTIONS_MESSAGE_FONT_SIZE)
MENU_GAP = 30
BUTTON_WIDTH = 440
BUTTON_HEIGHT = 85
BUTTON_GAP = 18
MENU_BUTTON_COUNT = 4
MENU_CONTENT_HEIGHT = (
    FONT.get_height()
    + MENU_GAP
    + MENU_BUTTON_COUNT * BUTTON_HEIGHT
    + (MENU_BUTTON_COUNT - 1) * BUTTON_GAP
)
MENU_TOP = (HEIGHT - MENU_CONTENT_HEIGHT) // 2
MENU_BUTTONS = {
    label: pygame.Rect(
        (WIDTH - BUTTON_WIDTH) // 2,
        MENU_TOP + FONT.get_height() + MENU_GAP + index * (BUTTON_HEIGHT + BUTTON_GAP),
        BUTTON_WIDTH,
        BUTTON_HEIGHT,
    )
    for index, label in enumerate(("Play Game", "Settings", "Credits", "Quit Game"))
}
END_SCREEN_BUTTONS = {
    label: pygame.Rect(
        (WIDTH - BUTTON_WIDTH) // 2,
        HEIGHT // 2 - 10 + index * (BUTTON_HEIGHT + BUTTON_GAP),
        BUTTON_WIDTH,
        BUTTON_HEIGHT,
    )

    # Pause???
    for index, label in enumerate(("Replay", "Menu"))
}
PAUSE_BUTTONS = {
    label: pygame.Rect(
        (WIDTH - BUTTON_WIDTH) // 2,
        HEIGHT // 2 + 25 + index * (BUTTON_HEIGHT + BUTTON_GAP),
        BUTTON_WIDTH,
        BUTTON_HEIGHT,
    )
    for index, label in enumerate(("Resume", "Main Menu"))
}

# Back Button Settings
BACK_LABEL = "Back"
BACK_BUTTON_WIDTH = 260
BACK_BUTTON_HEIGHT = 75
BACK_BUTTON_X = (WIDTH - BACK_BUTTON_WIDTH) // 2
BACK_BUTTON_Y = HEIGHT - 300
BACK_BUTTON_POS = (BACK_BUTTON_X, BACK_BUTTON_Y)
BACK_BUTTON_SIZE = (BACK_BUTTON_WIDTH, BACK_BUTTON_HEIGHT)
SETTINGS_CONTENT_HEIGHT = (
    FONT.get_height()
    + MENU_GAP
    + 2 * BUTTON_HEIGHT
    + 2 * BUTTON_GAP
    + BACK_BUTTON_HEIGHT
)
SETTINGS_CONTENT_TOP = (HEIGHT - SETTINGS_CONTENT_HEIGHT) // 2
SETTINGS_MUSIC_BUTTON_RECT = pygame.Rect(
    (WIDTH - BUTTON_WIDTH) // 2,
    SETTINGS_CONTENT_TOP + FONT.get_height() + MENU_GAP,
    BUTTON_WIDTH,
    BUTTON_HEIGHT,
)
SETTINGS_SOUND_BUTTON_RECT = pygame.Rect(
    (WIDTH - BUTTON_WIDTH) // 2,
    SETTINGS_MUSIC_BUTTON_RECT.bottom + BUTTON_GAP,
    BUTTON_WIDTH,
    BUTTON_HEIGHT,
)
SETTINGS_BACK_BUTTON_RECT = pygame.Rect(
    BACK_BUTTON_X,
    SETTINGS_SOUND_BUTTON_RECT.bottom + BUTTON_GAP,
    BACK_BUTTON_WIDTH,
    BACK_BUTTON_HEIGHT,
)
CREDITS_BACK_BUTTON_RECT = pygame.Rect(
    BACK_BUTTON_X,
    BACK_BUTTON_Y + 150,
    BACK_BUTTON_WIDTH,
    BACK_BUTTON_HEIGHT,
)

# Player Visuals
PLAYER_IMAGE = pygame.transform.scale(
    pygame.image.load(str(ASSET_DIR / "Player" / "cube_1.png")).convert_alpha(),
    (PLAYER_WIDTH, PLAYER_HEIGHT),
)

# Menu Button
def draw_button(label, rect, mouse_pos):
    button_color = (39, 214, 245) if rect.collidepoint(mouse_pos) else (70, 136, 232)
    text = BUTTON_FONT.render(label, True, (0, 0, 0))
    pygame.draw.rect(screen, button_color, rect, border_radius=16)
    screen.blit(text, text.get_rect(center=rect.center))

# Do you see me in the videoooooooooooooooooooooooooooooooooooooooooooooooooooooo?
def open_Ending_video():
    try:
        import cv2
    except ModuleNotFoundError as error:
        if error.name != "cv2":
            raise
        print("Cannot play the Ending video: install opencv-python to enable MP4 playback.")
        return None

    capture = cv2.VideoCapture(str(VIDEO))
    if not capture.isOpened():
        capture.release()
        print(f"Cannot open Ending video: {VIDEO}")
        return None

    success, frame = capture.read()
    if not success:
        capture.release()
        print(f"Cannot read Ending video: {VIDEO}")
        return None

    success, next_frame = capture.read()
    if not success:
        next_frame = frame.copy()

    fps = capture.get(cv2.CAP_PROP_FPS)
    frame_interval = 1 / fps if math.isfinite(fps) and fps > 0 else 1 / FPS
    return capture, frame, next_frame, frame_interval


# Main Menu Screen
def draw_menu(mouse_pos):
    screen.blit(BG, (0, 0))

    title = FONT.render("Break The Glass", True, (0, 0, 0))
    screen.blit(title, title.get_rect(center=(WIDTH // 2, MENU_TOP + FONT.get_height() // 2)))
    for label, rect in MENU_BUTTONS.items():
        draw_button(label, rect, mouse_pos)

# Settings/Credits Screens
def draw_info_screen(title_text, message, mouse_pos, back_label=BACK_LABEL, back_rect=None):
    if back_rect is None:
        back_rect = SETTINGS_BACK_BUTTON_RECT

    screen.blit(BG, (0, 0))
    title = FONT.render(title_text, True, (255, 255, 255))
    message_lines = [message] if isinstance(message, str) else message
    line_height = BUTTON_FONT.get_linesize()
    paragraph_gap = BUTTON_GAP
    title_gap = MENU_GAP
    message_height = len(message_lines) * line_height + max(0, len(message_lines) - 1) * paragraph_gap
    content_height = title.get_height() + title_gap + message_height
    horizontal_padding = 24
    vertical_padding = 20
    content_width = max(
        title.get_width(),
        *(BUTTON_FONT.size(line)[0] for line in message_lines),
    )
    panel_size = (
        content_width + 2 * horizontal_padding,
        content_height + 2 * vertical_padding,
    )
    panel_top = (back_rect.top - panel_size[1]) // 2
    panel = pygame.Surface(panel_size, pygame.SRCALPHA)
    pygame.draw.rect(panel, (0, 0, 0, 175), panel.get_rect(), border_radius=12)
    screen.blit(panel, panel.get_rect(midtop=(WIDTH // 2, panel_top)))
    content_top = panel_top + vertical_padding
    screen.blit(title, title.get_rect(midtop=(WIDTH // 2, content_top)))
    message_y = content_top + title.get_height() + title_gap
    for index, line in enumerate(message_lines):
        message_text = BUTTON_FONT.render(line, True, (255, 255, 255))
        screen.blit(
            message_text,
            message_text.get_rect(
                midtop=(WIDTH // 2, message_y + index * (line_height + paragraph_gap))
            ),
        )
    draw_button(back_label, back_rect, mouse_pos)

# Settings Settings
def draw_settings_screen(mouse_pos):
    screen.blit(BG, (0, 0))
    title = FONT.render("Settings", True, (0, 0, 0))
    screen.blit(title, title.get_rect(midtop=(WIDTH // 2, SETTINGS_CONTENT_TOP)))
    draw_button(
        f"Music: {'On' if music_enabled else 'Off'}",
        SETTINGS_MUSIC_BUTTON_RECT,
        mouse_pos,
    )
    draw_button(
        f"Sound: {'On' if sound_enabled else 'Off'}",
        SETTINGS_SOUND_BUTTON_RECT,
        mouse_pos,
    )
    draw_button(BACK_LABEL, SETTINGS_BACK_BUTTON_RECT, mouse_pos)

# Instructions Message Rendering
def draw_instructions_message(alpha):
    message_lines = []
    for paragraph in INSTRUCTIONS_MESSAGE.splitlines():
        if not paragraph.strip():
            message_lines.append("")
            continue

        current_line = ""
        for word in paragraph.split():
            candidate = f"{current_line} {word}".strip()
            if current_line and INSTRUCTIONS_MESSAGE_FONT.size(candidate)[0] > INSTRUCTIONS_MESSAGE_MAX_WIDTH:
                message_lines.append(current_line)
                current_line = word
            else:
                current_line = candidate
        if current_line:
            message_lines.append(current_line)
    if not message_lines:
        message_lines.append("")

    line_height = INSTRUCTIONS_MESSAGE_FONT.get_linesize()
    message_height = len(message_lines) * line_height + (len(message_lines) - 1) * INSTRUCTIONS_MESSAGE_LINE_GAP
    message_top = HEIGHT - INSTRUCTIONS_MESSAGE_BOTTOM - message_height
    for index, line in enumerate(message_lines):
        text = INSTRUCTIONS_MESSAGE_FONT.render(line, True, (255, 255, 255))
        text.set_alpha(alpha)
        text_rect = text.get_rect(
            topleft=(
                INSTRUCTIONS_MESSAGE_LEFT,
                message_top + index * (line_height + INSTRUCTIONS_MESSAGE_LINE_GAP),
            ),
        )
        screen.blit(text, text_rect)

# Reset Game
def reset_game():
    global player_vel_y, on_ground, spawn_timer, particle_spawn_timer, instructions_message_timer

    player.midbottom = (WIDTH // 2, GROUND_Y)
    player_vel_y = 0
    on_ground = True
    falling_blocks.clear()
    settled_blocks.clear()
    spawn_timer = 0
    particles.clear()
    particle_spawn_timer = 0
    instructions_message_timer = INSTRUCTIONS_MESSAGE_DURATION

# The Actual Game Loop
def main():
    run = True
    state = "menu"
    paused_screen = None
    clock = pygame.time.Clock()
    frame_time = 1 / FPS
    video_capture = None
    video_previous_frame = None
    video_next_frame = None
    video_surface = None
    ending_background = None
    video_frame_interval = 1 / FPS
    video_frame_timer = 0
    death_animation_timer = 0

    global player_vel_y, on_ground, falling_blocks, settled_blocks, spawn_timer
    global particles, particle_spawn_timer, instructions_message_timer
    global music_enabled, sound_enabled

    while run:
        # Inputs + Window
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_F11:
                    toggle_fullscreen()
                elif event.key == pygame.K_r and state in (
                    "playing", "death_animation", "game_over", "won", "Ending_video"
                ): # Reset
                    if video_capture is not None:
                        video_capture.release()
                        video_capture = None
                        video_previous_frame = None
                        video_next_frame = None
                        video_surface = None
                    reset_game()
                    state = "playing"
                elif state == "menu" and event.key == pygame.K_SPACE:
                    reset_game()
                    state = "playing"
                elif state == "game_over" and event.key == pygame.K_SPACE:
                    reset_game()
                    state = "playing"
                elif state == "game_over" and event.key == pygame.K_ESCAPE:
                    state = "menu"
                elif state == "won" and event.key == pygame.K_SPACE:
                    reset_game()
                    state = "playing"
                elif state == "won" and event.key == pygame.K_ESCAPE:
                    state = "menu"
                elif state == "Ending_video" and event.key == pygame.K_ESCAPE:
                    video_capture.release()
                    video_capture = None
                    video_previous_frame = None
                    video_next_frame = None
                    video_surface = None
                    state = "menu"
                elif state in ("settings", "credits") and event.key == pygame.K_ESCAPE:
                    state = "menu"
                elif state == "playing" and event.key == pygame.K_ESCAPE:
                    paused_screen = screen.copy()
                    state = "paused"
                elif state == "paused" and event.key == pygame.K_ESCAPE:
                    state = "playing"
                elif state == "menu" and event.key == pygame.K_ESCAPE:
                    run = False
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if state == "menu":
                    for label, rect in MENU_BUTTONS.items():
                        if rect.collidepoint(event.pos):
                            if label == "Quit Game":
                                run = False
                                break
                            state = {
                                "Play Game": "playing",
                                "Settings": "settings",
                                "Credits": "credits",
                            }[label]
                            if state == "playing":
                                reset_game()
                            break
                elif state == "settings":
                    if SETTINGS_MUSIC_BUTTON_RECT.collidepoint(event.pos):
                        music_enabled = not music_enabled
                        if music_enabled:
                            pygame.mixer.music.unpause()
                        else:
                            pygame.mixer.music.pause()
                    elif SETTINGS_SOUND_BUTTON_RECT.collidepoint(event.pos):
                        sound_enabled = not sound_enabled
                        if sound_enabled:
                            pygame.mixer.unpause()
                        else:
                            pygame.mixer.pause()
                    elif SETTINGS_BACK_BUTTON_RECT.collidepoint(event.pos):
                        state = "menu"
                elif state == "credits" and CREDITS_BACK_BUTTON_RECT.collidepoint(event.pos):
                    state = "menu"
                elif state == "paused":
                    if PAUSE_BUTTONS["Resume"].collidepoint(event.pos):
                        state = "playing"
                    elif PAUSE_BUTTONS["Main Menu"].collidepoint(event.pos):
                        state = "menu"
                elif state in ("game_over", "won"):
                    if END_SCREEN_BUTTONS["Replay"].collidepoint(event.pos):
                        reset_game()
                        state = "playing"
                    elif END_SCREEN_BUTTONS["Menu"].collidepoint(event.pos):
                        state = "menu"

        # Updates While Playing
        if state == "playing":
            instructions_message_timer = max(0, instructions_message_timer - frame_time)
            keys = pygame.key.get_pressed()

            # Particles
            particle_spawn_timer += frame_time
            while particle_spawn_timer >= PARTICLE_SPAWN_INTERVAL:
                lifetime = random.uniform(0.8, 1.5)
                particles.append({
                    "x": random.uniform(0, WIDTH),
                    "y": 3,
                    "vx": random.uniform(-22, 22),
                    "vy": random.uniform(35, 95),
                    "life": lifetime,
                    "max_life": lifetime,
                    "radius": random.randint(2, 4),
                })
                particle_spawn_timer -= PARTICLE_SPAWN_INTERVAL

            PARTICLE_LAYER.fill((0, 0, 0, 0))
            for particle in particles[:]:
                particle["x"] += particle["vx"] * frame_time
                particle["y"] += particle["vy"] * frame_time
                particle["life"] -= frame_time
                if particle["life"] <= 0 or particle["y"] >= PARTICLE_AREA_HEIGHT:
                    particles.remove(particle)
                    continue
                alpha = int(255 * particle["life"] / particle["max_life"])
                pygame.draw.circle(
                    PARTICLE_LAYER,
                    # Particle Color
                    (0, 0, 0, alpha),
                    (round(particle["x"]), round(particle["y"])),
                    particle["radius"],
                )

            # Spawn Blocks
            spawn_timer += frame_time
            while spawn_timer >= FALLING_BLOCK_SPAWN_INTERVAL:
                size = random.randint(FALLING_BLOCK_MIN_SIZE, FALLING_BLOCK_MAX_SIZE)
                x = random.randint(0, WIDTH - size)
                falling_blocks.append(pygame.Rect(x, -size, size, size))
                if sound_enabled:
                    BLOCK_FALL_SFX.play()
                spawn_timer -= FALLING_BLOCK_SPAWN_INTERVAL

            for block in falling_blocks[:]:
                next_y = block.y + FALLING_BLOCK_SPEED * frame_time
                next_bottom = next_y + block.height

                if (
                    player_vel_y >= 0
                    and block.left < player.right
                    and block.right > player.left
                    and block.bottom <= player.top <= next_bottom
                ):
                    death_animation_timer = 0
                    state = "death_animation"
                    break

                landing_y = GROUND_Y
                for settled in settled_blocks:
                    if (
                        block.left < settled.right
                        and block.right > settled.left
                        and block.bottom <= settled.top <= next_bottom
                    ):
                        landing_y = min(landing_y, settled.top)

                if next_bottom >= landing_y:
                    block.bottom = landing_y
                    falling_blocks.remove(block)
                    settled_blocks.append(block)
                else:
                    block.y = round(next_y)

            if state == "playing":

                # Move Controls
                solid_blocks = falling_blocks + settled_blocks
                move_x = int(keys[pygame.K_RIGHT] or keys[pygame.K_d]) - int(
                    keys[pygame.K_LEFT] or keys[pygame.K_a]
                )
                old_left = player.left
                old_right = player.right
                player.x += move_x * PLAYER_VEL

                for block in solid_blocks:
                    if player.colliderect(block):
                        if move_x > 0:
                            player.right = block.left
                        elif move_x < 0:
                            player.left = block.right
                        elif old_right <= block.left:
                            player.right = block.left
                        elif old_left >= block.right:
                            player.left = block.right
                player.x = max(0, min(player.x, WIDTH - player.width))

                # Jump + Gravity
                if (keys[pygame.K_UP] or keys[pygame.K_w] or keys[pygame.K_SPACE]) and on_ground:
                    player_vel_y = JUMP_STRENGTH
                    on_ground = False
                    if sound_enabled:
                        JUMP_SFX.play()

                player_vel_y += GRAVITY
                player.y += player_vel_y
                on_ground = False

                # I hate collisions
                if player_vel_y >= 0:
                    for block in solid_blocks:
                        if player.colliderect(block):
                            player.bottom = block.top
                            player_vel_y = 0
                            on_ground = True
                    if player.bottom >= GROUND_Y:
                        player.bottom = GROUND_Y
                        player_vel_y = 0
                        on_ground = True
                else:
                    for block in solid_blocks:
                        if player.colliderect(block):
                            player.top = block.bottom
                            player_vel_y = 0
                            break

                # Win/Won/End/Yay
                if player.top <= 0:
                    player.top = 0
                    player_vel_y = 0
                    ending_background = None
                    if VIDEO.is_file():
                        video = open_Ending_video()
                        if video is not None:
                            (
                                video_capture,
                                video_previous_frame,
                                video_next_frame,
                                video_frame_interval,
                            ) = video
                            video_frame_timer = 0
                            state = "Ending_video"
                        else:
                            state = "won"
                    else:
                        state = "won"

            # Rendering BG, Ground, And Blocks (And Color)
            screen.fill((255, 255, 255))
            screen.blit(GLOW, (0, 0))
            screen.blit(PARTICLE_LAYER, (0, 0))
            for block in falling_blocks + settled_blocks:
                pygame.draw.rect(screen, (0, 0, 0), block) # Block Color
            pygame.draw.rect(screen, (0, 0, 0), (0, GROUND_Y, WIDTH, GROUND_HEIGHT)) # Ground Color

            # Ending Screen Text
            if player_vel_y <= 0:
                title = FONT.render("You broke the glass!", True, (255, 255, 255))

            # Game Over Screen + Player Rynder
            if state == "playing":
                screen.blit(PLAYER_IMAGE, player)
                if instructions_message_timer > 0:
                    message_elapsed = INSTRUCTIONS_MESSAGE_DURATION - instructions_message_timer
                    fade_in = min(1.0, message_elapsed / INSTRUCTIONS_MESSAGE_FADE_DURATION)
                    fade_out = min(1.0, instructions_message_timer / INSTRUCTIONS_MESSAGE_FADE_DURATION)
                    message_alpha = round(255 * min(fade_in, fade_out))
                    draw_instructions_message(message_alpha)
        elif state == "death_animation":
            # Death Animation
            death_animation_timer += frame_time
            progress = min(death_animation_timer / DEATH_ANIMATION_DURATION, 1)
            player_tint = tuple(
                round(255 + (DEATH_PLAYER_COLOR[channel] - 255) * progress)
                for channel in range(3)
            )
            block_color = tuple(
                round(DEATH_BLOCK_COLOR[channel] * progress) for channel in range(3)
            )
            # Game Imaging
            screen.fill((255, 255, 255))
            screen.blit(GLOW, (0, 0))
            screen.blit(PARTICLE_LAYER, (0, 0))
            for block in falling_blocks + settled_blocks:
                pygame.draw.rect(screen, block_color, block)
            pygame.draw.rect(screen, (0, 0, 0), (0, GROUND_Y, WIDTH, GROUND_HEIGHT))
            tinted_player = PLAYER_IMAGE.copy()
            tinted_player.fill(player_tint, special_flags=pygame.BLEND_RGB_MULT)
            screen.blit(tinted_player, player)

            if death_animation_timer >= DEATH_ANIMATION_DURATION:
                state = "game_over"
        elif state == "Ending_video":

            # Increase FPS
            video_frame_timer += frame_time
            while video_frame_timer >= video_frame_interval and state == "Ending_video":
                video_frame_timer -= video_frame_interval
                success, frame = video_capture.read()
                if not success:
                    import cv2

                    final_rgb_frame = cv2.cvtColor(video_next_frame, cv2.COLOR_BGR2RGB)
                    final_frame_surface = pygame.image.frombuffer(
                        final_rgb_frame.tobytes(),
                        (final_rgb_frame.shape[1], final_rgb_frame.shape[0]),
                        "RGB",
                    ).copy()
                    ending_background = pygame.transform.smoothscale(
                        final_frame_surface, (WIDTH, HEIGHT)
                    )
                    video_capture.release()
                    video_capture = None
                    video_previous_frame = None
                    video_next_frame = None
                    state = "won"
                    break


                video_previous_frame = video_next_frame
                video_next_frame = frame
            if state == "Ending_video":
                import cv2

                blend = video_frame_timer / video_frame_interval
                frame = cv2.addWeighted(
                    video_previous_frame, 1 - blend, video_next_frame, blend, 0
                )
                rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                frame_size = (frame.shape[1], frame.shape[0])
                video_surface = pygame.image.frombuffer(rgb_frame.tobytes(), frame_size, "RGB").copy()
                screen.blit(pygame.transform.smoothscale(video_surface, (WIDTH, HEIGHT)), (0, 0))
       
        # Text Editing
        elif state == "game_over":
            screen.blit(BG, (0, 0))
            title = FONT.render("Game Over", True, (0, 0, 0))
            screen.blit(title, title.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 90)))
            for label, rect in END_SCREEN_BUTTONS.items():
                draw_button(label, rect, pygame.mouse.get_pos())
        elif state == "won":
            screen.blit(ending_background if ending_background is not None else BG, (0, 0))
            title = FONT.render("You broke the glass!", True, (255, 255, 255))
            title_rect = title.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 90))
            title_background = pygame.Surface(title_rect.inflate(32, 20).size, pygame.SRCALPHA)
            pygame.draw.rect(
                title_background,
                (0, 0, 0, 175),
                title_background.get_rect(),
                border_radius=12,
            )
            screen.blit(title_background, title_background.get_rect(center=title_rect.center))
            screen.blit(title, title_rect)
            for label, rect in END_SCREEN_BUTTONS.items():
                draw_button(label, rect, pygame.mouse.get_pos())
        elif state == "paused":
            screen.blit(paused_screen, (0, 0))
            pause_overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
            pause_overlay.fill((0, 0, 0, 160))
            screen.blit(pause_overlay, (0, 0))
            title = FONT.render("Paused", True, (255, 255, 255))
            screen.blit(title, title.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 70)))
            for label, rect in PAUSE_BUTTONS.items():
                draw_button(label, rect, pygame.mouse.get_pos())
        elif state == "menu":
            draw_menu(pygame.mouse.get_pos())

        # Settings and Credits Screen
        elif state == "settings":
            draw_settings_screen(pygame.mouse.get_pos())
        else:
            draw_info_screen(
                "Credits",
                [
                    "Made with Python/Pygame in Visual Studio Code by LWD200",
                    "Code by LWD200",
                    "Animations made in Geometry Dash by LWD200",
                    "Art by LWD200",
                    "Music and SFX by LWD200",
                ],
                pygame.mouse.get_pos(),
                back_label=BACK_LABEL,
                back_rect=CREDITS_BACK_BUTTON_RECT,
            )

        # FPS :3
        pygame.display.flip()
        target_fps = VIDEO_FPS if state == "Ending_video" else FPS
        frame_time = min(clock.tick(target_fps) / 1000, 0.05)

    # Exit Game / End
    if video_capture is not None:
        video_capture.release()
    pygame.quit()

# Idk ima be real, but this is necessary
if __name__ == "__main__":
    main()