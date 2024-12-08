import os
from datetime import datetime

import generation2
import pygame
import sys
from pyvidplayer2 import Video
from pygame import mixer

from hand_tracking import audio2

vid = Video("y2mate.com - Gogosi de post ca la gogoserie pufoase reteta care ti va face ziua mai buna_360p.mp4")
vid_alt = Video("Prajitura_Fanta_cu_suc_natural_de_portocale__prajitura_perf(1).mp4")
vidFoody2 = Video("gutui.mp4")
vidFoody3 = Video("radauteana.mp4")

tts_name = f"tts_{datetime.now().strftime('%y%m%d%H%M%S')}.mp3"

pygame.init()
mixer.init()


generate = 0

def music(check):
    if check == 1:
        mixer.music.unpause()
    else:
        mixer.music.pause()

# Screen dimensions
SCREEN_WIDTH = 640
SCREEN_HEIGHT = 480
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.RESIZABLE)
pygame.display.set_caption("Interactive Cooking Assistant")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

# Fonts
font = pygame.font.Font(None, 14)
font_large = pygame.font.Font(None, 20)



def parse_recipe(recipe: str):
    # Split the recipe into lines
    lines = recipe.splitlines()

    # Initialize variables to store ingredients and instructions
    ingredients = []
    instructions = []

    # Flags to determine the current section
    in_ingredients = False
    in_instructions = False

    # Iterate through the lines to categorize them
    for line in lines:
        line = line.strip()  # Remove leading/trailing whitespace
        if not line:  # Skip blank lines
            continue

        # Check for section headers
        if line.lower().startswith("**ingredients**"):
            in_ingredients = True
            in_instructions = False
            continue
        elif line.lower().startswith("**recipe**"):
            in_ingredients = False
            in_instructions = True
            continue

        # Add lines to the appropriate section
        if in_ingredients:
            ingredients.append(line)
        elif in_instructions:
            instructions.append(line)

    # Join the lists into strings
    ingredients_str = "\n".join(ingredients).strip()
    instructions_str = "\n".join(instructions).strip()

    return ingredients_str, instructions_str




def video(screen, x, y, width, height, draw, vidd):
    """
    Draw the video in a specific position and repeat it continuously.
    """
    # Update the video size if needed
    vidd.resize((width, height))

    if not draw:
        vidd.stop()
        return

    # Draw the video at the specified position
    if not vidd.active:
        vidd.restart()  # Restart the video if it ends
    vidd.draw(screen, (x, y), force_draw=True)


def misc():
    x_pot = 30
    y_pot = 320
    text = "Next Task"
    text_surface = font.render(text, True, BLACK)
    screen.blit(text_surface, (x_pot, y_pot))

    pygame.draw.circle(screen, RED, (135, 320), 40, 5)
    x_pot = 105
    y_pot = 320
    text = "Last Task"
    text_surface = font.render(text, True, BLACK)
    screen.blit(text_surface, (x_pot, y_pot))

    pygame.draw.circle(screen, GREEN, (220, 320), 40, 5)
    x_weight = 200
    y_weight = 310
    text = "Measure"
    text2 = "Quantity"
    text_surface = font.render(text, True, BLACK)
    screen.blit(text_surface, (x_weight, y_weight))
    text_surface = font.render(text2, True, BLACK)
    screen.blit(text_surface, (200, 300))

    pygame.draw.circle(screen, GREEN, (310, 320), 40, 5)
    text = "Go back"
    text_surface = font.render(text, True, BLACK)
    screen.blit(text_surface, (295, 310))

    circle_center = (50, 320)  # Center of the circle
    circle_radius = 40  # Radius of the circle
    pygame.draw.circle(screen, GREEN, circle_center, circle_radius, 5)



def display_ingredients(ingredients):
    """Display ingredients in the upper-left corner."""
    text = "Ingredient List:"
    text_surface = font.render(text, True, RED)
    screen.blit(text_surface, (50, 25))

    max_width = 300  # Maximum width for the text
    x_offset = 50
    y_offset = 50
    ingredients_list = ingredients.splitlines()

    for ingredient in ingredients_list:
        wrapped_lines = wrap_text(ingredient, font, max_width)
        for line in wrapped_lines:
            text = font.render(line, True, BLACK)
            screen.blit(text, (x_offset, y_offset))
            y_offset += 20  # Space between lines


def display_tasks(tasks):
    """Display tasks in the upper-right corner."""
    text = "Recipe Steps:"
    text_surface = font.render(text, True, RED)
    screen.blit(text_surface, (SCREEN_WIDTH - 350, 25))

    max_width = 300  # Maximum width for the text

    x_offset = SCREEN_WIDTH - 350
    y_offset = 50
    task_list = tasks.splitlines()

    for task in task_list:
        wrapped_lines = wrap_text(task, font, max_width)
        for line in wrapped_lines:
            text = font.render(line, True, BLACK)
            screen.blit(text, (x_offset, y_offset))
            y_offset += 20  # Space between lines


def display_ingredients_alt(foody = None):
    steps1 = ["500 g faina",
        "250 ml lapte",
        "50 g unt topit",
        "40 g zahar",
        "10 g drojdie uscata",
        "2 oua",
        "1 galbenus",
        "1 lingura esenta de vanilie",
        "coaja de la o lamaie",
        "putina sare" ]

    steps2 = ["5 pulpe de pui superioare"
" 2 gutui mari taiate in felii",
"4 linguri zahar",
" 4-5 linguri ulei",
"20 g amidon",
"1 lingurita boia",
"sare",
"piper"]

    steps3 = ["700 g carne de pui cu os",
"300 g smantana",
" 4 galbenusuri",
"2-3 linguri otet",
" 2 radacini mici de pastarnac",
" 2 cepe",
" 1 ardei gras",
" 1 morcov mare",
" 1 legatura patrunjel",
"1/2 telina",
"cativa catei de usturoi",
"foi de dafin",
"sare",
"piper"]

    if foody == 1:
        steps = steps1
    elif foody == 2:
        steps = steps2
    else: steps = steps3

    max_width = 300  # Maximum width for the text
    x_offset = 50
    y_offset = 50
    for ingredient in steps:
        wrapped_lines = wrap_text(ingredient, font, max_width)
        for line in wrapped_lines:
            text = font.render(line, True, BLACK)
            screen.blit(text, (x_offset, y_offset))
            y_offset += 20


def display_tasks_alt():
    """Display tasks in the upper-right corner."""
    text = "Recipe Steps:"
    text_surface = font.render(text, True, RED)
    screen.blit(text_surface, (SCREEN_WIDTH - 350, 25))

    max_width = 300  # Maximum width for the text

    x_offset = SCREEN_WIDTH - 350
    y_offset = 50
    task_list = ["1. Asigurați-vă că aluatul este moale, dar suplu. Adăugați o cantitate minimă de ulei și suficiente arome pentru un gust deosebit.",
        "2. Frământați aluatul bine, fie cu mâna, fie cu un mixer cu funcție de frământare. Nu vă îngrijorați dacă aluatul este moale – acest lucru este normal și va contribui la textura pufoasă a gogoșilor.",
        "3. Modelați aluatul în bile rotunde pe suprafața de lucru, astfel încât să aibă o formă uniformă și perfectă.",
        "4. Încălziți uleiul într-o tigaie adâncă, dar nu-l faceți excesiv de fierbinte. Prăjiți gogoșile la foc mediu pentru a permite o gătire uniformă, inclusiv în interior.",
        "5. Pudrați gogoșile cu zahăr sau umpleți-le cu creme sau gemuri după preferințe. Pentru o variantă delicioasă, încercați gogoșile umplute cu cremă de ciocolată.",
        "6. Bucurați-vă de cele mai bune gogoși pufoase, servindu-le calde alături de familie sau prieteni!"

    ]

    x_offset = SCREEN_WIDTH - 350
    y_offset = 50
    for task in task_list:
        wrapped_lines = wrap_text(task, font, max_width)
        for line in wrapped_lines:
            text = font.render(line, True, BLACK)
            screen.blit(text, (x_offset, y_offset))
            y_offset += 20  # Space between lines


def wrap_text(text, font, max_width):
    """Wrap text to fit within a specific width."""
    words = text.split(' ')
    lines = []
    current_line = []

    for word in words:
        current_line.append(word)
        # Render the line with the font to check its width
        line_width, _ = font.size(' '.join(current_line))
        if line_width > max_width:
            # If too wide, remove the last word and finalize the line
            current_line.pop()
            lines.append(' '.join(current_line))
            current_line = [word]

    # Add the last line
    if current_line:
        lines.append(' '.join(current_line))

    return lines


def draw_task(task, font, max_width, x, y, color, surface):
    """Draw a single task at the specified position on the given surface."""
    wrapped_lines = wrap_text(task, font, max_width)
    for line in wrapped_lines:
        text = font.render(line, True, color)
        surface.blit(text, (x, y))
        y += 20



def display_current_task(current_task_index, task_list, task_surface, transition=False):
    """
    Display the current task dynamically with the previous and next tasks, including a slide transition.
    Updates only the `task_surface` without affecting the rest of the screen.
    """
    max_width = 500
    task_surface.fill(WHITE)  # Clear only the task surface
    center_y = task_surface.get_height() // 2  # Center position for the current task on the surface
    previous_task_y = center_y - 40  # Position for the previous task
    next_task_y = center_y + 40  # Position for the next task

    # Calculate indices for previous and next tasks
    previous_task_index = (current_task_index - 1) % len(task_list)
    next_task_index = (current_task_index + 1) % len(task_list)

    if transition:
        # Transition animation: sliding effect
        for offset in range(50, 0, -5):  # Slide the tasks into view
            task_surface.fill(WHITE)  # Clear only the task surface

            # Draw the previous task sliding in
            draw_task(task_list[previous_task_index], font, max_width, 20, previous_task_y + offset, GREEN, task_surface)
            # Draw the current task sliding in
            draw_task(task_list[current_task_index], font, max_width, 20, center_y + offset, RED, task_surface)
            # Draw the next task sliding in
            draw_task(task_list[next_task_index], font, max_width, 20, next_task_y + offset, BLUE, task_surface)

            # Blit the task surface to the main screen
            screen.blit(task_surface, (50, SCREEN_HEIGHT - task_surface.get_height() - 10))
            pygame.display.flip()  # Update the display
            pygame.time.delay(30)  # Delay to control animation speed

    # Draw the previous, current, and next tasks on the surface
    draw_task(task_list[previous_task_index], font, max_width, 20, previous_task_y, GREEN, task_surface)
    draw_task(task_list[current_task_index], font, max_width, 20, center_y, RED, task_surface)
    draw_task(task_list[next_task_index], font, max_width, 20, next_task_y, BLUE, task_surface)

    # Blit the updated task surface to the main screen
    screen.blit(task_surface, (50, SCREEN_HEIGHT - task_surface.get_height() - 10))






def render_static_sections():
    """Render ingredients and tasks only once."""
    screen.fill(WHITE)  # Clear the screen
    #display_ingredients()
    #display_tasks()
    misc()




def render_main_screen(current_task_index, transition=False):
    """Render the main cooking assistant screen."""
    screen.fill(WHITE)  # Clear the screen

    # Create a surface for tasks (width: 500px, height: 120px)
    # task_surface = pygame.Surface((500, 120))
    #
    # # Render static sections
    # display_ingredients()
    # misc()
    # music(0)
    #
    # video_width, video_height = 300, 180
    # video(screen, x=SCREEN_WIDTH - video_width - 10, y=SCREEN_HEIGHT - 400,
    #       width=video_width, height=video_height, draw=True, vidd=vid_alt)
    #
    # # Render the current task on the task surface
    # task_list = tasks.splitlines()
    # display_current_task(current_task_index, task_list, task_surface, transition)

    global generate

    if generate == 0:

        if os.path.isfile("response.txt"):
            os.remove("response.txt")


        pygame.draw.rect(screen, GREEN, (240, 90, 180, 180), 5)
        write("Alege tu", 240 + 180 / 2 - 30, 90 + 180 / 2 - 15)
        pygame.display.flip()
        audio2.begin_gen_from_audio()

        text = open("response.txt", 'r')
        text = text.read()
        generation2.read_response_file("response.txt")

        generation2.generate_tts(text,
                                 tts_name)
        mixer.music.load(tts_name)

        mixer.music.set_volume(0.7)
        mixer.music.play()
        generate=1

    else:
        text = open("response.txt", 'r')
        music(1)
        task_surface = pygame.Surface((500, 120))
        ingredients, tasks = parse_recipe(text.read())

        # Render static sections
        display_ingredients(ingredients)
        misc()

        video_width, video_height = 300, 180
        video(screen, x=SCREEN_WIDTH - video_width - 10, y=SCREEN_HEIGHT - 400,
              width=video_width, height=video_height, draw=True, vidd=vid_alt)

        # Render the current task on the task surface
        task_list = tasks.splitlines()
        display_current_task(current_task_index, task_list, task_surface, transition)

    # Render the video in the bottom-right corner


def render_interface():
    screen.fill(WHITE)
    pygame.draw.circle(screen, GREEN, (160, 240), 80, 5)
    text = "Get a your own recipe idea :3"
    text_surface = font.render(text, True, BLACK)
    screen.blit(text_surface, (90, 240))

    pygame.draw.circle(screen, RED, (480, 240), 80, 5)
    text = "Pick from our catalogue"
    text_surface = font.render(text, True, BLACK)
    screen.blit(text_surface, (420, 240))
    music(0)



def write(text, x, y):
    text_surface = font_large.render(text, True, BLACK)
    screen.blit(text_surface, (x, y))

def render_prev_main():
    screen.fill(WHITE)
    pygame.draw.rect(screen, RED, (60, 60, 180, 90), 5)
    write("Gogosi Pufoase :P", 85, 105)
    pygame.draw.rect(screen, BLUE, (60, 180, 180, 90), 5)
    write("Mancare de gutui cu pui", 75, 225)
    pygame.draw.rect(screen, GREEN, (60, 300, 180, 90), 5)
    write("Ciorba radauteana", 85, 340)



def render_prev_alternate():
    screen.fill(WHITE)
   #RED, (60, 60, 90, 180), 5)

def render_alternate_screen(current_task_index, transition=False, foody = None):
    """Render the alternate screen."""
    # Clear the screen
    screen.fill(WHITE)
    music(0)
    task_surface = pygame.Surface((500, 120))

    # Create and update the video surface for the alternate screen
    video_width, video_height = 300, 180

    if foody == 1:
        videoUse = vid
    elif foody == 2:
        videoUse = vidFoody2
    else: videoUse = vidFoody3

    video(screen, x=SCREEN_WIDTH - video_width - 10, y=SCREEN_HEIGHT - 400,
          width=video_width, height=video_height, draw=True, vidd=videoUse)

    misc()
    # Render alternate elements (different text, primitives, and video)
    text = "Alternate Screen: Different Recipe"
    text_surface = font.render(text, True, BLACK)
    screen.blit(text_surface, (50, 30))


    # Alternate tasks and current task
    task_list_alt1 = [
    "1. Asigurați-vă că aluatul este moale, dar suplu. Adăugați o cantitate minimă de ulei și suficiente arome pentru un gust deosebit.",
    "2. Frământați aluatul bine, fie cu mâna, fie cu un mixer cu funcție de frământare. Nu vă îngrijorați dacă aluatul este moale – acest lucru este normal și va contribui la textura pufoasă a gogoșilor.",
    "3. Modelați aluatul în bile rotunde pe suprafața de lucru, astfel încât să aibă o formă uniformă și perfectă.",
    "4. Încălziți uleiul într-o tigaie adâncă, dar nu-l faceți excesiv de fierbinte. Prăjiți gogoșile la foc mediu pentru a permite o gătire uniformă, inclusiv în interior.",
    "5. Pudrați gogoșile cu zahăr sau umpleți-le cu creme sau gemuri după preferințe. Pentru o variantă delicioasă, încercați gogoșile umplute cu cremă de ciocolată.",
    "6. Bucurați-vă de cele mai bune gogoși pufoase, servindu-le calde alături de familie sau prieteni!",
    "7. Păstrați gogoșile rămase într-un recipient ermetic pentru a le menține proaspete și savurați-le mai târziu."
]

    task_list_alt2 = [
    "1. Alegeți și fierbeți legumele. Păstrați câteva bucăți de morcov pentru culoare, restul se pasează sau se aruncă.",
    "2. Amestecați smântâna cu gălbenușurile și adăugați treptat supă fierbinte, amestecând continuu.",
    "3. Nu turnați amestecul de smântână direct în ciorbă; temperați-l întâi.",
    "4. Răciți ciorba rapid: iarna afară, vara în apă rece, apoi puneți-o în frigider.",
    "5. Încălziți ciorba pe foc mic, fără să ajungă la fierbere, amestecând continuu.",
    "6. Serviți fierbinte cu ardei iute, pătrunjel, pâine, oțet sau usturoi după gust.",
    "7. Păstrați resturile de ciorbă în frigider și consumați-le în maximum 2 zile, încălzind doar porțiile necesare."
]

    task_list_alt3 = [
    "1. Rumeniți carnea de pui până devine aurie.",
    "2. Tăiați gutuile (cu coajă) în bucăți și rumeniți-le.",
    "3. Faceți un sos din zahăr caramelizat, apă și amidon.",
    "4. Puneți carnea, gutuile și sosul într-un vas. Coaceți 30 de minute.",
    "5. Pe aragaz, gătiți cu apă adăugată treptat.",
    "6. Presărați cimbru la final.",
    " 7. Serviți simplu sau cu orez."]

    if foody == 1:
        task_list_alt = task_list_alt1
    elif foody == 2:
        task_list_alt = task_list_alt3
    else: task_list_alt = task_list_alt2


    # Display alternate tasks and current task
    display_ingredients_alt(foody)
    display_current_task(current_task_index, task_list_alt, task_surface, transition)

    music(1)


