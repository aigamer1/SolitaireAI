import time
import os
import sys
from imagesearch import *
import random
from Card import Card
from GameState import GameState
from Action import Action
from datetime import datetime
from game_vals import GameVals

random.seed(datetime.now())

class GameUI:
    time_delay=0.1
    gv = GameVals()
    gs = GameState()

    def __init__(self):
        self.findImgAndClick('CollapseMenuBtn.png')
        
    #######################################
    ### Helper Functions
    #######################################

    def focusOnEmulatorScreen(self):
        # Click inside the emulator screen to make sure it is in focus
        pyautogui.moveTo(300,575)
        pyautogui.mouseDown()
        pyautogui.mouseUp()

    def GetCardsFromRegion(self, x1, y1, x2, y2, precision = 0.90, caller = '', filterForSpecialCards = False):
        #print(caller)
        cardsRendered = []
        im = region_grabber((x1, y1, x2, y2))        
        #im.save('Debug_region.png')
        for crd,crdpath in self.gv.cards.items():
            #print(crd + ":" + crdpath)
            if filterForSpecialCards and int(crd[1:]) > 10:                
                precision = 0.90
            pos1 = imagesearcharea(crdpath, x1, y1, x2, y2, precision, im)
            if pos1[0] != -1:
                #print(crd + " detected")
                # TODO May be define a class for [card,pos_x,pos_y] tuple
                cardsRendered.append([crd,x1+pos1[0]+25,y1+pos1[1]+25])            
        return cardsRendered

    # y3 represents top portion of bottom most card in column
    def GetSlicedCardsFromRegion(self, x1, y1, x2, y2, y3, caller = ''):
        #print(caller)        
        #print("y3: " + str(y3))
        newy2 = y2
        if y3 != -1 and y3 > 400:
            newy2 = y3

        cardsRendered = []
        im = region_grabber((x1, y1, x2, newy2))        
        #im.save('debug_region.png')
        indOfLastRenderedCard = -1

        for crd,crdpath in self.gv.sliced_cards.items():
            #print(crd + ":" + crdpath)
            crdNumber = int(crd[1:])
            if crdNumber > 10:
                pos1 = imagesearcharea(crdpath, x1, y1, x2, y2, 0.90, im)
            else:
                pos1 = imagesearcharea(crdpath, x1, y1, x2, y2, 0.97, im)
            if pos1[0] != -1:
                # If we missed a card in sequence, keep trying to find it
                if indOfLastRenderedCard != -1 and crdNumber > indOfLastRenderedCard+1:
                    cardFound = False
                    tryCount = 0

                    while cardFound == False and tryCount < 3:
                        # Keep trying to search missing number card
                        for ch in ['s','c','d','h']:
                            crdToFind = ch + str(indOfLastRenderedCard+1)
                            crdCandidatePath = self.gv.sliced_cards[crdToFind]
                            if crdNumber > 10:
                                pos2 = imagesearcharea(crdCandidatePath, x1, y1, x2, y2, 0.90, im)
                            else:
                                pos2 = imagesearcharea(crdCandidatePath, x1, y1, x2, y2, 0.97, im)
                            if pos2[0] != -1:
                                cardsRendered.append([crd,x1+pos1[0]+25,y1+pos1[1]+25])
                                cardFound = True
                                break
                        if cardFound == False:
                            print("Could not find card with index:" + str(indOfLastRenderedCard+1) + ". Trying again...")
                            tryCount += 1

                    if cardFound == False:
                        print("Card not found.. Exiting")
                        exit(0)
                
                #print(crd + " detected")
                # TODO May be define a class for [card,pos_x,pos_y] tuple
                #print("Found card: " + crd)
                indOfLastRenderedCard = crdNumber
                cardsRendered.append([crd,x1+pos1[0]+25,y1+pos1[1]+25])  
                
        return cardsRendered

    def GetNewCardsInColumn(self, x1, y1, caller = ''):
        #print(caller)
        im = region_grabber((x1-30, y1-150, x1+120, y1-10))
        #im.save('debug_new_card.png')
        absolute_path = os.path.join(os.getcwd(), self.gv.imageFolderName, 'Slices','NewCardBorder.png')
        pos = imagesearcharea(absolute_path, x1-30, y1-150, x1+120, y1-10, 0.80, im)
        if pos[0] != -1:
            return True
        return False


    def findImgAndClick(self,imageName, precision = 0.90):
        absolute_path = os.path.join(os.getcwd(), self.gv.imageFolderName, imageName)
        pos = imagesearch(absolute_path, precision)
        if pos[0] != -1:
            click_image(absolute_path, pos, "left", 0, False, offset=5)
            return True
        return False

    def PressSolveBtn(self):
        im = region_grabber((300, 100, 800, 300))
        absolute_path = os.path.join(os.getcwd(), self.gv.imageFolderName, 'SolveBtn.png')
        pos1 = imagesearcharea(absolute_path, 300, 100, 800, 300, 0.90, im)
        if pos1[0] != -1:
            pyautogui.moveTo(300+pos1[0]+10,100+pos1[1]+10)
            pyautogui.mouseDown()
            pyautogui.mouseUp()
            exit(0)

    #######################################
    ### Main Functions
    #######################################

    def UpdateGameState(self):
        # Render game state

        self.focusOnEmulatorScreen()

        # If solve button exists, press it and exit                 
        self.PressSolveBtn()
        
        #############################
        # Capture top left draw deck
        #############################

        if "draw_deck" in self.gs.ui_components_to_render:
            self.gs.draw_deck_top_card.clear()  
            cardsRendered = self.GetCardsFromRegion(self.gv.drawDeckArea[0], self.gv.drawDeckArea[1],
             self.gv.drawDeckArea[2], self.gv.drawDeckArea[3], 0.95, "Capture Draw Deck", True)        
            if len(cardsRendered) > 0:
                self.gs.draw_deck_top_card = cardsRendered[0] 
            else:
                # Draw new card if possible
                print("Drawing a new card")
                self.findImgAndClick('draw_deck_card.png')
                time.sleep(1)
                cardsRendered = self.GetCardsFromRegion(self.gv.drawDeckArea[0], self.gv.drawDeckArea[1],
             self.gv.drawDeckArea[2], self.gv.drawDeckArea[3], 0.95, "Capture Draw Deck", True)        
                if len(cardsRendered) > 0:
                    self.gs.draw_deck_top_card = cardsRendered[0] 

        #########################
        # Capture top right area
        #########################

        if "top_deck" in self.gs.ui_components_to_render:
            self.gs.deck_cards_top.clear()
            cardsRendered = self.GetCardsFromRegion(self.gv.deckArea[0],self.gv.deckArea[1],self.gv.deckArea[2],self.gv.deckArea[3], 0.95, "Capture Deck")
            for crd in cardsRendered:
                self.gs.deck_cards_top.append(crd)

        #############################
        # Capture card columns
        #############################

        if "columns" in self.gs.ui_components_to_render:
            left = self.gv.columnsStart

            currColumnCards = []
            currColumnAllCards = []
            currNewCardsInColumn = []
            currEmptyColumnIndices = []            
            for ind in self.gs.empty_column_indices:
                currEmptyColumnIndices.append(ind)
            
            for i in range(0,7):
                if (i+1) not in self.gs.ui_components_to_render['columns']:
                    currColumnCards.append(self.gs.column_cards[i])
                    currColumnAllCards.append(self.gs.column_all_cards[i])
                    currNewCardsInColumn.append(self.gs.new_cards_in_column[i])
                else:
                    print("Rendering Column " + str(i+1))
                    cardsRendered = self.GetCardsFromRegion(left, 325, left+self.gv.columnWidth, 1050, 0.95, "Capture Column Cards", True)            
                    crdToAdd = []
                    if len(cardsRendered) > 0:
                        crdToAdd = cardsRendered[0]   
                    else:                        
                        if (i+1) not in currEmptyColumnIndices:
                            currEmptyColumnIndices.append(i+1)
                    currColumnCards.append(crdToAdd)
                    
                    # Render all sliced card in column
                    if len(crdToAdd) > 0:        
                        #print("crdtoadd:")
                        #print(crdToAdd)                      
                        slicedCardsRendered = self.GetSlicedCardsFromRegion(left, 325, left+self.gv.columnWidth, 1050, crdToAdd[2]-25, "Capture All Column Cards")
                        if len(slicedCardsRendered) > 0 and slicedCardsRendered[0][0] != crdToAdd[0]:
                            slicedCardsRendered.insert(0,crdToAdd)
                    else:
                        slicedCardsRendered = self.GetSlicedCardsFromRegion(left, 325, left+self.gv.columnWidth, 1050, -1, "Capture All Column Cards")

                    ColumnAllCardsToAdd = slicedCardsRendered
                    if len(slicedCardsRendered) == 0:
                        ColumnAllCardsToAdd = [crdToAdd]
                    currColumnAllCards.append(ColumnAllCardsToAdd)

                    if len(ColumnAllCardsToAdd[-1:][0]) > 0:
                        #print(ColumnAllCardsToAdd)
                        #print(ColumnAllCardsToAdd[-1:][0])
                        # Check if there are new cards in this column (flippable new cards)
                        NewCardExists = self.GetNewCardsInColumn(ColumnAllCardsToAdd[-1:][0][1],ColumnAllCardsToAdd[-1:][0][2])
                        if NewCardExists:
                            currNewCardsInColumn.append(1)
                        else:
                            currNewCardsInColumn.append(0)
                    else:
                        currNewCardsInColumn.append(0)
                left += self.gv.columnOffset

            self.gs.column_cards.clear()
            for crd in currColumnCards:
                self.gs.column_cards.append(crd)

            self.gs.empty_column_indices.clear()
            for crd in currEmptyColumnIndices:
                self.gs.empty_column_indices.append(crd)

            self.gs.column_all_cards.clear()
            for crd in currColumnAllCards:
                self.gs.column_all_cards.append(crd)

            self.gs.new_cards_in_column.clear()
            for crd in currNewCardsInColumn:
                self.gs.new_cards_in_column.append(crd)
    
        '''
        print("=====")
        print("ColumnCards:")
        print(self.gs.column_cards)
        print("=====")
        print("ColumnAllCards:")
        print(self.gs.column_all_cards)
        print("=====")
        print("NewCardsInColumn:")
        print(self.gs.new_cards_in_column)
        print("=====")
        print("DeckCards:")
        print(self.gs.deck_cards_top)
        print("=====")
        print("Draw deck card:")
        print(self.gs.draw_deck_top_card)
        print("=====")
        print("Empty Column Indices:")
        print(self.gs.empty_column_indices)
        '''
        return

    def ProcessAction(self, a):
        print("Processing action: " + a.name)
        print(a.cards)
        #return
        
        if a.name == 'DrawNewCard':
            if not self.findImgAndClick('draw_deck_card.png'):
                self.findImgAndClick('redraw_deck_card.png')
        elif a.name == 'MoveCardToDeck':
            print(a.cards[0])
            pyautogui.moveTo(a.cards[0][1],a.cards[0][2])
            pyautogui.mouseDown()
            pyautogui.mouseUp()
            pyautogui.mouseDown()
            pyautogui.mouseUp()
            time.sleep(0.5)
        elif a.name == 'MoveCardToColumn':            
            #print(a.cards)
            pyautogui.moveTo(a.cards[0][1]+50,a.cards[0][2]+50)
            pyautogui.mouseDown()
            pyautogui.mouseUp()            
            #time.sleep(1)

            indToGo = 0
            # If moving to empty column, process accordingly
            if a.cards[1][0] == 'empty_col':
                indToGo = a.cards[1][1]
            else:
                for crd in self.gs.column_cards:
                    indToGo += 1
                    if len(crd) > 0 and crd[0] == a.cards[1][0]:
                        break

            #print("Pressing key: " + str(indToGo))
            pyautogui.press(str(indToGo)) 
            #time.sleep(0.5)
            pyautogui.press('enter')
            time.sleep(0.5)
        

