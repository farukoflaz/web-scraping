from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup

import tkinter as tk
import datetime
import pytz

#initializing the tk instance for the GUI
root = tk.Tk()
root.title("CROSSBREAKER")

#settings for webdriver 
driver = webdriver.Chrome("chromedriver.exe")

"""
This function reveal the answers for the puzzle by navigating on the web page
"""
def revealAnswers():
    #navigate to Ny Times mini crossword puzzle
    driver.get("https://www.nytimes.com/crosswords/game/mini")
    
    try: #It clicks on OK button if the "Ready to get started?" pops up 
        driver.find_element_by_xpath("/html/body/div[1]/div/div/div[4]/div/main/div[2]/div/div[2]/div[3]/div/article/div[2]/button/div/span").click()
    except Exception as e:
        print('nothing')

    try: #It clicks on the Play without account button
        driver.find_element_by_xpath("/html/body/div[1]/div/div/div[4]/div/main/div[2]/div/div[2]/div[3]/div/article/button").click()
    except Exception as e:
        print('nothing')    

    #It clicks on Reveal button
    driver.find_element_by_xpath("/html/body/div[1]/div/div/div[4]/div/main/div[2]/div/div/ul/div[2]/li[2]/button").click()
    #It clicks on Puzzle button
    driver.find_element_by_xpath("/html/body/div[1]/div/div/div[4]/div/main/div[2]/div/div/ul/div[2]/li[2]/ul/li[3]/a").click()
    #It clicks on Reveal button to accept
    driver.find_element_by_xpath("/html/body/div[1]/div/div[2]/div[2]/article/div[2]/button[2]/div/span").click()
    #It quits from the last pop up 
    driver.find_element_by_xpath("/html/body/div[1]/div/div[2]/div[2]/span").click()
   
"""
This function creates a grid structure for puzzle and places its elements on it
data: data obtained after scraping from website
"""
def create_grid(data):

    counter = 0
    for j in range(50,451,100):
        for i in range(10, 411, 100):
            
            if data[counter]['color'] == 0:
                c.create_rectangle(i,j,i+100,j+100, fill="black", outline="white")
                counter = counter +1

            else:
                c.create_rectangle(i,j,i+100,j+100, fill="white")
                c.create_text(i+15, j+15, text = data[counter]['number'], font=("nyt-franklin", 20))
                c.create_text(i+50, j+50, text = data[counter]['answerLetter'], font=("nyt-franklin", 47), fill="blue")
                counter = counter +1

    c.create_rectangle(10,50,510,550, width = 4)

    
"""
This function prints clue section of the puzzle
clueLabel: numbers belong to clues
clueText: texts of the clues
"""
def printClues(clueLabel, clueText):
    #starting point for printing clue section 
    x=545
    y=60

    for k in range (len(clueLabel)):
        if (k == 0 or k == 5):
            if (k == 0):
                c.create_text(x,y, text= "ACROSS", anchor= tk.W,font=("bold", 10))
                y+=40
            if (k == 5):
                y= 60
                x = 870
                c.create_text(x,y, text= "DOWN", anchor=tk.W, font=("bold", 10))
                y+=40
                
        c.create_text(x +15, y, text= clueLabel[k], anchor=tk.W)
            
        c.create_text(x + 30, y, text= clueText[k], anchor=tk.W, width=250)
        y += 40
        temp_y = y

        #lines under the ACROSS and DOWN
        c.create_line(545,75,820,75, fill= "black" )
        c.create_line(870,75,1145,75, fill= "black" )

"""
This function returns current time
"""        
def getCurrentTime():
    tzIS = pytz.timezone('Europe/Istanbul')
    currentTime = datetime.datetime.now(tzIS)
    time = str(currentTime) 
    return time        

"""
This function prints data & time and group nick
"""
def printIdentity():
    time = getCurrentTime()

    c.create_text(315,570,text= "Date & Time: "+time[:19],font=("nyt-franklin", 10), anchor=tk.W)
    c.create_text(315,585,text="Group nick: CROSSBREAKER",font=("nyt-franklin", 10), anchor=tk.W)

"""
This function divides and arranges the data obtained from the website after web scraping
and returns them into grid, clueLabels and clueTexts
boardContent: it contains data belong to the puzzle board
sectionLayoutClueList: it contains data belong to the clue section
"""    
def arrangeData(boardContent, sectionLayoutClueList):
    clueLabels = list()
    for clueLabel in sectionLayoutClueList.find_all('span', class_= 'Clue-label--2IdMY'):
      clueLabels.append(clueLabel.text)

    clueTexts = list()
    for clueText in sectionLayoutClueList.find_all('span', class_= 'Clue-text--3lZl7'):
      clueTexts.append(clueText.text)

    grid =list()

    for i in range(len(clueLabels)*len(clueLabels)):
      grid.append({'number': None,'color':None, 'answerLetter':None})

    for i, a in enumerate(boardContent.find_all('g')):
      if i == 3:    
        cells = a

    for i, b in enumerate(cells.find_all('g')):
      
      if b.rect['class'][0][:10] == 'Cell-block':
        grid[i]['color'] = 0  #if it is black
      else:
        grid[i]['color'] = 1  #if it is white
      
      try:
        if len(b.text) == 3:	
          grid[i]['number'] = b.text[0]
          grid[i]['answerLetter'] = b.text[1]
        else:
          grid[i]['answerLetter'] = b.text[0]    
      except Exception as e: 
        grid[i]['number'] = None
        grid[i]['answerLetter'] = None

    return grid, clueLabels, clueTexts

"""
main function
"""
def main():
    global c
    revealAnswers()

    #it gets page source of the webpage
    source= driver.page_source
    soup = BeautifulSoup(source, 'lxml')
    body = soup.body

    #it contains content of the puzzle board     
    boardContent = body.find('div', class_ = 'Board-boardContent--1AzTH').svg

    #it contains content of the clue section 
    sectionLayoutClueList = body.find('section', class_= 'Layout-clueLists--10_Xl')

    grid, clueLabels, clueTexts = arrangeData(boardContent, sectionLayoutClueList)

    c = tk.Canvas(root, height=650, width=1200, bg='white')
    c.pack(fill=tk.BOTH, expand=True)

    create_grid(grid)
    printClues(clueLabels,clueTexts)
    printIdentity()
    root.mainloop()

if __name__ == "__main__":
    main()
