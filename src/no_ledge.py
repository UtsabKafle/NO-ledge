import wikipedia
import pyttsx3
import sqlite3
import datetime,os
from PIL import Image, ImageDraw, ImageFont
import urllib.request






engine = pyttsx3.init()


class noledge:
    def __init__(self) -> None:
        self.conn = sqlite3.connect('assets/noledge.db')
        all_fonts = os.listdir('assets/fonts')
        self.font = all_fonts[1]
        self.font = f"assets/fonts/{self.font}"

    def get_random_id(self):
        self.random_id  = wikipedia.random()
        return self.random_id

    def get_summary(self):
        self.summary = wikipedia.summary(self.get_random_id())
        return self.summary
    
    def internet_conn(self,host='http://google.com'):
        try:
            urllib.request.urlopen(host)
            return True
        except:
            return False
    
    def get_content(self):
        check = open('assets/check.uk','r')
        ch = check.readline()
        today = str(datetime.date.today())
        print(f"{ch} - {today}")
        if ch==today:
            print('done !')
            check.close()
        else:
            if self.internet_conn():
                check = open('assets/check.uk','w')
                que = 'INSERT INTO DATA (title, content, date) values(?,?,?)'
                data = []
                for i in range(5):
                    try:
                        data.append((self.get_random_id(),self.get_summary(),datetime.date.today()))
                    except Exception:
                        print("some errors, please try again !")
                with self.conn:
                    self.conn.executemany(que,data)
                check.write(today)
                check.close()
            else:
                pass
        
    def show_all(self):
        que = 'SELECT * FROM DATA'
        data = self.conn.execute(que)
        for i in data:
            print(i)

    def add_line_breaks(self,text):
        words = text.split(" ")
        for i in range(1,len(words)+1):
            if i%8==0:
                words[i-1] += "\n"
        cont_ = ""
        for i in range(len(words)):
            cont_ += words[i]+" "
        return cont_

    def draw(self,type='content',title=None,content=None):
        """
            draw function draws the image
            type: can be title, logo or content(default). I won't say anything about them, try it yourself !
        """
        pot = (1080,1350)
        # print(self.font)
        self.jii = Image.new('RGB',pot,color=(0,0,0))
        self.wr = ImageDraw.Draw(self.jii)
        ###logo
        logo_x_corr = 10
        logo_y_corr = 180
        logo_f_size = 50
        tits_font = ImageFont.truetype(self.font,logo_f_size)
        self.wr.text((logo_x_corr,logo_y_corr),title,font=tits_font)
        #content
        x_corr = 30
        y_corr = 255
        content_f_size = 35
        tits_font = self.font
        tits_font = ImageFont.truetype(self.font,content_f_size)
        content = self.add_line_breaks(content)
        self.wr.text((x_corr,y_corr),content,font=tits_font)
    def save(self,file_name):
        self.jii.save(file_name)
        self.jii.show()
    
    def daily(self):
        ran = "SELECT * FROM DATA ORDER BY RANDOM() LIMIT 1"
        data = self.conn.execute(ran)
        for i in data:
            title = i[1]
            content = i[2]
            date = i[3]
        self.draw(title=title,content=content)
        self.save(f'images/{date}_{title}.png')
        engine.say(title+". ."+content)
        engine.runAndWait()
def main():
    x = noledge()
    x.get_content()
    x.daily()

if __name__ == "__main__":
    main()