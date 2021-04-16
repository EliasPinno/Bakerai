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
        # Title label
        title = tk.Label(mainFrame, text="Welcome to Sakura's very own BakerAI!", font=TITLE_FONT)
        title.grid(row=1,column=1,columnspan=7)
        # Add labels for input
        entryLabel = tk.Label(mainFrame, text="Enter your text below! Type 'Wiki <text>' to query Wikipedia.", font=FONT)
        entryLabel.grid(row=4, column=1, columnspan=4, sticky="")
        # What we will change to show output
        self.outputBox = tk.Text(mainFrame, font=FONT)
        self.outputBox.grid(row=3, column=1, columnspan=7, rowspan=1, sticky="")
        self.outputBox.insert(tk.END,"BakerAI: Hey there! How can I help you? \n")
        self.outputBox.configure(state="disabled")
        # Create a scrollbar and configure it
        scrollbar = tk.Scrollbar(self)
        scrollbar.config(command = self.outputBox.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.outputBox.config(yscrollcommand=scrollbar.set)

        # Input related items
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
            # Send user message without the wiki portion, and save the response  
            wikiReply = self.wikiResponse(userMessage[5:], shortLan) 
            self.addExchange(userMessage, wikiReply)
            return
        # Translate input to english to send to our bot
        userEnglish = m.translate(userMessage, shortLan, 'en')
        # Get our reply
        reply = m.getFinalOutput(self.loaded_clf,userEnglish)
        # Translate reply to proper language
        replyLan = m.translate(reply, 'en', shortLan)
        self.addExchange(userMessage,replyLan)

    
    def wikiResponse(self, userMessage, lan):
        # Set the wiki language and get a response
        m.setWikiLan(lan)
        topResult, summary = m.getTopSearch(userMessage)
        if topResult != -1:
            # Translate the wrapping text, and get the display that response
            outputStr = f'{m.translate("Are you talking about","en",lan)} {topResult.title}? {m.translate("Here is what I know about this based on wikipedia.","en",lan)} \n{m.translate("A link to the page is:","en",lan)} {topResult.url}\n{m.translate("Here is the first 3 sentences of the summary:","en",lan)}\n{summary}'
        else:
            # If the wiki search returned no results, return this string translated
            outputStr = m.translate("I don\'t have any hits for that search, sorry!","en",lan)
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

