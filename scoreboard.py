import pygame
from constants import *
from shot import Shot

class ScoreBoard():

    def __init__(self,  lives = 1, level = 1):
        self.score = 0
        self.lives = lives
        self.level = level
        self.level_score = 0
        self.font36 = pygame.font.Font(None, 36)
        self.font24 = pygame.font.Font(None, 24)
        self.font20 = pygame.font.Font(None, 20)

    # If new level is reached, return True, if notn return False
    def add(self, value = 1):
        self.score += value
        self.level_score += value
        if self.level_score >= LEVEL_UP_VALUE:
            self.__level_up()
            return True
        return False

    def lose_life(self, value = 1):
        self.lives -= value

    def __level_up(self, value = 1):
        self.level += value
        self.level_score = 0
        print(f"Level up by {value} to level {self.level}!")

    def update(self, screen):
        score_text = self.font36.render(f"Score: {int(self.score)}", True, "green")
        lives_text = self.font36.render(f"Lives: {self.lives}", True, "green")
        level_text = self.font24.render(f"Level: {self.level}", True, "white")
        upgrades_text = self.font20.render(f"Active upgrades: {self.get_upgrades()}", True, "black", "white")

        screen.blit(score_text, (10, 10))
        screen.blit(lives_text, (10, 35))
        screen.blit(level_text, (10, 60))
        screen.blit(upgrades_text, (10, screen.get_height()-30))

    def get_upgrades(self):
        upgrades = []
        if Shot.piercing_active:
            upgrades.append("piercing bullets")
        if Shot.shot_size_multiplier > 1:
            upgrades.append(f"bullet size + {Shot.shot_size_multiplier-1}")
        return "none" if not upgrades else ", ".join(upgrades)