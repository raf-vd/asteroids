import pygame
from constants import *
from functions import rect_surface, render_line
from gamedata import highscores
from resources import font20, font24, font36, font48, game_sounds, level_up_sound, surface

class ScoreBoard():

    def __init__(self,  lives = PLAYER_STARTING_LIVES, level = 1):
        self.score = 0
        self.lives = lives
        self.level = level
        self.level_score = 0

    def game_over(self, win=False, name=""):
        condition = "VICTORY" if win else "GAME OVER"
        bar_surface = rect_surface(400, 300, (255, 255, 255, 100))
        render_line(font48, f"Final score: {int(self.score)}", bar_surface, (150, 255, 150, 255), 50)
        render_line(font48, f"{condition}", bar_surface, (255, 0, 0, 100), 125)

        if self.is_highscore(name):
            self.player_name_box(bar_surface, name)

        render_line(font48, f"Final level: {self.level}", bar_surface, (255, 255, 255, 0), 200)
        render_line(font36, f"Press ESC to continue", bar_surface, (0, 0, 0, 0), bar_surface.get_height() - 25)
        surface.blit(bar_surface, ((SCREEN_WIDTH - bar_surface.get_width()) / 2, (SCREEN_HEIGHT - bar_surface.get_height()) / 2))

    def __draw_shield_bar(self, player):

            # setup bar display parameters
            bar_width, bar_height = 180, 20  
            bar_x, bar_y = SCREEN_WIDTH - bar_width - 10, 10  # Top right corner

            # Determine the background color and text based on the shield's state
            if player.shield_charge == 0:
                bg_color = (255, 0, 0, 255)  # Solid red, fully opaque
                text = "SHIELD DEPLETED"
            elif player.shield_charge == 100:
                bg_color = (150, 250, 150, 255)  # Solid green, fully opaque
                text = "SHIELD FULLY LOADED"
            else:
                # Semi-transparent green for intermediate shield strength
                alpha = int(255 * (player.shield_charge / 100))  # Transparency depends on strength
                bg_color = (150, 255, 150, alpha)
                if player.non_hit_scoring_streak >= PLAYER_MIN_SCORE_STREAK:
                    text = f"Shield: {player.shield_charge:.1f}% (+{player.shield_regeneration:.3f})"
                else:
                    text = f"Shield: {player.shield_charge:.1f}%"

            # Prepare a surface for the bar
            bar_surface = rect_surface(bar_width, bar_height, bg_color)

            # Render the text set color to white below 50%
            if player.shield_charge < 50:
                text_color = (255, 255, 255)  # White
            else:
                text_color = (0, 0, 0)
            text_surface = font20.render(text, True, text_color)

            # Center the text on the bar
            text_rect = text_surface.get_rect(center=(bar_width / 2, bar_height / 2))
            bar_surface.blit(text_surface, text_rect)

            # Blit the bar onto the surface
            surface.blit(bar_surface, (bar_x, bar_y))    

    def add(self, value = 1): # If new level is reached, return True, if notn return False
        self.score += value
        self.level_score += value
        if self.level_score >= LEVEL_UP_VALUE:
            self.__level_up()
            return True
        return False

    def __level_up(self, value = 1):
        self.level += value
        self.level_score = 0
        if game_sounds.get_busy: game_sounds.stop()
        game_sounds.play(level_up_sound)

    def __get_upgrades(self, player):
        upgrades = []
        if player.piercing_active():
            upgrades.append("piercing bullets")
        if player.shot_size_multiplier() > 1:
            upgrades.append(f"bullet size + {player.shot_size_multiplier()-1}")
        return "none" if not upgrades else ", ".join(upgrades)

    def update(self, player):
        score_text = font36.render(f"Score: {int(self.score)}", True, "green")
        lives_text = font36.render(f"Lives: {player.lives}", True, "green")
        level_text = font24.render(f"Level: {self.level}", True, "white")
        upgrades_text = font20.render(f"Active upgrades: {self.__get_upgrades(player)}", True, "black", "white")

        surface.blit(score_text, (10, 10))
        surface.blit(lives_text, (10, 35))
        surface.blit(level_text, (10, 60))
        surface.blit(upgrades_text, (10, SCREEN_HEIGHT-30))
        self.__draw_shield_bar(player)
    
    def is_highscore(self, name):
        if int(self.score) > list(highscores.settings.values())[-1]:
            if highscores.settings.get(name) != int(self.score):                                             # Score for this player already saved, only allow player 1x in highscore
                return True
        return False

    def player_name_box(self, bar_surface, name_so_far=""):
        input_surface = rect_surface(185, 30, (0, 0, 0, 255))                                           # Create a surface for the box
        input_surface.fill((0, 0, 0))                                                                   # Make it black
        pygame.draw.rect(input_surface, "green", input_surface.get_rect(), 1)                           # Give it a border
        text_width, _ = font24.size(name_so_far)                                                        # Get cursor position
        current_time = pygame.time.get_ticks()                                                          # Cursor timer variable
        if (current_time // 500) % 2:                                                                   # Blinks every 500ms
            pygame.draw.line(input_surface, "white", (5 + text_width, 5), (5 + text_width, 25))         # Draw cursor
        bar_surface.blit(font24.render("Enter name for highcore", True, (255,255,0)), (5, 152))         # Show msg
        input_surface.blit(font24.render(name_so_far, True, (255,255,255)), (5, 6))                     # Show currently typed in name
        bar_surface.blit(input_surface, (205, 145))                                                     # Blit it all to target surface
                    