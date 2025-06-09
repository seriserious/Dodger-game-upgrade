# Splash scene - first scene the user sees
from typing import List, Optional, Any
import pygame
import pygwidgets
import pyghelpers
from BaseScene import BaseScene
from Constants import *

class SceneSplash(BaseScene):
    def __init__(self, window: pygame.Surface):
        super().__init__(window)
        self._background_image = pygwidgets.Image(self.window, (0, 0), 'images/splashBackground.jpg')
        self._dodger_image = pygwidgets.Image(self.window, (150, 30), 'images/dodger.png')
        
        self._start_button = pygwidgets.CustomButton(self.window, (250, 500),
                                                   up='images/startNormal.png',
                                                   down='images/startDown.png',
                                                   over='images/startOver.png',
                                                   disabled='images/startDisabled.png',
                                                   enterToActivate=True)

        self._quit_button = pygwidgets.CustomButton(self.window, (30, 650),
                                                  up='images/quitNormal.png',
                                                  down='images/quitDown.png',
                                                  over='images/quitOver.png',
                                                  disabled='images/quitDisabled.png')

        self._high_scores_button = pygwidgets.CustomButton(self.window, (360, 650),
                                                         up='images/gotoHighScoresNormal.png',
                                                         down='images/gotoHighScoresDown.png',
                                                         over='images/gotoHighScoresOver.png',
                                                         disabled='images/gotoHighScoresDisabled.png')

    def getSceneKey(self) -> str:
        return SCENE_SPLASH

    def enter(self, data: Optional[Any] = None) -> None:
        pass

    def handleInputs(self, eventsList: List[pygame.event.Event], keyPressedList: List[int]) -> None:
        for event in eventsList:
            if self._start_button.handleEvent(event):
                self.goToScene(SCENE_PLAY)
            elif self._quit_button.handleEvent(event):
                self.quit()
            elif self._high_scores_button.handleEvent(event):
                self.goToScene(SCENE_HIGH_SCORES)

    def update(self) -> None:
        pass

    def draw(self) -> None:
        self._background_image.draw()
        self._dodger_image.draw()
        self._start_button.draw()
        self._quit_button.draw()
        self._high_scores_button.draw()

    def leave(self) -> Optional[Any]:
        return None
