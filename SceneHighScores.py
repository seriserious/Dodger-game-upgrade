# High Scores scene
from typing import List, Optional, Any
import pygame
import pygwidgets
import pyghelpers
from BaseScene import BaseScene
from HighScoresData import HighScoresData
from Constants import *

def showCustomAnswerDialog(theWindow: pygame.Surface, theText: str) -> Optional[str]:
    oDialogBackground = pygwidgets.Image(theWindow, (35, 450), 'images/dialog.png')
    oPromptDisplayText = pygwidgets.DisplayText(theWindow, (0, 480), theText,
                                              width=WINDOW_WIDTH,
                                              justified='center', fontSize=36)
    oUserInputText = pygwidgets.InputText(theWindow, (200, 550), '',
                                        fontSize=36, initialFocus=True)
    oNoButton = pygwidgets.CustomButton(theWindow, (65, 595),
                                      'images/noThanksNormal.png',
                                      over='images/noThanksOver.png',
                                      down='images/noThanksDown.png',
                                      disabled='images/noThanksDisabled.png')
    oYesButton = pygwidgets.CustomButton(theWindow, (330, 595),
                                       'images/addNormal.png',
                                       over='images/addOver.png',
                                       down='images/addDown.png',
                                       disabled='images/addDisabled.png')
    userAnswer = pyghelpers.customAnswerDialog(theWindow,
                                            oDialogBackground,
                                            oPromptDisplayText, oUserInputText,
                                            oYesButton, oNoButton)
    return userAnswer

def showCustomResetDialog(theWindow: pygame.Surface, theText: str) -> bool:
    oDialogBackground = pygwidgets.Image(theWindow, (35, 450), 'images/dialog.png')
    oPromptDisplayText = pygwidgets.DisplayText(theWindow, (0, 480), theText,
                                              width=WINDOW_WIDTH,
                                              justified='center', fontSize=36)
    oNoButton = pygwidgets.CustomButton(theWindow, (65, 595),
                                      'images/cancelNormal.png',
                                      over='images/cancelOver.png',
                                      down='images/cancelDown.png',
                                      disabled='images/cancelDisabled.png')
    oYesButton = pygwidgets.CustomButton(theWindow, (330, 595),
                                       'images/okNormal.png',
                                       over='images/okOver.png',
                                       down='images/okDown.png',
                                       disabled='images/okDisabled.png')
    choiceAsBoolean = pyghelpers.customYesNoDialog(theWindow,
                                                oDialogBackground, oPromptDisplayText,
                                                oYesButton, oNoButton)
    return choiceAsBoolean

class SceneHighScores(BaseScene):
    def __init__(self, window: pygame.Surface):
        super().__init__(window)
        self._high_scores_data = HighScoresData()
        
        self._background_image = pygwidgets.Image(self.window, (0, 0),
                                                'images/highScoresBackground.jpg')

        self._names_field = pygwidgets.DisplayText(self.window, (260, 84), '',
                                                fontSize=48, textColor=BLACK,
                                                width=300, justified='left')
        self._scores_field = pygwidgets.DisplayText(self.window, (25, 84), '',
                                                  fontSize=48, textColor=BLACK,
                                                  width=175, justified='right')

        self._quit_button = pygwidgets.CustomButton(self.window, (30, 650),
                                                  up='images/quitNormal.png',
                                                  down='images/quitDown.png',
                                                  over='images/quitOver.png',
                                                  disabled='images/quitDisabled.png')

        self._back_button = pygwidgets.CustomButton(self.window, (240, 650),
                                                  up='images/backNormal.png',
                                                  down='images/backDown.png',
                                                  over='images/backOver.png',
                                                  disabled='images/backDisabled.png')

        self._reset_scores_button = pygwidgets.CustomButton(self.window, (450, 650),
                                                          up='images/resetNormal.png',
                                                          down='images/resetDown.png',
                                                          over='images/resetOver.png',
                                                          disabled='images/resetDisabled.png')

        self.show_high_scores()

    def getSceneKey(self) -> str:
        return SCENE_HIGH_SCORES

    def enter(self, new_high_score_value: Optional[int] = None) -> None:
        if new_high_score_value is None:
            return

        self.draw()
        dialog_question = (f'To record your score of {new_high_score_value},\n'
                         'please enter your name:')
        player_name = showCustomAnswerDialog(self.window, dialog_question)
        
        if player_name is None:
            return

        if player_name == '':
            player_name = 'Anonymous'
            
        self._high_scores_data.addHighScore(player_name, new_high_score_value)
        self.show_high_scores()

    def show_high_scores(self) -> None:
        scores_list, names_list = self._high_scores_data.getScoresAndNames()
        self._names_field.setValue(names_list)
        self._scores_field.setValue(scores_list)

    def handleInputs(self, eventsList: List[pygame.event.Event], keyPressedList: List[int]) -> None:
        for event in eventsList:
            if self._quit_button.handleEvent(event):
                self.quit()
            elif self._back_button.handleEvent(event):
                self.goToScene(SCENE_PLAY)
            elif self._reset_scores_button.handleEvent(event):
                confirmed = showCustomResetDialog(self.window,
                                               'Are you sure you want to \nRESET the high scores?')
                if confirmed:
                    self._high_scores_data.resetScores()
                    self.show_high_scores()

    def update(self) -> None:
        pass

    def draw(self) -> None:
        self._background_image.draw()
        self._scores_field.draw()
        self._names_field.draw()
        self._quit_button.draw()
        self._reset_scores_button.draw()
        self._back_button.draw()

    def leave(self) -> Optional[Any]:
        return None

    def respond(self, requestID: str) -> Optional[dict]:
        if requestID == HIGH_SCORES_DATA:
            highest_score, lowest_score = self._high_scores_data.getHighestAndLowest()
            return {'highest': highest_score, 'lowest': lowest_score}
        return None
