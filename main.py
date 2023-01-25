from joblib import load
from sklearn.feature_extraction.text import CountVectorizer
from nltk.stem import WordNetLemmatizer
from nltk.corpus import stopwords
import re
import PySimpleGUI as sg

engStopWords = stopwords.words('english')


def lemmatize(word):
    wnl = WordNetLemmatizer()
    word = wnl.lemmatize(word, pos='v')
    word = wnl.lemmatize(word, pos='n')
    word = wnl.lemmatize(word, pos='a')
    return word


def cleanText(text):
    # emojis pattern source is stackoverflow
    emoj = re.compile(
        "["
        u"\U0001F600-\U0001F64F"  # emoticons
        u"\U0001F300-\U0001F5FF"  # symbols & pictographs
        u"\U0001F680-\U0001F6FF"  # transport & map symbols
        u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
        u"\U00002500-\U00002BEF"  # chinese char
        u"\U00002702-\U000027B0"
        u"\U00002702-\U000027B0"
        u"\U000024C2-\U0001F251"
        u"\U0001f926-\U0001f937"
        u"\U00010000-\U0010ffff"
        u"\u2640-\u2642"
        u"\u2600-\u2B55"
        u"\u200d"
        u"\u23cf"
        u"\u23e9"
        u"\u231a"
        u"\ufe0f"  # dingbats
        u"\u3030"
        "]+",
        re.UNICODE)

    # Removing links, non letters, eemojis, and turning to lower case
    text = re.sub(r'http\S+ ', '', text).lower()
    text = re.sub(r'[^a-zA-Z]+', ' ', text)
    text = re.sub(emoj, "", text)

    # Lemmatizing and removing stop words
    text = list(map(lemmatize, text.split()))
    text = ' '.join([word for word in text if word not in engStopWords])

    return text


def classifyText(text):
    if text == '':
        return "No text entered"
    text = cleanText(text)
    text = cv.transform([text]).toarray()
    pred = model.predict(text)
    return "The text is suicidal" if pred else "The text is not suicidal"


cv = load('./models/cv.joblib')
model = load('./models/model.joblib')

sg.theme('DarkPurple4')

layout = [[
    sg.Text("Enter your text"),
    sg.InputText(size=(40, 4), pad=((0, 30), (0, 0))),
    sg.Button('Classify', key="submit", pad=((0, 30), (0, 0))),
    sg.Button("Clear", key="clear",)
], [sg.Text("", key="answer", size=(80, 1), justification='center',pad=(0,40),auto_size_text=True)]]

window = sg.Window(title="Suicide Detection", layout=layout, margins=(80, 80))

while True:
    event, values = window.read()
    if event == sg.WIN_CLOSED:
        break
    elif event == "submit":
        answer = classifyText(values[0])
        window["answer"].update(answer)
    elif event == "clear":
        window[0].update('')

