import pygame
from constants import *
from resources import font20, font24, font36, font48, game_sounds, level_up_sound, screen
from shot import Shot

class ScoreBoard():

    def __init__(self,  lives = PLAYER_STARTING_LIVES, level = 1):
        self.score = 0
        self.lives = lives
        self.level = level
        self.level_score = 0

    def __render_game_over_line(self, font, text, bar_surface, colour, bar_w, bar_h, vertical_offset=0):
        text_surface = font.render(text, True, colour)
        text_rect = text_surface.get_rect(center=(bar_w / 2, bar_h / 2 + vertical_offset))
        bar_surface.blit(text_surface, text_rect)

    def __rect_surface(self, bar_w, bar_h, colour):
        bar_surface = pygame.Surface((bar_w, bar_h), pygame.SRCALPHA)  
        bar_surface.fill(colour)  
        return bar_surface

    def game_over(self):
        bar_w, bar_h = 400, 300
        bar_surface = self.__rect_surface(400, 300, (255, 255, 255, 100))
        self.__render_game_over_line(font48, f"Final score: {int(self.score)}", bar_surface, (150, 255, 150, 255), bar_w, bar_h, -110)
        self.__render_game_over_line(font48, f"GAME OVER", bar_surface, (255, 0, 0, 100), bar_w, bar_h - 55)
        self.__render_game_over_line(font48, f"Final level: {self.level}", bar_surface, (255, 255, 255, 0), bar_w, bar_h, 45)
        self.__render_game_over_line(font36, f"Press any key to continue", bar_surface, (0, 0, 0, 0), bar_w, bar_h, 120)
        screen.blit(bar_surface, ((SCREEN_WIDTH -bar_w)/ 2, (SCREEN_HEIGHT - bar_h) / 2))

    def __draw_shield_bar(self, player):

            # setup bar display parameters
            bar_width, bar_height = 180, 20  
            bar_x, bar_y = SCREEN_WIDTH - bar_width - 10, SCREEN_HEIGHT - bar_height - 10  # Bottom right corner with padding

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
            bar_surface = self.__rect_surface(bar_width, bar_height, bg_color)

            # Render the text set color to white below 50%
            if player.shield_charge < 50:
                text_color = (255, 255, 255)  # White
            else:
                text_color = (0, 0, 0)
            text_surface = font20.render(text, True, text_color)

            # Center the text on the bar
            text_rect = text_surface.get_rect(center=(bar_width / 2, bar_height / 2))
            bar_surface.blit(text_surface, text_rect)

            # Blit the bar onto the screen
            screen.blit(bar_surface, (bar_x, bar_y))    

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

    def update(self, player):
        score_text = font36.render(f"Score: {int(self.score)}", True, "green")
        lives_text = font36.render(f"Lives: {player.lives}", True, "green")
        level_text = font24.render(f"Level: {self.level}", True, "white")
        upgrades_text = font20.render(f"Active upgrades: {self.get_upgrades()}", True, "black", "white")

        screen.blit(score_text, (10, 10))
        screen.blit(lives_text, (10, 35))
        screen.blit(level_text, (10, 60))
        screen.blit(upgrades_text, (10, screen.get_height()-30))
        self.__draw_shield_bar(player)

    def get_upgrades(self):
        upgrades = []
        if Shot.piercing_active:
            upgrades.append("piercing bullets")
        if Shot.shot_size_multiplier > 1:
            upgrades.append(f"bullet size + {Shot.shot_size_multiplier-1}")
        return "none" if not upgrades else ", ".join(upgrades)
    
    