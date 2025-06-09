#  Play scene - the main game play scene
from typing import List, Optional, Any
from pygame.locals import *
import pygame
import pygwidgets
import pyghelpers
from BaseScene import BaseScene
from Player import Player
from Baddies import BaddieMgr
from Goodies import GoodieMgr
from Constants import *

def showCustomYesNoDialog(theWindow, theText):
    oDialogBackground = pygwidgets.Image(theWindow, (40, 250),
                                            'images/dialog.png')
    oPromptDisplayText = pygwidgets.DisplayText(theWindow, (0, 290),
                                            theText, width=WINDOW_WIDTH,
                                            justified='center', fontSize=36)

    oYesButton = pygwidgets.CustomButton(theWindow, (320, 370),
                                            'images/gotoHighScoresNormal.png',
                                            over='images/gotoHighScoresOver.png',
                                            down='images/gotoHighScoresDown.png',
                                            disabled='images/gotoHighScoresDisabled.png')

    oNoButton = pygwidgets.CustomButton(theWindow, (62, 370),
                                            'images/noThanksNormal.png',
                                            over='images/noThanksOver.png',
                                            down='images/noThanksDown.png',
                                            disabled='images/noThanksDisabled.png')

    choiceAsBoolean = pyghelpers.customYesNoDialog(theWindow,
                                            oDialogBackground, oPromptDisplayText,
                                            oYesButton, oNoButton)
    return choiceAsBoolean

BOTTOM_RECT = (0, GAME_HEIGHT + 1, WINDOW_WIDTH,
                                WINDOW_HEIGHT - GAME_HEIGHT)

class GameState:
    WAITING = 'waiting'
    PLAYING = 'playing'
    GAME_OVER = 'game over'

class GameUI:
    def __init__(self, window: pygame.Surface):
        self.window = window
        self.controlsBackground = pygwidgets.Image(self.window, (0, GAME_HEIGHT), 'images/controlsBackground.jpg')
        self.quitButton = pygwidgets.CustomButton(self.window, (30, GAME_HEIGHT + 90),
                                                up='images/quitNormal.png',
                                                down='images/quitDown.png',
                                                over='images/quitOver.png',
                                                disabled='images/quitDisabled.png')
        self.highScoresButton = pygwidgets.CustomButton(self.window, (190, GAME_HEIGHT + 90),
                                                      up='images/gotoHighScoresNormal.png',
                                                      down='images/gotoHighScoresDown.png',
                                                      over='images/gotoHighScoresOver.png',
                                                      disabled='images/gotoHighScoresDisabled.png')
        self.newGameButton = pygwidgets.CustomButton(self.window, (450, GAME_HEIGHT + 90),
                                                   up='images/startNewNormal.png',
                                                   down='images/startNewDown.png',
                                                   over='images/startNewOver.png',
                                                   disabled='images/startNewDisabled.png',
                                                   enterToActivate=True)
        self.soundCheckBox = pygwidgets.TextCheckBox(self.window, (430, GAME_HEIGHT + 17),
                                                   'Background music', True, textColor=WHITE)
        self.gameOverImage = pygwidgets.Image(self.window, (140, 180), 'images/gameOver.png')
        self.titleText = pygwidgets.DisplayText(self.window, (70, GAME_HEIGHT + 17),
                                              'Score:                                 High Score:',
                                              fontSize=24, textColor=WHITE)
        self.scoreText = pygwidgets.DisplayText(self.window, (80, GAME_HEIGHT + 47), '0',
                                              fontSize=36, textColor=WHITE, justified='right')
        self.highScoreText = pygwidgets.DisplayText(self.window, (270, GAME_HEIGHT + 47), '',
                                                  fontSize=36, textColor=WHITE, justified='right')

    def draw(self, game_state: str) -> None:
        self.controlsBackground.draw()
        self.titleText.draw()
        self.scoreText.draw()
        self.highScoreText.draw()
        self.soundCheckBox.draw()
        self.quitButton.draw()
        self.highScoresButton.draw()
        self.newGameButton.draw()
        
        if game_state == GameState.GAME_OVER:
            self.gameOverImage.draw()

    def enable_buttons(self) -> None:
        self.newGameButton.enable()
        self.highScoresButton.enable()
        self.soundCheckBox.enable()
        self.quitButton.enable()

    def disable_buttons(self) -> None:
        self.newGameButton.disable()
        self.highScoresButton.disable()
        self.soundCheckBox.disable()
        self.quitButton.disable()

class GameAudio:
    def __init__(self):
        pygame.mixer.music.load('sounds/background.mid')
        self.dingSound = pygame.mixer.Sound('sounds/ding.wav')
        self.gameOverSound = pygame.mixer.Sound('sounds/gameover.wav')

    def play_background_music(self) -> None:
        pygame.mixer.music.play(-1, 0.0)

    def stop_background_music(self) -> None:
        pygame.mixer.music.stop()

    def play_ding(self) -> None:
        self.dingSound.play()

    def play_game_over(self) -> None:
        self.gameOverSound.play()

class ScenePlay(BaseScene):
    def __init__(self, window: pygame.Surface):
        super().__init__(window)
        self._ui = GameUI(window)
        self._audio = GameAudio()
        self._player = Player(window)
        self._baddie_mgr = BaddieMgr(window)
        self._goodie_mgr = GoodieMgr(window)
        
        self._highest_high_score = 0
        self._lowest_high_score = 0
        self._background_music = True
        self._score = 0
        self._playing_state = GameState.WAITING

    @property
    def score(self) -> int:
        return self._score

    @score.setter
    def score(self, value: int) -> None:
        self._score = value
        self._ui.scoreText.setValue(value)

    @property
    def playing_state(self) -> str:
        return self._playing_state

    @playing_state.setter
    def playing_state(self, value: str) -> None:
        self._playing_state = value

    def getSceneKey(self) -> str:
        return SCENE_PLAY

    def enter(self, data: Optional[Any] = None) -> None:
        self.get_high_scores()

    def get_high_scores(self) -> None:
        info_dict = self.request(SCENE_HIGH_SCORES, HIGH_SCORES_DATA)
        self._highest_high_score = info_dict['highest']
        self._ui.highScoreText.setValue(self._highest_high_score)
        self._lowest_high_score = info_dict['lowest']

    def reset(self) -> None:
        self.score = 0
        self.get_high_scores()
        
        self._baddie_mgr.reset()
        self._goodie_mgr.reset()

        if self._background_music:
            self._audio.play_background_music()
        
        self._ui.disable_buttons()
        pygame.mouse.set_visible(False)

    def handleInputs(self, eventsList: List[pygame.event.Event], keyPressedList: List[int]) -> None:
        if self._playing_state == GameState.PLAYING:
            return

        for event in eventsList:
            if self._ui.newGameButton.handleEvent(event):
                self.reset()
                self._playing_state = GameState.PLAYING

            if self._ui.highScoresButton.handleEvent(event):
                self.goToScene(SCENE_HIGH_SCORES)

            if self._ui.soundCheckBox.handleEvent(event):
                self._background_music = self._ui.soundCheckBox.getValue()

            if self._ui.quitButton.handleEvent(event):
                self.quit()

    def update(self) -> None:
        if self._playing_state != GameState.PLAYING:
            return

        mouseX, mouseY = pygame.mouse.get_pos()
        player_rect = self._player.update(mouseX, mouseY)

        n_goodies_hit = self._goodie_mgr.update(player_rect)
        if n_goodies_hit > 0:
            self._audio.play_ding()
            self.score += (n_goodies_hit * POINTS_FOR_GOODIE)

        n_baddies_evaded = self._baddie_mgr.update()
        self.score += (n_baddies_evaded * POINTS_FOR_BADDIE_EVADED)

        if self._baddie_mgr.hasPlayerHitBaddie(player_rect):
            self._handle_game_over()

    def _handle_game_over(self) -> None:
        pygame.mouse.set_visible(True)
        self._audio.stop_background_music()
        self._audio.play_game_over()
        self._playing_state = GameState.GAME_OVER
        self.draw()

        if self.score > self._lowest_high_score:
            self._handle_high_score()

        self._ui.enable_buttons()

    def _handle_high_score(self) -> None:
        score_string = f'Your score: {self.score}\n'
        if self.score > self._highest_high_score:
            dialog_text = score_string + 'is a new high score, CONGRATULATIONS!'
        else:
            dialog_text = score_string + 'gets you on the high scores list.'

        result = showCustomYesNoDialog(self.window, dialog_text)
        if result:
            self.goToScene(SCENE_HIGH_SCORES, self.score)

    def draw(self) -> None:
        self.window.fill(BLACK)
        
        self._baddie_mgr.draw()
        self._goodie_mgr.draw()
        self._player.draw()
        self._ui.draw(self._playing_state)

    def leave(self) -> Optional[Any]:
        self._audio.stop_background_music()
        return None
