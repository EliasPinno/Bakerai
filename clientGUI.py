import tkinter as tk
import tkinter.ttk as ttk
import main as m

FONT = ("Verdana",12)
TITLE_FONT = ("Verdana",16)
# Based off of my own application in Tkinter previously
class bakerClient(tk.Tk):
    def __init__(self,*args,**kwargs):
        tk.Tk.__init__(self,*args,**kwargs)
        # Set title and good inital window size
        tk.Tk.wm_title(self, "BakerAI")
        self.geometry("1000x700")

        # Container is parent frame, containing all frames
        parent = tk.Frame(self)
        parent.pack(side="top",fill="both",expand=True)
        # Format: min size, weight is z index
        parent.grid_rowconfigure(0, weight=1)
        parent.grid_columnconfigure(0, weight=1)
        # Main frame layout: where content is stored 
        mainFrame = tk.Frame(parent)
        mainFrame.pack(side="top",fill="both",expand=True)
        for i in range(9):
            mainFrame.grid_rowconfigure(index=i, weight=1)
            mainFrame.grid_columnconfigure(index=i, weight=1)
        self.loaded_clf = m.load_sentiment_analysis()[0]

        # Create the language map
        self.languages = {"English": "en", "Français": "fr", "Русский": "ru", "Español": "es", "Suomi": "fi"}
        
        # Elements of the main frame #
        # Title
        title = tk.Label(mainFrame, text="Welcome to Sakura's very own BakerAI!", font=TITLE_FONT)
        title.grid(row=1,column=1,columnspan=7)
        # What we will change to show output
        self.outputBox = tk.Text(mainFrame, font=FONT)
        self.outputBox.grid(row=3, column=1, columnspan=7, rowspan=1, sticky="")
        self.outputBox.insert(tk.END,"BakerAI: Hey there! How can I help you? \n")
        self.outputBox.configure(state="disabled")
        scrollbar = tk.Scrollbar(self)
        scrollbar.config(command = self.outputBox.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.outputBox.config(yscrollcommand=scrollbar.set)

        # Input related items
        entryLabel = tk.Label(mainFrame, text="Enter your text below!", font=FONT)
        entryLabel.grid(row=4, column=2, columnspan=2, sticky="")
        self.userInput = tk.Entry(mainFrame)
        self.userInput.grid(row=5, column=1, columnspan=4, sticky="EW")
        sendButton = tk.Button(mainFrame, text="Send message", command=lambda: self.getResponse())
        sendButton.grid(row=5, column=6, columnspan=1, sticky="EW")
        self.userInput.bind("<Return>", lambda x: self.getResponse())
        # Language selector
        optionList = list(self.languages.keys())
        self.lan = tk.StringVar()
        self.lan.set(optionList[0]) # Set the current language to english
        self.lanSelection = tk.OptionMenu(mainFrame, self.lan,  *optionList)
        self.lanSelection.grid(row=5, column = 7, columnspan=1, sticky="EW")

    def getResponse(self):
        # Get user message
        userMessage = self.userInput.get()
        # Language is usable forms
        shortLan = self.languages[self.lan.get()]
        # Ignore empty messages
        if userMessage == "":
            return
        # Clear the user input
        self.userInput.delete(0, "end")
        # Check if the wiki command is in the chat
        if "wiki " == userMessage.lower()[0:5]:
            # Send user message without the wiki portion    
            wikiReply = self.wikiResponse(userMessage[5:], shortLan) 
            self.addExchange(userMessage, wikiReply)
            return
        
        # Translate input to english to send to our bot
        userEnglish = m.translate(userMessage, shortLan, 'en')
        # Get our reply
        reply = m.getFinalOutput(self.loaded_clf,userEnglish)
        # Translate reply to proper language
        replyLan = "BakerAI: " + m.translate(reply, 'en', shortLan) + "\n"
        self.addExchange(userMessage,replyLan)

    
    def wikiResponse(self, userMessage, lan):
        m.setWikiLan(lan)
        topResult, summary = m.getTopSearch(userMessage)
        outputStr = f'Are you talking about {topResult.title}? Here is what I know about this based on wikipedia. \nA link to the page is: {topResult.url}\nHere is the first 3 sentences of the summary:\n{summary}'
        return outputStr 
    
    def addExchange(self, userStr, botStr):
        # Append who is speaking to the string
        userStr = f'You: {userStr}\n'
        botStr = f'BakerAI: {botStr}\n'
        # Add the exchange to the window
        self.outputBox.configure(state="normal")
        self.outputBox.insert(tk.END, userStr) 
        self.outputBox.insert(tk.END, botStr) 
        self.outputBox.configure(state="disabled")


if __name__ == '__main__':
    client = bakerClient()
    client.mainloop()

