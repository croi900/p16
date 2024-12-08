import os
import threading

import pygame
import sys
from pyvidplayer2 import Video
from pygame import mixer
from scipy.interpolate import interp1d

import render
import socket
import struct

# Set up the server details
UDP_IP = "192.168.34.119"  # Localhost
UDP_PORT = 5000       # Port number

# Create a UDP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Bind to the address
sock.bind((UDP_IP, UDP_PORT))



# create video object
os.environ['SDL_VIDEO_WINDOW_POS'] = "0,0"
os.environ['SDL_VIDEO_CENTERED'] = '0'

win = pygame.display.set_mode((640,480))
pygame.display.set_caption(render.vid.name)

# Initialize Pygame
pygame.init()
mixer.init()

mixer.music.load("tts.mp3")
mixer.music.set_volume(0.7)
mixer.music.play()


def music(check):
    if check == 1:
        mixer.music.unpause()
    else:
        mixer.music.pause()


# Screen dimensions
SCREEN_WIDTH = 640
SCREEN_HEIGHT = 480
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Interactive Cooking Assistant")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

# Fonts
font = pygame.font.Font(None, 14)


# Sample data for the recipe
distance = 16
mconv = interp1d([0,20.80],[200,0],bounds_error=False,fill_value=0)
def read_dist():
    global distance
    while True:

        data, addr = sock.recvfrom(4)  # Buffer size is 1024 bytes
        float_value = struct.unpack('f', data)[0]
        print(float_value)
        distance = mconv(float_value)

def main():

    threading.Thread(target=read_dist, daemon=True).start()

    global screen

    current_task_index = 0
    alt_index = 0
    running = True
    screenType = 0

    # State variable to track the current screen
    #current_screen = "main" if screenType == 0 else "alternate"

    if screenType == 0:
        current_screen = "interface"
    elif screenType == 1:
        current_screen = "main"
    else:
        current_screen = "alternate"


    # Define the clickable circle region
    circle_center = (50, 320)  # Center of the circle
    circle_radius = 40  # Radius of the circle

    circileircle_center = (135, 320)
    circileircle_radius = 40

    interface_l = (160, 240)
    interface_lc = 40

    interface_r = (480, 240)
    interface_rc = 40


    rect1_top = 60
    rect1_bottom = 150
    rect1_right = 240
    rect1_left = 60


    rect2_top = 180
    rect2_bottom = 270
    rect2_right = 240
    rect2_left = 60

    rect3_top = 300
    rect3_bottom = 390
    rect3_right = 240
    rect3_left = 60

    cback_center = (295, 310)
    cback_radius = 40

    rectp_top = 80
    rectp_bottom = 260
    rectp_right = 630
    rectp_left = 330

    video_paused = True

    while running:
        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                running = False
                render.vid.stop()  # Stop the video when quitting

            # Handle mouse clicks
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.math.Vector2(event.pos)  # Get the position of the mouse click
                circle_distance = pygame.math.Vector2(circle_center).distance_to(mouse_pos)
                circileircle_distance = pygame.math.Vector2(circileircle_center).distance_to(mouse_pos)
                interface_rd = pygame.math.Vector2(interface_r).distance_to(mouse_pos)
                interface_ld = pygame.math.Vector2(interface_l).distance_to(mouse_pos)
                cback_d = pygame.math.Vector2(cback_center).distance_to(mouse_pos)

                if rect1_left <= mouse_pos.x <= rect1_right and rect1_top <= mouse_pos.y <= rect1_bottom:
                    if current_screen == "prev_main":
                        current_screen = "main"
                        foody = 1
                        #render.render_prev_main()

                if rect2_left <= mouse_pos.x <= rect2_right and rect2_top <= mouse_pos.y <= rect2_bottom:
                    if current_screen == "prev_main":
                        current_screen = "main"
                        foody = 2

                if rect3_left <= mouse_pos.x <= rect3_right and rect3_top <= mouse_pos.y <= rect3_bottom:
                    if current_screen == "prev_main":
                        current_screen = "main"
                        foody = 3



                if rectp_left <= mouse_pos.x <= rectp_right and rectp_top <= mouse_pos.y <= rectp_bottom:
                    if current_screen == "main":
                        video_paused = not video_paused
                        if video_paused:
                            render.vid.pause()
                            render.vidFoody3.pause()
                            render.vidFoody2.pause()
                        else:
                            render.vid.resume()
                            render.vidFoody3.resume()
                            render.vidFoody2.resume()


                if cback_d <= cback_radius:
                    if current_screen == "main" or current_screen == "alternate":
                        current_screen = "interface"
                        render.generate = 0
                if interface_rd <= interface_rc:
                    if current_screen == "interface":
                        current_screen = "prev_main"
                        #render.render_prev_main()

                if interface_ld <= interface_lc:
                    if current_screen == "interface":
                        current_screen = "alternate"
                        #current_task_index = (current_task_index + 1) % len(
                            #render.tasks.splitlines())
                        #render.render_prev_alternate()


                # Check if the click was within the circle
                if circle_distance <= circle_radius:
                    # Increment the current task based on the current screen

                    if current_screen == "main":
                        current_task_index = (current_task_index + 1) % len(render.tasks.splitlines())
                        render.render_alternate_screen(current_task_index, transition=True, foody = foody)
                    elif current_screen == "alternate":
                        alt_index = (alt_index + 1) % 6
                        render.render_main_screen(alt_index, transition=True)

                if circileircle_distance <= circileircle_radius:
                    if current_screen == "main":
                        current_task_index = (current_task_index - 1) % len(render.tasks.splitlines())
                        render.render_alternate_screen(current_task_index, transition=True, foody=foody)
                    elif current_screen == "alternate":
                        alt_index = (alt_index - 1) % 6
                        render.render_main_screen(alt_index, transition=True)


        if (current_screen == "interface"):
            render.render_interface()
            render.vid.stop()
            render.vidFoody3.stop()
            render.vidFoody2.stop()
        # Update the video surfaces
        elif current_screen == "main":

            #video(screen, x=0, y=0, width=300, height=180, draw=True, vidd=vid)
            render.render_alternate_screen(current_task_index, foody = foody)
            render.write(f"Weight: {distance}",532,32)

            # Blit the clickable region
            pygame.draw.circle(screen, BLUE, circle_center, circle_radius, 5)
        elif current_screen == "alternate":
            #video(screen, x=0, y=0, width=300, height=200, draw=True, vidd=vid_alt)

            render.render_main_screen(alt_index)
            render.write(f"Weight: {distance}",532,32)

            # Blit the clickable region

        elif current_screen == "prev_main":
            render.render_prev_main()
        elif current_screen == "prev_alternate":
            render.render_prev_alternate()


        pygame.display.flip()  # Update the display

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
