# 2017 ამერიკის ერთერთ შტატში მომხდარი ავარიების სტატისტიკა
# ცხრილი აღებულია https://catalog.data.gov/dataset  საიტიდან, ექსელის  დოკუმენტი მაქ დაფორმატებული,
# იმისმიხედვით თუ რა მონაცემი მჭირდებოდა. მოცემულია ავარიების თარიღები, მანქანის მოდელები, მძღოლების აიდი, სქესი და
# დაზიანების ხარისხი.  ცხრილის მონაცემებით ვავსებ მონგო დბ -ის ბაზას, მანადე კი გრაფიკული ინტერსფეისის 2 ღილაკით
# ვაჩვენებ დიაგრამებს. ამისათვის ვქმნი კლასს;


import pandas as pd  # ექსელთან სამუშაოდ
from matplotlib import pyplot as py  # დიაგრამებთან სამუშაოდ
from tkinter import *  # ინტერფეისი გასაკეთებლად
from pymongo import MongoClient  # მოგოს ბაზასათან სამუშაოდ
import numpy as np  # ორგანზომილებიანი ლისტისთვის
import threading as th


class Crash:
    # მეთოდი, რომელიც ქმნის მარტივ წრიულ დიაგრამას, მასზე წრმოდგენილია  ავარიებში დამნაშავე მამაკაცების და ქალების წილი

    def show():
        df = pd.read_excel("Crash.xlsx", "CRASH1")  # ექსელის  ფაილიდან წაკითხვა და წამოღება
        sex = df['SEX_CODE']  # შესაბამისი ინფორმაციის (სქესის) შენახვა
        a, b = 0, 0
        for i in sex:
            if i == 'M':  # მარტივი  if, თუ M (მამრობითი) ასო აღმოჩნდა
                a += 1  # მთვლელი გაიზრდება ერთით

            elif i == 'F':  # ხოლო თუკი F (მდედრობითი სქესი) ასო აღმოჩნდა
                b += 1  # მთვლელი გაიზრდება ერთით

        # წრიული დიაგრამის გაკეთება

        numbers = [a, b]
        purpose = ['Female', 'Male']
        exp = [0, 0.1]  # გამოყოფა ერთი ნაწილის მეორესთან
        cl = ['red', 'green', ]  # ფერების განსაზღვრა
        py.pie(numbers, labels=purpose, explode=exp, autopct='%2.1f%%', colors=cl)  # წრის განსაზღვრა
        py.title('ავარიაში მონაწილეები')  # სათაური
        py.legend()  # დიაგრამის ლეგენდების ჩვენება (მნიშვნელობები)
        py.show(bg='cadet blue')  # დიაგრამის გამოჩენა

    # მეთოდი, რომელიც ცხრილის სახით აჩვენებს იმ მანქენების მწარმოებელი ფირმის სახელებს, რომელებიც ყველაზე ხშირად
    # მოყვნენ ავარიაში:

    def show_2():
        df = pd.read_excel("Crash.xlsx", "CRASH1")  # ექსელის  ფაილიდან წაკითხვა და წამოღება
        car = df['VEH_MAKE']  # შესაბამისი ინფორმაციის (მანქანის მოდელის) შენახვა ამ რაოდენობის იმიტო რო
        # დიდი დროროარ დაჭირდეს სამუშაოდ  და მალე ქნას
        k, t, b, m, f, h, n, ot = 0, 0, 0, 0, 0, 0, 0, 0
        # კონკრეტული მანქანების რაოდენობების დათვლა ცხრილის მონაცემების მიხედვით
        for j in car:
            if j == 'KIA':
                k += 1
            elif j == 'TOYOTA':
                t += 1
            elif j == 'HONDA':
                h += 1
            elif j == 'NISSAN':
                n += 1
            elif j == 'BMW':
                b += 1
            elif j == 'MERCEDES':
                m += 1
            elif j == 'FORD':
                f += 1
            else:
                ot += 1

        # მასივის შექმნა აუტომანქანების მწარმოებელი ფირმის სახელებითა და მათი ავარიათა რაოდენობით
        g = ['KIA', 'TOYOTA', 'HONDA', 'NISSAN', 'BMW', 'MERCEDES', 'FORD', 'others']
        z = [k, t, h, n, b, m, f, ot]
        num = np.arange(len(g))
        py.xticks(num, g)
        py.bar(num, z)

        py.title('ძირითადი დაზიანებები 2017 წლის მომხდარ ავარიებში')  # სათაური
        py.show(bg='yellow')  # დიაგრამის გამოჩენა


# df = pd.read_excel("Crash.xlsx", "CRASH1")  # ვუკავშირდებით ექსელის დოკუმნტს სრული რაოდენობა
df = pd.read_excel("Crash.xlsx", "CRASH1")[:1000]    # შემცირებული რაოდენობა
ID = df['PERSON_ID']  # და თითოეულ ველს ვავსებთ ექსელის სვეტებზე განთავსებული ინფორმაციებით
sex = df['SEX_CODE']
birth = df['DATE_OF_BIRTH']
damage = df['REPORT_TYPE']
date = df['ACC_DATE']
car = df['VEH_MAKE']


# ვიწყებ thread ებთან მუშაობას, ამიტომ ვქმნი ფუნქციას, რომელიც try except ის დახმარებით ავსებს მონგოდბ ის ბაზას

def thr():
    # ვიყენებ try except ის ბლოკს, თუ მონგო არ შეივსო სწორად და შეცდომა დაფიქსირდება, მაშინ
    # except  დაწერს რომ ბაზის შევსება შეუძლებელია, ინფორმაციის დიდი ზომის გამო.

    try:

        client = MongoClient('localhost', 27017)  # ვუკავშირდები ბაზას
        db = client['data_base']  # ხდება კოლექციის შექმნა
        collection = db['CRASH1']  # კოლექციაში ბაზის შექმნა

        # ლექსიკონის შევსება,  რათა შედეგშ იგი ჩავწეროთ მონგოს ბაზაში :
        for i in range(ID.size):
            dct = {"ID": ID[i], "Sex": sex[i], "Birth Date": birth[i], "Accident Date": date[i], "car": car[i],
                   "Damage": damage[i]}

            # მონგოს შევსება ლექსიკონით

            collection.insert_one(dct)
        # მონგოში ჩაწერილი პირველი 5 ელემენტის ჩვენება
        for record in collection.find()[:5]:
            print(record)

    except:     # თუ კი შეცდომა წარმოიშვა მონაცემთა შენახვისას დაიწერება ეს -> :
        print('Too large data; \n'
              'Cant save in base')

    else:  # თუ კი ყველაფერმა სწორად იმუშავა დაიბეჭდება:
        print("everything done correctly ")


x = th.Thread(target=thr)  # სრედის განსაზღვრა, ფუნქციის მიბმა
x.start()  # დწყება
print(f'process amount = {th.activeCount()}')


window = Tk()  # ინტერსფეისის დაკავშირება
window.title('2017y. Crash statistic')  # გამოტანის ეკრანის სათაური
butt1 = Button(window, text='Show Diagram 1', pady=15, padx=50, bg='yellow', command=Crash.show)  # ღილაკი
butt2 = Button(window, text='Show diagram 2', pady=15, padx=50, bg='yellow', command=Crash.show_2)  # ღილაკი2
butt1.grid(row=1, column=0)  # განლაგება
butt2.grid(row=1, column=2)  # განლაგენა
window.geometry("375x100+0+0")  # ფანჯარის ზომა
window.config(bg='black')   # ფანჯარის ფერი

window.mainloop()  # ტკინტერის ეკრანის ჩვენება
