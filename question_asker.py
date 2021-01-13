""" TO DO LIST:
-Think about the text files --> how to make them more convenient, how to explain how to write questions
"""

import random
import PySimpleGUI as ps

filePath = ""
allQuestionsPath = "../all_questions.txt"
saveFilePath = "../saved_questions.txt"
saveInput = "s"

GUITitle = "Question Asker"
textBg = "gray10"

ps.theme("DarkGreen3")

def readTextFile(filePath):
    QAList = []
    with open(filePath, "r") as f:
        while(True):
            curStr = f.readline()
            if curStr == "":
                break
            question = curStr.split("&")[0]
            answer = curStr.split("&")[1].strip()
            QAList.append((question, answer))
        return QAList


def saveQuestionsToTxt(saveList):
    textList = []
    for QA in saveList:
        textList.append(QA[0] + "& " + QA[1])
    with open(saveFilePath, "w") as f:
        for i in range(len(textList) - 1):
            f.write(textList[i] + "\n")
        f.write(textList[len(textList) - 1])
    
def removeQuestionsFromText(removeList):
    lines = []
    with open(filePath, "r") as f:
        lines = f.readlines()

    for QA in removeList:
        try:
            lines.remove(QA[0] + "& " + QA[1] + "\n")
        except:
            lines.remove(QA[0] + "& " + QA[1])

    lines[len(lines)-1].strip()
    with open(filePath, "w") as f:
        f.writelines(lines)
    


def askerMainLoop():
    invButtons = [[ps.Button("Save", size=(7, 2), font=("default", 15, "bold")), ps.Button("Remove", size=(7, 2), font=("default", 15, "bold"))]]
    askerLayout = [[ps.Text(size=(40, 1), key="-QA Text-", font=("default", 20, "bold"), border_width=10, background_color=textBg)],
                   [ps.Button("Next", size=(7, 2), font=("default", 15, "bold")), ps.Col(invButtons, key="-Inv Buttons-")]]
    window = ps.Window(GUITitle, askerLayout, finalize=True, no_titlebar=False, alpha_channel=1)

    QAList = readTextFile(filePath)
    saveList = []
    removeList = []
    while(True):
        window["-Inv Buttons-"].update(visible=False)

        QA = QAList[random.randint(0, len(QAList) - 1)]
        window["-QA Text-"].update(QA[0] + "  Q's: " + str(len(QAList)))
        event, values = window.read()
        while event != "Next":
            event, values = window.read()
            if event == ps.WINDOW_CLOSED:
                quit()
        
        window["-Inv Buttons-"].update(visible=True)
    
        window["-QA Text-"].update(QA[1])

        event, values = window.read()
        if event == ps.WINDOW_CLOSED:
            quit()
        elif event == "Save":
            saveList.append(QA)
        elif event == "Remove":
            removeList.append(QA)

        QAList.remove(QA)
        if(len(QAList) == 0):
            if(len(saveList) > 0):
                saveQuestionsToTxt(saveList)
            if(len(removeList) > 0):
                removeQuestionsFromText(removeList)
            break
    window.close()


def menuMainLoop():
    global filePath
    menuLayout = [[ps.Text("From which set do you want to see questions?", font=("default", 20, "bold"), border_width=10, background_color=textBg)],
                  [ps.Button("Saved Questions", size=(15, 2), font=("default", 15, "bold")), ps.Button("All Questions", size=(15, 2), font=("default", 15, "bold"))]]
    window = ps.Window(GUITitle, menuLayout, no_titlebar=False)
    event, values = window.read()
    if(event == ps.WINDOW_CLOSED):
        quit()
    elif(event == "Saved Questions"):
        filePath = saveFilePath
    elif(event == "All Questions"):
        filePath = allQuestionsPath
    window.close()


if __name__ == "__main__":
    while(True):
        menuMainLoop()
        askerMainLoop()
