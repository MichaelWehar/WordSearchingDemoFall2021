# Import Flask
from flask import Flask, render_template
app = Flask(__name__)

# Import SQL
import sqlite3

# Import date
import datetime

# Server routes
# (1) This will return a webpage
@app.route("/")
def get_main_page():
    return render_template("index.html")

# (2) This will return a sample message
@app.route("/test")
def get_test_message():
    return "Hello World!"

# (3) This will return a text response
@app.route('/search/<searchTerm>')
def get_search_results(searchTerm):
    # Record search
    conn = sqlite3.connect('private/searchHistory.db')
    cursor = conn.cursor()
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")
    sql_command = 'insert into history (searchTerm,timestamp) values ("' + searchTerm + '","' + timestamp + '");'
    cursor.execute(sql_command)
    conn.commit()
    conn.close()

    # Perform search
    toReturn = ""
    searchTerm = searchTerm.lower()
    # words comes from: https://github.com/MichaelWehar/Public-Domain-Word-Lists/blob/master/5000-more-common.txt
    wordlist = ["species","practice","natural","measure","present","form","order","quality","condition","state","action","element","part","division","subject","ground","power","station","register","person","place","ordinary","strong","under","make","light","exercise","exchange","parallel","charge","support","judgment","substance","figure","strength","sound","service","quantity","standard","right","point","character","strike","discharge","force","return","spring","square","between","without","water","spirit","distance","contract","positive","position","straight","moderate","double","superior","certain","compound","interest","language","passage","business","through","manner","relation","general","process","strain","delicate","bearing","property","advance","account","original","religion","round","over","principal","sharp","surface","line","degree","report","course","matter","sentence","body","express","close","quarter","head","negative","take","plant","argument","increase","house","movement","table","balance","separate","small","back","entrance","settle","reason","machine","common","material","scale","authority","capable","anything","regular","stock","break","opposite","into","distress","work","standing","cross","color","number","stroke","convert","radical","relative","function","stand","press","question","peculiar","progress","together","touch","capacity","physical","horse","specific","external","produce","incapable","passion","represent","promise","tender","issue","family","range","domestic","shoulder","change","approach","transfer","carriage","feeling","security","something","direction","pressure","frame","like","free","company","inferior","distinct","variety","solution","capital","grain","deposit","circular","receive","pleasure","particular","office","faculty","motion","personal","country","narrow","occasion","open","addition","second","complete","short","ancient","contrary","serve","disorder","crown","mark","weight","large"]
    for word in wordlist:
        word = word.lower()
        if searchTerm in word:
            toReturn += word + "<br>\n"
    return toReturn

# (4) This will return the search history
@app.route('/history')
def get_history():
    toReturn = ""
    conn = sqlite3.connect('private/searchHistory.db')
    cursor = conn.cursor()
    historyData = cursor.execute("select * from history;")
    for row in historyData:
        toReturn += row[0] + "|" + row[1] + "<br>\n"
    return toReturn

if __name__ == '__main__':
    app.run()
