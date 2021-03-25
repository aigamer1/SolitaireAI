import os

class GameVals:
    cards = {}
    sliced_cards = {}
    borders = []

    # Variables related to screen size
    ScreenSize = "FullScreen"
    imageFolderName = 'Images'
    drawDeckArea = [300, 100, 800, 300]
    deckArea = [800, 100, 1600, 300]
    columnsStart = 375
    columnWidth = 150
    columnOffset = 170

    def __init__(self):

        if self.ScreenSize == "FullScreen":            
            self.imageFolderName = 'FullScreenImages'
            self.drawDeckArea = [300, 50, 800, 300]
            self.deckArea = [850, 50, 1600, 300]
            self.columnsStart = 325
            self.columnWidth = 175
            self.columnOffset = 182

        for i in range(1,5):
            borderName = 'border' + str(i) + '.png'
            self.borders.append(borderName)
        
        for i in range(1,14):
            for ch in ['c','d','h','s']:
                card = ch+str(i) 
                cardpath = os.path.join(os.getcwd(), self.imageFolderName, card + '.png') 
                sliceCardPath = os.path.join(os.getcwd(), self.imageFolderName, 'Slices', card + '.png') 
                self.cards[card] = cardpath     
                self.sliced_cards[card] = sliceCardPath
