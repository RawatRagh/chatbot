import nltk
from nltk.stem import WordNetLemmatizer
lemmatizer = WordNetLemmatizer()
import pickle
import numpy as np

from keras.models import load_model
model = load_model('chatbot_model1.h5')
import json
import random
intents = json.loads(open('intents.json').read())
words = pickle.load(open('words.pkl','rb'))
classes = pickle.load(open('classes.pkl','rb'))


def clean_up_sentence(sentence):
    sentence_words = nltk.word_tokenize(sentence)
    sentence_words = [lemmatizer.lemmatize(word.lower()) for word in sentence_words]
    return sentence_words

# return bag of words array: 0 or 1 for each word in the bag that exists in the sentence

def bow(sentence, words, show_details=True):
    # tokenize the pattern
    sentence_words = clean_up_sentence(sentence)
    # bag of words - matrix of N words, vocabulary matrix
    bag = [0]*len(words)
    
    for s in sentence_words:
        print(s)
        for i,w in enumerate(words):
          
            print(w)
            if w == s:
                # assign 1 if current word is in the vocabulary position
                print("here")
                bag[i] = 1
                if show_details:
                    print ("found in bag: %s" %w)
    print(np.array(bag))
    return(np.array(bag))

def predict_class(sentence, model):
    # filter out predictions below a threshold
    p = bow(sentence, words,show_details=True)
    print(p)
    print("KG")
    res = model.predict(np.array([p]))[0]
    print(res)
    ERROR_THRESHOLD = 0.25
    results = [[i,r] for i,r in enumerate(res) if r>ERROR_THRESHOLD]
    print(results)
    # sort by strength of probability
    results.sort(key=lambda x: x[1], reverse=True)
    print(results)
    return_list = []
    for r in results:
        return_list.append({"intent": classes[r[0]], "probability": str(r[1])})
       
    return return_list

def getResponse(ints, intents_json):
    tag = ints[0]['intent']
    list_of_intents = intents_json['intents']
    prob = float(ints[0]['probability'])
    
    print(prob)
    if prob>0.9 :
        for i in list_of_intents:
            if(i['tag']== tag):
                result = random.choice(i['responses'])
                break
    else:
        for i in list_of_intents:
            if(i['tag']== "noanswer"):
                result = random.choice(i['responses'])
                break    
    return result

def chatbot_response(msg):
    ints = predict_class(msg, model)
    print(ints)
    res = getResponse(ints, intents)
    return res


#Creating GUI with tkinter
import tkinter
from tkinter import *



def send(): 
    msg = EntryBox.get("1.0",'end-1c').strip()
    EntryBox.delete("0.0",END)
    
    if msg != '':
        ChatLog.config(state=NORMAL)
        ChatLog.insert(END, "You: " + msg + '\n\n')
        ChatLog.config(foreground="#442265", font=("Verdana", 8 ))

        res = chatbot_response(msg)
        
        ChatLog.insert(END, "Virtual Buddy: " + res + '\n\n')
        ChatLog.insert(END, "---------------------------------------------------------------------" +'\n\n')

        ChatLog.config(state=DISABLED)
        ChatLog.yview(END)
    

base = Tk()
base.title("Welcome to NTT Data Virtual Buddy")

base.geometry("550x550")
base.resizable(width=FALSE, height=FALSE)

#Create Chat window
ChatLog = Text(base, bd=1, bg="white", height="375", width="500", font="Arial",wrap="word")
def_msg = "Welcome to NTT Data Self Service system. I am your virtual buddy. Let me know how can i help you.!!!"
ChatLog.config(foreground="#442265", font=("Verdana", 8 ),)
ChatLog.insert(END, "Virtual Buddy: " + def_msg + '\n\n')
ChatLog.config(state=DISABLED)


#Bind scrollbar to Chat window
scrollbar = Scrollbar(base, command=ChatLog.yview, cursor="arrow")
ChatLog['yscrollcommand'] = scrollbar.set

#Create Button to send message
SendButton = Button(base, font=("Verdana",9,'bold'), text="Send", width="12", height=5,
                    bd=3, bg="#32de97", activebackground="#3c9d9b",fg='#ffffff',
                    command= send )

#Create the box to enter message
EntryBox = Text(base, bd=2, bg="light grey",width="375", height="5", font=("Arial",10))
#EntryBox.bind("<Return>", send)


#Place all components on the screen
scrollbar.place(x=525,y=6, height=375)
ChatLog.place(x=6,y=6, height=375, width=500)
EntryBox.place(x=6, y=401, height=90, width=350)
SendButton.place(x=356, y=420, height=50)

base.mainloop()