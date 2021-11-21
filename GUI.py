import tkinter as tk
import tkinter.font as font
import tkinter.messagebox
from Zoo import *
import pickle
import tkinter.filedialog as filedialog


# 첫 실행시 나오는 화면
class MainFrame(tk.Frame):
    main = None
    mainCanvas = None

    lbContinue = None
    lbStart = None
    lbExit = None

    btContinue = None
    btStart = None
    btExit = None
    bg = None

    def __init__(self, root):
        tk.Frame.__init__(self, root)

        self.font = font.Font(family="휴먼매직체", size=24, weight="bold")

        self.root = root
        self.zoo = Zoo()

        self.InitWindow()
        self.bg = ImageTk.PhotoImage(
            Image.open("./image/MainBackground2.png").resize((self.w, self.h), Image.ANTIALIAS))

        self.InitComponent()

    # 윈도우창(Frame)의 크기, 타이틀 등등을 초기화
    def InitWindow(self):
        self.w = 500
        self.h = 600

        x = (self.root.winfo_screenwidth() // 2) - (self.w // 2)
        y = (self.root.winfo_screenheight() // 2) - (self.h // 2)

        self.root.title("Zoo Tycoon")
        self.root.geometry("%dx%d+%d+%d" % (self.w, self.h, x, y))
        self.root.resizable(False, False)

    # Label, Button등의 Component를 초기화
    def InitComponent(self):
        self.main = tk.Frame(self.root, width=self.w, height=self.h)
        self.main.pack()

        self.mainCanvas = tk.Canvas(self.main, width=self.w, height=self.h)
        self.mainCanvas.create_image(0, 0, image=self.bg, anchor="nw")
        self.mainCanvas.place(x=0, y=0)

        self.btStart = tk.Button(self.main, text="새로하기", width=7,
                                 height=1, borderwidth=0, font=self.font,
                                 bg="#d09a41", cursor="hand2", command=self.Start)
        self.btStart.place(x=180, y=180)

        self.btContinue = tk.Button(self.main, text="이어하기", width=7,
                                    height=1, borderwidth=0, font=self.font,
                                    bg="#d09a41", cursor="hand2", command=self.Continue)
        self.btContinue.place(x=180, y=320)

        self.btExit = tk.Button(self.main, text="종료하기", width=7,
                                height=1, borderwidth=0, font=self.font,
                                bg="#d09a41", cursor="hand2", command=self.Exit)
        self.btExit.place(x=180, y=460)

        self.root.bind("<Escape>", lambda _:self.Test())

    def Test(self):
        self.main.destroy()
        PlayFrame(self.root, self.zoo, 1)


    def Start(self):
        self.main.destroy()
        PlayFrame(self.root, self.zoo)

    def Continue(self):
        types = [("zoo file", ".zoo")]
        file = filedialog.askopenfilename(filetypes=types, title="파일 열기")

        if file == "":
            return

        self.main.destroy()

        with open(file, "rb") as F:
            zoo = pickle.load(F)
            PlayFrame(self.root, zoo)

    def Exit(self):
        quit()

# 실질적으로 게임을 하는 화면
class PlayFrame(tk.Frame):
    w = 1200  # 게임 창의 width
    h = 900  # 게임 창의 heigth
    lbFont = None  # 라벨을 위한 폰트

    status = None  # 상단바(정보 표시 부분)
    lbMoney = None  # 상단바에 놓여지는 Label들
    lbCustomer = None  # #
    lbDate = None  # #
    lbWeather = None  # #
    lbTime = None  # #

    # 상단바를 그리기 위해 필요한 string 값들
    money = None
    customer = None
    date = None
    weather = None
    time = None

    main = None  # 메인 프레임(실질적으로 그려지는 부분)
    background = None  # main위에 놓여지는 canvas
    bg = None  # ground(canvas)위에 그려질 이미지
    ground = None  # background(canvas)위에 그려질 때 ID받는 변수

    groundMenu = None  # 땅 클릭시 나오는 메뉴(Frame)
    btBuy = None  # 동물 사기 버튼
    btBuyLand = None  # 토지 확장 버튼
    lbBuyLand = None

    boundaryMenu = None  # 우리 클릭시 나오는 메뉴(Frame)
    btAdd = None  # 동물추가 버튼
    lbAdd = None  # 동물 추가 가격
    btGroupFeed = None  # 우리 전체 먹이주기 버튼
    btGroupWash = None  # 우리 전체 씻겨주기 버튼
    lbGroupFeed = None  # 우리 전체 먹이주기 가격
    lbGroupWash = None  # 우리 전체 먹이주기 가격

    animalMenu = None  # 동물 클릭시 나오는 메뉴(Frame)
    btSell = None  # 동물 팔기 버튼
    lbSell = None  # 동물 팔기 가격
    btFeed = None  # 동물 먹이주기 버튼
    lbFeed = None  # 동물 먹이주기 가격
    btWash = None  # 동물 씻겨주기 버튼
    btCure = None  # 동물 치료하기 버튼
    lbCure = None  # 동물 치료하기 가격

    groundFlag = 0  # 땅, 우리, 동물 클릭을 위한 플래그
    animalFlag = 0  # 동물 클릭시 Boundary가 같이 클릭 되는거 방지

    tempo = 1  # 게임의 배속을 결정 높을수록 빠름

    btNormal = None
    btDouble = None
    btTriple = None
    btQuadruple = None

    offsetX = 0  # 화면을 이동하기 위한 x값
    offsetY = 0  # 화면을 이동하기 위한 y값
    zoo = None
    escFlag = 0

    def __init__(self, root, zoo, test = 0):
        tk.Frame.__init__(self, root)
        self.btFont = font.Font(family="HY엽서M", size=14)  # Button을 위한 폰트
        self.lbFont = font.Font(family="HY엽서M", size=11)  # Label을 위한 폰트

        self.btBg = "#4048d0"   #버튼 색상 지정
        self.btWidth = 11

        self.btOffsetX = 50     #메뉴에 달리는 버튼의 맨왼쪽 버튼의 위치
        self.btOffsetY = 20     #메뉴에 달리는 버튼의 y축 위치
        self.GapX = 200         #메뉴에 달리는 Component의 x 간격
        self.lbOffsetX = 55     #메뉴에 달리는 Label의 맨왼쪽 Label의 위치
        self.lbOffsetY = 80     #메뉴에 달리는 Label의 y축 위치

        # Background 이미지(풀 이미지임)
        self.bg = ImageTk.PhotoImage(Image.open("./image/BackgroundTile.png"))

        self.root = root
        self.zoo = zoo
        self.boundaryList = []
        self.groundFlag = 0
        self.animalFlag = 0

        self.InitWindow()
        self.InitComponent()
        self.Time()

        self.offsetX = 0
        self.offsetY = 0
        self.escFlag = 0

        if test == 1:
            self.btTest = tk.Button(self.status, text="test용", font=self.btFont, width=7, height=1, bg="#c0d0ff",
                                    command=self.Test)
            self.btTest.place(x=250, y=10)
    def InitWindow(self):

        self.xCoordinate = 0
        self.yCoordinate = 0
        self.BoundaryList = []

        # 화면 크기 설정
        x = (self.root.winfo_screenwidth() // 2) - (self.w // 2)
        y = (self.root.winfo_screenheight() // 2) - (self.h // 2)
        self.root.title("Zoo Tycoon")
        self.root.geometry("%dx%d+%d+%d" % (self.w, self.h, x, y))
        self.root.resizable(False, False)

    def InitComponent(self):
        self.money = tk.StringVar()
        self.customer = tk.StringVar()
        self.date = tk.StringVar()
        self.weather = tk.StringVar()
        self.time = tk.StringVar()

        self.money.set(self.zoo.GetMoney())
        self.customer.set(self.zoo.GetCustomer())
        self.date.set(self.zoo.GetDate())
        self.weather.set(self.zoo.GetWeather())
        self.time.set(self.zoo.GetTime())

        self.main = tk.Frame(self.root, width=self.zoo.maxGround, height=self.zoo.maxGround)
        self.main.place(x=0, y=50)
        self.background = tk.Canvas(self.main, width=self.zoo.maxGround, height=self.zoo.maxGround)
        self.background.place(x=0, y=0)
        for x in range(self.zoo.maxGround // 40):
            for y in range(self.zoo.maxGround // 40):
                ground = self.background.create_image(x * 40, y * 40, image=self.bg, anchor="nw")
                self.background.tag_lower(ground)
        self.background.bind("<Button-1>", self.GroundClick)

        #groundMenu에 달리는 Component들
        self.groundMenu = tk.Frame(self.root, width=self.w + 10, height=150 + 10, bg="#d0d0ca", relief="solid", borderwidth=4)

        self.btBuy = tk.Button(self.groundMenu, bg=self.btBg, font=self.btFont, text="동물 구입", width=self.btWidth, height=1, borderwidth=0, command=self.BuyAnimal)
        self.btBuy.place(x=0*self.GapX + self.btOffsetX,
                         y=self.btOffsetY)
        self.btBuyLand = tk.Button(self.groundMenu, bg=self.btBg,font=self.btFont, text="토지 확장", width=self.btWidth, height=1, borderwidth=0, command=self.BuyLand)
        self.btBuyLand.place(x=1*self.GapX + self.btOffsetX,
                             y=self.btOffsetY)
        self.lbBuyLand = tk.Label(self.groundMenu, bg = "#d0d0ca", font=self.lbFont,  text=self.zoo.GetBuyLandCost(), width=self.btWidth, height=1)
        self.lbBuyLand.place(x=1*self.GapX + self.lbOffsetX,
                             y=self.lbOffsetY)



        #boundaryMenu에 달리는 Component들
        self.boundaryMenu = tk.Frame(self.root, width=self.w + 10, height=150 + 10, bg="#d0d0ca", relief="solid",
                                     borderwidth=4)

        self.btAdd = tk.Button(self.boundaryMenu, bg=self.btBg, font=self.btFont, text="동물추가", width=self.btWidth, height=1, borderwidth=0)
        self.btAdd.place(x=0*self.GapX + self.btOffsetX,
                         y=self.btOffsetY)
        self.btGroupFeed = tk.Button(self.boundaryMenu, bg=self.btBg, font=self.btFont, text="단체 먹이주기", width=self.btWidth, height=1, borderwidth=0)
        self.btGroupFeed.place(x=1*self.GapX + self.btOffsetX,
                               y=self.btOffsetY)
        self.btGroupWash = tk.Button(self.boundaryMenu, bg=self.btBg, font=self.btFont, text="단체 씻겨주기", width=self.btWidth, height=1, borderwidth=0)
        self.btGroupWash.place(x=2*self.GapX + self.btOffsetX,
                               y=self.btOffsetY)

        self.lbAdd = tk.Label(self.boundaryMenu,width=10, height=1, bg="#d0d0ca", font=self.lbFont)
        self.lbAdd.place(x=0*self.GapX + self.lbOffsetX,
                         y=self.lbOffsetY)
        self.lbGroupFeed = tk.Label(self.boundaryMenu, width=10, height=1, bg="#d0d0ca", font=self.lbFont)
        self.lbGroupFeed.place(x=1*self.GapX + self.lbOffsetX,
                               y=self.lbOffsetY)

        #animalMenu에 달리는 Component들
        self.animalMenu = tk.Frame(self.root, width=self.w + 10, height=150 + 10, bg="#d0d0ca", relief="solid",
                                   borderwidth=4)

        self.btSell = tk.Button(self.animalMenu, bg=self.btBg, font=self.btFont, text="동물판매", width=self.btWidth, height=1, borderwidth=0)
        self.btSell.place(x=0*self.GapX + self.btOffsetX, y=self.btOffsetY)
        self.btFeed = tk.Button(self.animalMenu, bg=self.btBg, font=self.btFont, text="먹이주기", width=self.btWidth, height=1, borderwidth=0)
        self.btFeed.place(x=1*self.GapX + self.btOffsetX, y=self.btOffsetY)
        self.btWash = tk.Button(self.animalMenu, bg=self.btBg, font=self.btFont, text="씻겨주기", width=self.btWidth, height=1, borderwidth=0)
        self.btWash.place(x=2*self.GapX + self.btOffsetX, y=self.btOffsetY)
        self.btCure = tk.Button(self.animalMenu, bg=self.btBg, font=self.btFont, text="치료하기", width=self.btWidth, height=1, borderwidth=0)
        self.btCure.place(x=3*self.GapX + self.btOffsetX, y=self.btOffsetY)

        self.lbSell = tk.Label(self.animalMenu, width=10, bg="#d0d0ca", height=1, font=self.lbFont)
        self.lbSell.place(x=0*self.GapX + self.lbOffsetX, y=self.lbOffsetY)
        self.lbFeed = tk.Label(self.animalMenu, width=10, bg="#d0d0ca", height=1, font=self.lbFont)
        self.lbFeed.place(x=1*self.GapX + self.lbOffsetX, y=self.lbOffsetY)
        self.lbCure = tk.Label(self.animalMenu, width=10, bg="#d0d0ca", height=1, font=self.lbFont)
        self.lbCure.place(x=2*self.GapX + self.lbOffsetX, y=self.lbOffsetY)

        #상단바에 달리는 Component들
        self.status = tk.Frame(self.root, width=self.w, height=50, bg="#c0d0ff")
        self.status.place(x=0, y=0)

        self.lbMoney = tk.Label(self.status, textvariable=self.money, width=12, height=1, font=self.lbFont, anchor="w",
                                bg="#c0d0ff")
        self.lbMoney.place(x=100, y=10)

        self.lbCustomer = tk.Label(self.status, textvariable=self.customer, width=6, height=1, font=self.lbFont,
                                   bg="#c0d0ff")
        self.lbCustomer.place(x=400, y=10)

        self.lbDate = tk.Label(self.status, textvariable=self.date, width=15, height=1, font=self.lbFont, bg="#c0d0ff")
        self.lbDate.place(x=500, y=10)

        self.lbTime = tk.Label(self.status, textvariable=self.time, width=7, height=1, font=self.lbFont, bg="#c0d0ff")
        self.lbTime.place(x=700, y=10)

        self.btNormal = tk.Button(self.status, font=self.btFont, text="X 1", width=3, height=1, bg="#0000d7",
                                  command=lambda: self.SetTempo(1))
        self.btNormal.place(x=800, y=5)
        self.btDouble = tk.Button(self.status, font=self.btFont, text="X 2", width=3, height=1, bg="#c0d0ff",
                                  command=lambda: self.SetTempo(2))
        self.btDouble.place(x=850, y=5)
        self.btTriple = tk.Button(self.status, font=self.btFont, text="X 5", width=3, height=1, bg="#c0d0ff",
                                  command=lambda: self.SetTempo(5))
        self.btTriple.place(x=900, y=5)
        self.btQuadruple = tk.Button(self.status, font=self.btFont, text="X 10", width=3, height=1, bg="#c0d0ff",
                                     command=lambda: self.SetTempo(10))
        self.btQuadruple.place(x=950, y=5)

        self.lbWeather = tk.Label(self.status, textvariable=self.weather, width=10, height=1, font=self.lbFont,
                                  bg="#c0d0ff")
        self.lbWeather.place(x=1050, y=10)



        # 방향키 조작으로 맵 이동
        self.root.bind("<Left>", lambda _: self.Direction(4))
        self.root.bind("<Right>", lambda _: self.Direction(6))
        self.root.bind("<Up>", lambda _: self.Direction(8))
        self.root.bind("<Down>", lambda _: self.Direction(2))

        # ESC 버튼으로 메뉴 띄우기
        self.root.bind("<Escape>", lambda _: self.EscMenu(self.zoo))

        # 불러오기를 하였을 때 캔버스를 그려줌
        for boundary in self.zoo.boundaryList:
            self.LoadBoundary(boundary)

    def Test(self):
        self.SetMonth()
        self.zoo.date += datetime.timedelta(days=30)
        self.zoo.money += 100000000
        self.MoneyRefresh()
        self.zoo.time = (ZooData.maxTime // 24) * 6
        self.SetTomorrow()

    def EscMenu(self, zoo):
        if self.escFlag == 1:
            self.esc.Close()
            self.escFlag = 0
        else:
            self.esc = EscWindow(self, self.root, self.background, self.zoo)
            self.escFlag = 1

    def Direction(self, direction):
        if direction == 4:  # 왼쪽
            if self.offsetX <= -40:
                self.offsetX += 40
        elif direction == 6:  # 오른쪽
            if self.offsetX > self.w - self.zoo.maxGround:
                self.offsetX -= 40
        elif direction == 8:  # 위쪽
            if self.offsetY <= -40:
                self.offsetY += 40
        elif direction == 2:  # 아래쪽
            if self.offsetY > self.h - self.zoo.maxGround:
                self.offsetY -= 40
        self.main.place(x=self.offsetX, y=self.offsetY + 50)

    # 게임의 빠르기를 결정
    def SetTempo(self, speed):
        self.tempo = speed
        if speed == 1:
            self.btNormal.configure(bg="#0000d7")
            self.btDouble.configure(bg="#c0d0ff")
            self.btTriple.configure(bg="#c0d0ff")
            self.btQuadruple.configure(bg="#c0d0ff")
        elif speed == 2:
            self.btNormal.configure(bg="#c0d0ff")
            self.btDouble.configure(bg="#0000d7")
            self.btTriple.configure(bg="#c0d0ff")
            self.btQuadruple.configure(bg="#c0d0ff")
        elif speed == 5:
            self.btNormal.configure(bg="#c0d0ff")
            self.btDouble.configure(bg="#c0d0ff")
            self.btTriple.configure(bg="#0000d7")
            self.btQuadruple.configure(bg="#c0d0ff")
        elif speed == 10:
            self.btNormal.configure(bg="#c0d0ff")
            self.btDouble.configure(bg="#c0d0ff")
            self.btTriple.configure(bg="#c0d0ff")
            self.btQuadruple.configure(bg="#0000d7")

    # 매 초마다 불리는 함수
    def Time(self):
        if self.escFlag == 1:  # esc메뉴가 켜져있을때
            self.TimeStop()
        else:
            self.zoo.Enter()  # 고객 입장 및 퇴장
            self.MoneyRefresh()
            check = self.zoo.TikTok()
            if check >= 1:  # 내일
                self.SetTomorrow()
                if check == 2:  # 내일로 가는데 month가 바뀔 경우
                    self.SetMonth()
                elif check == 3:  # 내일로 가는데 year이 바뀔 경우
                    self.SetMonth()
                    self.SetYear()
            elif check == -1:  # 정각
                for boundaryFrm in self.boundaryList:
                    for animal in boundaryFrm.boundary.animalList:
                        if animal.health <= 0:
                            self.zoo.money -= ZooData.GetSellCost(animal)
                            self.SellAnimal(animal)
                            tk.messagebox.showwarning("사망", animal.nameIndex + "이 사망했습니다")
            else:
                oneHour = ZooData.maxTime // 24
                if oneHour*6 < self.zoo.time < oneHour*22:  # 06~22시 사이에만 동물들이 이동
                    self.Move()
            self.after(500 // self.tempo, self.Time)
            self.time.set(self.zoo.GetTime())
            self.customer.set(self.zoo.GetCustomer())

    def TimeStop(self):
        if self.escFlag == 1:  # esc메뉴가 켜져있으면
            self.after(1000, self.TimeStop)  # 이 함수를 계속 불러준다
        elif self.escFlag == 0:  # esc메뉴가 켜져있지 않으면
            self.Time()  # 다시 시간이 흘러가게 한다

    # 시간이 지나 내일로 갈 경우
    def SetTomorrow(self):
        self.weather.set(self.zoo.GetWeather())
        self.date.set(self.zoo.GetDate())

    # 한달이 지날때마다 불리는 함수
    def SetMonth(self):
        self.zoo.Month()
        for bound in self.boundaryList:
            bound.Refresh()

    # 일년이 지날때마다 불리는 함수
    def SetYear(self):
        # 필요한 부분 기입
        return

    # 동물을 움직이는 함수
    def Move(self):
        for boundaryFrm in self.boundaryList:
            for animal, id in zip(boundaryFrm.boundary.animalList, boundaryFrm.IDList):
                x1, y1, x2, y2 = animal.Move()
                boundaryFrm.frame.move(id, x2 - x1, y2 - y1)

    # 땅을 클릭할 경우 메뉴를 출력
    def GroundClick(self, event):
        if self.groundFlag == 1 or event == 0:
            self.groundMenu.place_forget()
            self.boundaryMenu.place_forget()
            self.animalMenu.place_forget()
            self.groundFlag = 0
        else:
            self.groundMenu.place(x=-5, y=750)
            self.groundFlag = 1
            self.xCoordinate = (event.x // 20) * 20  # 좌표를 20단위로 끊어줌
            self.yCoordinate = (event.y // 20) * 20
            self.boundaryMenu.place_forget()

    # 땅을 클릭하면 나오는 메뉴에서 동물 추가를 할 경우
    def BuyAnimal(self):
        BuyWindow(self, self.root, self.background, self.zoo, self.xCoordinate, self.yCoordinate)

    # 땅을 클릭하면 나오는 메뉴에서 토지 확장을 할 경우
    def BuyLand(self):
        beforeMaxGround, MaxGround = self.zoo.BuyLand()

        if beforeMaxGround == -1:  # 돈이 부족하여 실패 시
            tk.messagebox.showwarning("경고", "돈이 부족합니다")
        else:  # 구입에 성공시 영역을 확장
            self.main.configure(width=MaxGround, height=MaxGround)
            self.background.configure(width=MaxGround, height=MaxGround)

            for y in range(0, beforeMaxGround, 40):
                for x in range(beforeMaxGround, MaxGround, 40):
                    ground = self.background.create_image(x, y, image=self.bg, anchor="nw")
                    self.background.tag_lower(ground)

            for y in range(beforeMaxGround, MaxGround, 40):
                for x in range(0, MaxGround, 40):
                    ground = self.background.create_image(x, y, image=self.bg, anchor="nw")
                    self.background.tag_lower(ground)

            self.MoneyRefresh()
            self.GroundClick(0)
            self.lbBuyLand.configure(text=self.zoo.GetBuyLandCost())
            tk.messagebox.showwarning("알림", "토지 확장을 하였습니다")

    # BuyAnimal -> BuyWindow -> Buy를 성공적으로 할 경우 동물 우리를 화면에 출력
    def AddBoundary(self):
        newBoundaryFrame = boundaryFrame(self.main, self.zoo.boundaryList[-1])
        newBoundaryFrame.frame.bind("<Button-1>", lambda _: self.BoundaryClick(newBoundaryFrame.boundary))
        self.boundaryList.append(newBoundaryFrame)
        boundary = newBoundaryFrame.boundary

        for id, animal in zip(newBoundaryFrame.IDList, boundary.animalList):
            self.AnimalBind(newBoundaryFrame.frame, id, animal)
        self.MoneyRefresh()

    # 불러오기 시 boundary를 생성해줌
    def LoadBoundary(self, bound):
        newBoundaryFrame = boundaryFrame(self.main, bound)
        newBoundaryFrame.frame.bind("<Button-1>", lambda _: self.BoundaryClick(newBoundaryFrame.boundary))
        self.boundaryList.append(newBoundaryFrame)
        boundary = newBoundaryFrame.boundary

        for id, animal in zip(newBoundaryFrame.IDList, boundary.animalList):
            self.AnimalBind(newBoundaryFrame.frame, id, animal)
        self.MoneyRefresh()

    # 생성된 우리를 클릭할 시 우리에 대한 명령을 띄워줌
    def BoundaryClick(self, boundary):
        if self.animalFlag == 0:
            self.boundaryMenu.place(x=-5, y=750)
            self.groundFlag = 1
            self.groundMenu.place_forget()
            self.animalMenu.place_forget()
            self.btAdd.configure(command=lambda: self.AddAnimal(boundary))
            self.btGroupFeed.configure(command=lambda: self.FeedBoundary(boundary))
            self.btGroupWash.configure(command=lambda: self.zoo.WashBoundary(boundary))

            costSum = 0
            for animal in boundary.animalList:
                costSum += ZooData.GetFoodCost(animal)

            self.lbAdd.configure(text = "-" + format(ZooData.GetBuyCost(boundary.name), ",") + "원")
            self.lbGroupFeed.configure(text = "-" + format(costSum, ",") + "원")

    # 우리를 선택하고 동물을 추가할 경우
    def AddAnimal(self, boundary):
        index, animal = self.zoo.AddAnimal(boundary)
        if index == -1:
            tk.messagebox.showwarning("구입오류", "돈이 부족합니다")
            return
        boundaryFrm = self.boundaryList[index]
        id = self.boundaryList[index].AddAnimal(animal)
        self.AnimalBind(boundaryFrm.frame, id, animal)
        self.MoneyRefresh()

    # 동물 우리를 선택하고 먹이주기를 할 경우
    def FeedBoundary(self, boundary):
        if self.zoo.FeedBoundary(boundary) == False:
            tk.messagebox.showwarning("경고", "돈이 부족합니다")
        else:
            self.MoneyRefresh()

    # 동물 클릭시 boundaryClick 이벤트가 발생하는 걸 방지
    def FlagReturn(self):
        self.animalFlag = 0

    # 우리에 있는 동물 하나하나에 버튼 클릭을 bind
    def AnimalBind(self, frame, id, animal):
        frame.tag_bind(id, "<Button-1>", lambda _: self.AnimalClick(animal))

    # 동물에 명령을 바인딩
    def AnimalClick(self, animal):
        AnimalWindow(self, self.root, self.background, animal)
        self.animalFlag = 1
        self.animalMenu.place(x=-5, y=750)
        self.groundFlag = 1
        self.groundMenu.place_forget()
        self.boundaryMenu.place_forget()
        self.btSell.configure(command=lambda: self.SellAnimal(animal))
        self.btFeed.configure(command=lambda: self.FeedAnimal(animal))
        self.btWash.configure(command=lambda: self.WashAnimal(animal))
        self.btCure.configure(command=lambda: self.Cure(animal))

        self.lbSell.configure(text="-" + format(ZooData.GetSellCost(animal), ",") + "원")
        self.lbFeed.configure(text="-" + format(ZooData.GetFoodCost(animal), ",") + "원")
        self.lbCure.configure(text="-" + format(ZooData.GetCureCost(animal), ",") + "원")

        self.after(100, self.FlagReturn)

    # 동물을 클릭 하고 동물 판매를 할 경우
    def SellAnimal(self, animal):
        boundaryIndex, animalIndex, flag = self.zoo.SellAnimal(animal)
        boundaryFrame = self.boundaryList[boundaryIndex]
        boundaryFrame.frame.delete(boundaryFrame.IDList[animalIndex])
        boundaryFrame.IDList.pop(animalIndex)
        self.GroundClick(0)
        if flag == True:  # 마지막 동물일 경우 삭제
            boundaryFrame.frame.delete("all")
            boundaryFrame.frame.place_forget()
            self.boundaryList.pop(boundaryIndex)
        self.MoneyRefresh()

    # 동물을 선택하고 먹이주기를 할 경우
    def FeedAnimal(self, animal):
        AnimalWindow(self, self.root, self.background, animal)
        if self.zoo.FeedAnimal(animal) == False:
            tk.messagebox.showwarning("경고", "돈이 부족합니다")
        else:
            self.MoneyRefresh()

    # 동물을 선택하고 씻겨주기를 할 경우
    def WashAnimal(self, animal):
        AnimalWindow(self, self.root, self.background, animal)
        self.zoo.WashAnimal(animal)

    # 동물을 선택하고 치료하기를 할 경우
    def Cure(self, animal):
        AnimalWindow(self, self.root, self.background, animal)
        check = self.zoo.Cure(animal)
        if check == 1:  # 치료할 돈이 없으면
            tk.messagebox.showwarning("경고", "돈이 부족합니다")
        elif check == 2:  # 질병에 걸린 상태가 아니면
            tk.messagebox.showwarning("경고", "질병에 걸린 상태가 아닙니다")
        else:
            self.MoneyRefresh()

    # 돈의 변동이 생길 경우 돈을 새로고침 해줌
    def MoneyRefresh(self):
        self.money.set(self.zoo.GetMoney())

# 동물구매 시 띄워주는 창
class BuyWindow(tk.Toplevel):
    def __init__(self, top, root, topFrame, zoo, x, y):
        super().__init__(top)
        btList = []
        lbList = []
        self.photoList = []
        self.previewList = []
        self.top = top
        self.root = root
        self.topFrame = topFrame
        self.preview = 0  # 미리보기 사각형 ID받아주는 변수
        self.protocol("WM_DELETE_WINDOW", self.Close)
        self.configure(bg="#c0d0ff")
        self.font = font.Font(family="HY엽서M", size=9, weight="bold")
        self.font2 = font.Font(family="HY엽서M", size=9)
        for animal in ZooData.nameList:
            btList.append(tk.Button(self, text=animal, font=self.font, bg="#a0a0ff", relief="groove"))
            lbList.append(tk.Label(self, text=format(ZooData.GetBuyCost(animal), ",") + "원", font=self.font2, bg="#c0d0ff"))
            self.photoList.append(ZooData.GetPreviewPhoto(animal))
            self.previewList.append(tk.Canvas(self, width=100, height=100, bg="#c0d0ff", highlightthickness=0))

        for index in range(len(ZooData.nameList)):
            btList[index].place(x=(50 + (160 * (index // 8))), y=(50 + (50 * (index % 8))))
            lbList[index].place(x=(105 + (160 * (index // 8))), y=(50 + (50 * (index % 8))))
            self.previewList[index].create_image(20, 20, image=self.photoList[index], anchor="nw")

        self.zoo = zoo
        self.x = x
        self.y = y
        w = 400
        h = 500
        x1 = (self.root.winfo_screenwidth() // 2) - (w // 2)
        y1 = (self.root.winfo_screenheight() // 2) - (h // 2)
        self.geometry("%dx%d+%d+%d" % (w, h, x1, y1))
        self.animal = None
        self.num = 0

        self.text = tk.StringVar()
        self.lbNum = tk.Label(self, textvariable=self.text, font=self.font2, bg="#c0d0ff")
        self.lbNum.place(x=250, y=420)
        self.lbMary = tk.Label(self, text=" 마리", font=self.font2, bg="#c0d0ff")
        self.lbMary.place(x=275, y=420)
        btBuy = tk.Button(self, text="구입", command=lambda: self.Buy(), font=self.font, bg="#a0a0ff", relief="groove")
        btBuy.place(x=325, y=415)

        for index, name in enumerate(ZooData.nameList):
            self.BtBind(btList[index], name)

    # 동물버튼에 이벤트를 bind
    def BtBind(self, bt, name):
        bt.configure(command=lambda: self.Select(name))

    # Select -> Buy를 하여 실제로 동물을 구매함
    def Buy(self):
        # 영역이 겹칠 경우 0
        # 영역을 벗어날 경우 1
        # 돈이 부족할 경우 2
        # 성공 했을 경우 3
        self.top.GroundClick(0)
        self.destroy()
        try:
            self.topFrame.delete(self.preview)
        except:
            return

        check = self.zoo.BuyAnimal(self.animal, self.num, self.x, self.y)
        if check == 0:
            tk.messagebox.showwarning("구입오류", "영역이 겹칩니다")
        elif check == 1:
            tk.messagebox.showwarning("구입오류", "영역이 동물원을 벗어납니다")
        elif check == 2:
            tk.messagebox.showwarning("구입오류", "돈이 부족합니다")
        else:
            self.top.AddBoundary()

    # 동물을 클릭 하여서 얼마나 추가할 지 정할 수 있음
    def Select(self, name):
        boundarySize = ZooData.GetBoundarySize(name)
        if self.num > 0 and not self.animal == name:
            self.previewList[ZooData.GetIndex(self.animal)].place_forget()
            self.num = 0
        self.num += 1
        self.animal = name
        self.text.set(self.num)

        if self.num == 1:
            try:
                self.topFrame.delete(self.preview)
                self.preview = self.topFrame.create_rectangle(self.x, self.y,
                                                              self.x + ZooData.GetBoundarySize(name),
                                                              self.y + ZooData.GetBoundarySize(name),
                                                              outline=ZooData.GetColor(name), width=5)
                self.previewList[ZooData.GetIndex(name)].place(x=200, y=300)
            except:
                self.preview = self.topFrame.create_rectangle(self.x, self.y,
                                                              self.x + ZooData.GetBoundarySize(name),
                                                              self.y + ZooData.GetBoundarySize(name),
                                                              outline=ZooData.GetColor(name), width=5)

    # 창을 닫을 때 미리보기를 없애줌
    def Close(self):
        self.top.GroundClick(0)
        self.destroy()
        try:
            self.topFrame.delete(self.preview)
        except:
            return

class boundaryFrame:
    def __init__(self, main, boundary):
        self.boundary = boundary
        self.IDList = []
        self.frame = tk.Canvas(main, width=boundary.x2 - boundary.x1,
                               height=boundary.y2 - boundary.y1,
                               bg=ZooData.GetColor(boundary.name),
                               highlightcolor="#000000", bd=0)
        self.frame.place(x=boundary.x1, y=boundary.y1)
        self.photoList = []
        for animal in self.boundary.animalList:
            self.photoList.append(ImageTk.PhotoImage(
                Image.open(animal.photo).resize((ZooData.GetImageSize(animal), ZooData.GetImageSize(animal)),
                                                Image.ANTIALIAS)))

        for index, animal in enumerate(self.boundary.animalList):
            animalid = self.frame.create_image(animal.x, animal.y,
                                               image=self.photoList[index], anchor="nw")
            self.IDList.append(animalid)

    def AddAnimal(self, animal):
        self.photoList.append(ImageTk.PhotoImage(
            Image.open(animal.photo).resize((ZooData.GetImageSize(animal), ZooData.GetImageSize(animal)),
                                            Image.ANTIALIAS)))
        animalid = self.frame.create_image(animal.x, animal.y, image=self.photoList[-1], anchor="nw")
        self.IDList.append(animalid)
        return animalid

    def Refresh(self):
        index = 0
        for id, animal in zip(self.IDList, self.boundary.animalList):
            self.photoList[index] = ImageTk.PhotoImage(
                Image.open(animal.photo).resize((ZooData.GetImageSize(animal), ZooData.GetImageSize(animal)),
                                                Image.ANTIALIAS))
            self.frame.itemconfig(id, image=self.photoList[index])
            index += 1

class AnimalWindow(tk.Toplevel):
    def __init__(self, top, root, topFrame, animal):
        super().__init__(top)
        self.overrideredirect(True)
        self.top = top
        self.root = root
        self.topFrame = topFrame
        self.animal = animal
        self.configure(bg="#c0d0ff")
        self.focus()
        self.font = font.Font(family="HY엽서M", size=10)

        w = 200
        h = 300
        x = (self.root.winfo_screenwidth() // 2) + (w * 1.9)
        y = (self.root.winfo_screenheight() // 2) + (h * 0.05)
        self.geometry("%dx%d+%d+%d" % (w, h, x, y))

        # 기본 정보 출력 라벨
        self.lbName = tk.Label(self, text="이름 : " + str(animal.nameIndex), font=self.font, bg="#c0d0ff")
        self.lbName.place(x=28, y=20)
        self.lbSex = tk.Label(self, text="성별 : " + ZooData.GetSex(animal), font=self.font, bg="#c0d0ff")
        self.lbSex.place(x=28, y=45)
        self.lbAge = tk.Label(self, text="나이 : " + str(animal.age), font=self.font, bg="#c0d0ff")
        self.lbAge.place(x=28, y=70)
        self.lbHunger = tk.Label(self, text="배고픔 : " + str(animal.hungry), font=self.font, bg="#c0d0ff")
        self.lbHunger.place(x=28, y=95)
        self.lbDirty = tk.Label(self, text="청결도 : " + str(animal.dirty), font=self.font, bg="#c0d0ff")
        self.lbDirty.place(x=28, y=120)
        self.lbHealth = tk.Label(self, text="건강 : " + str(animal.health), font=self.font, bg="#c0d0ff")
        self.lbHealth.place(x=28, y=145)

        # 세부 정보 출력 라벨
        self.lbBBHealth = tk.Label(self, text="타고난 건강 : " + str(animal.bebornHealth), font=self.font, bg="#c0d0ff")
        self.lbBBHealth.place(x=28, y=175)
        self.lbBBHunger = tk.Label(self, text="타고난 식성 : " + str(animal.bebornHunger), font=self.font, bg="#c0d0ff")
        self.lbBBHunger.place(x=28, y=200)
        self.lbPersonality = tk.Label(self, text="성격 : " + str(animal.GetPersonality()), font=self.font, bg="#c0d0ff")
        self.lbPersonality.place(x=28, y=225)
        self.lbCost = tk.Label(self, text="현재 가치 : " + format(ZooData.GetSellCost(animal), ",")+"원", font=self.font, bg="#c0d0ff")
        self.lbCost.place(x=28, y=250)

        self.bind("<FocusOut>", lambda _: self.CloseTop())

        self.Refresh()

    def Refresh(self):
        self.lbAge.configure(text="나이 : " + str(self.animal.age))
        self.lbHunger.configure(text="배고픔 : " + str(self.animal.hungry))
        self.lbDirty.configure(text="청결도 : " + str(self.animal.dirty))
        self.lbHealth.configure(text="건강 : " + str(self.animal.health))
        self.lbCost.configure(text="현재 가치 : " + format(ZooData.GetSellCost(self.animal), ",")+"원")

        self.after(200, self.Refresh)

    def CloseTop(self):
        self.destroy()

class EscWindow(tk.Toplevel):
    def __init__(self, top, root, topFrame, zoo):
        super().__init__(top)
        self.top = top
        self.root = root
        self.topFrame = topFrame
        self.zoo = zoo
        self.font = font.Font(family="휴먼매직체", size=24, weight="bold")
        self.font2 = font.Font(family="HY엽서M", size=11)
        self.font3 = font.Font(family="HY엽서M", size=10)

        self.Frame = tk.Frame(self, width=650, height=500, bg="#d0d0ca")
        self.scrollbar = tk.Scrollbar(self.Frame)
        self.animalListbox = tk.Listbox(self, yscrollcommand=self.scrollbar.set, font=self.font3, width=45, height=8, bg="#d0d0ca")

        self.animalListbox.insert(0,"{0:<6} {1:>6} {2:>6} {3:>6} {4:>6}".format("이름","나이","배고픔","청결도","건강"))

        for boundary in self.zoo.boundaryList:
            for i, animal in enumerate(boundary.animalList):
                self.animalListbox.insert(i+1,
                       "{0:<6} {1:>6} {2:>7} {3:>7} {4:>7}".format(animal.nameIndex,
                           str(animal.age) + "살", str(animal.hungry),
                           str(animal.dirty), str(animal.health)))


        self.scrollbar["command"] = self.animalListbox.yview
        self.Frame.place(x=0, y=0)

        w = 650
        h = 500
        x1 = (self.root.winfo_screenwidth() // 2) - (w // 2)
        y1 = (self.root.winfo_screenheight() // 2) - (h // 2)
        self.geometry("%dx%d+%d+%d" % (w, h, x1, y1))
        self.configure(bg="#d0d0ca")

        self.btSave = tk.Button(self.Frame, text="저장하기", width=10, height=1, font=self.font, command=self.Save)
        self.btStatus = tk.Button(self.Frame, text="통계 보기", width=10, height=1, font=self.font,
                                  command=self.Status)
        self.btEnd = tk.Button(self.Frame, text="종료하기", width=10, height=1, font=self.font, command=self.ProgramExit)
        self.btSave.place(x=225, y=100)
        self.btStatus.place(x=225, y=200)
        self.btEnd.place(x=225, y=300)
        self.lbLine = tk.Label(self.Frame, text="───────────────────────────────────────────────────────", bg="#d0d0ca")
        self.lbLine2 = tk.Label(self.Frame, text="───────────────────────────────────────────────────────", bg="#d0d0ca")
        self.lbLine3 = tk.Label(self.Frame, text="───────────────────────────────────────────────────────", bg="#d0d0ca")

        self.protocol("WM_DELETE_WINDOW", self.Close)

    def Status(self):
        self.btSave.place_forget()
        self.btStatus.place_forget()
        self.btEnd.place_forget()

        self.lb1 = tk.Label(self.Frame, text="현재 보유 동물:", font=self.font3, bg="#d0d0ca")
        self.lb1.place(x=15, y=80)
        self.lb2 = tk.Label(self.Frame, text="현재 총 수입: ", font=self.font3, bg="#d0d0ca")
        self.lb2.place(x=15, y=200)
        self.lb3 = tk.Label(self.Frame, text="현재 총 지출: ", font=self.font3, bg="#d0d0ca")
        self.lb3.place(x=15, y=300)
        self.lb4 = tk.Label(self.Frame, text="손님 수: ", font=self.font3, bg="#d0d0ca")
        self.lb4.place(x=15, y=400)
        self.lb5 = tk.Label(self.Frame, text="입장료", font=self.font3, bg="#d0d0ca")
        self.lb5.place(x=120, y=200)
        self.lb6 = tk.Label(self.Frame, text="동물 판매", font=self.font3, bg="#d0d0ca")
        self.lb6.place(x=220, y=200)
        self.lb7 = tk.Label(self.Frame, text="총 합", font=self.font3, bg="#d0d0ca")
        self.lb7.place(x=540, y=200)
        self.lbLine.place(x=0, y=185)
        self.lb8 = tk.Label(self.Frame, text="동물 구매", font=self.font3, bg="#d0d0ca")
        self.lb8.place(x=120, y=300)
        self.lb9 = tk.Label(self.Frame, text="먹이값", font=self.font3, bg="#d0d0ca")
        self.lb9.place(x=240, y=300)
        self.lb10 = tk.Label(self.Frame, text="토지 확장값", font=self.font3, bg="#d0d0ca")
        self.lb10.place(x=330, y=300)
        self.lb11 = tk.Label(self.Frame, text="치료비", font=self.font3, bg="#d0d0ca")
        self.lb11.place(x=450, y=300)
        self.lb12 = tk.Label(self.Frame, text="총 합", font=self.font3, bg="#d0d0ca")
        self.lb12.place(x=540, y=300)
        self.lb13 = tk.Label(self.Frame, text="누적 손님 수", font=self.font3, bg="#d0d0ca")
        self.lb13.place(x=250, y=400)
        self.lb14 = tk.Label(self.Frame, text="하루 손님 수", font=self.font3, bg="#d0d0ca")
        self.lb14.place(x=120, y=400)
        self.lbLine2.place(x=0, y=280)

        self.lbicCustomer = tk.Label(self.Frame, text="+"+self.zoo.GeticCustomer()+"원", font=self.font3, bg="#d0d0ca")
        self.lbicCustomer.place(x=120, y=250)
        self.lbicAnimalSell = tk.Label(self.Frame, text="+"+self.zoo.GeticAnimalSell()+"원", font=self.font3, bg="#d0d0ca")
        self.lbicAnimalSell.place(x=220, y=250)
        self.lbTotalIncome = tk.Label(self.Frame, text="+"+self.zoo.GetTotalIncome()+"원", font=self.font3, bg="#d0d0ca")
        self.lbTotalIncome.place(x=540, y=250)
        self.lbocAnimalBuy = tk.Label(self.Frame, text="-"+self.zoo.GetocAnimalBuy()+"원", font=self.font3, bg="#d0d0ca")
        self.lbocAnimalBuy.place(x=120, y=350)
        self.lbocBuyFood = tk.Label(self.Frame, text="-"+self.zoo.GetocBuyFood()+"원", font=self.font3, bg="#d0d0ca")
        self.lbocBuyFood.place(x=240, y=350)
        self.lbocBuyLand = tk.Label(self.Frame, text="-"+self.zoo.GetocBuyLand()+"원", font=self.font3, bg="#d0d0ca")
        self.lbocBuyLand.place(x=330, y=350)
        self.lbocAnimalCure = tk.Label(self.Frame, text="-"+self.zoo.GetocAnimalCure()+"원", font=self.font3, bg="#d0d0ca")
        self.lbocAnimalCure.place(x=450, y=350)
        self.lbTotalOutcome = tk.Label(self.Frame, text="-"+self.zoo.GetTotalOutcome()+"원", font=self.font3, bg="#d0d0ca")
        self.lbTotalOutcome.place(x=540, y=350)
        self.lbTotalCustomer = tk.Label(self.Frame, text=self.zoo.GetTotalCustomer(), font=self.font3, bg="#d0d0ca")
        self.lbTotalCustomer.place(x=250, y=420)
        self.lbDailyCustomer = tk.Label(self.Frame, text=self.zoo.GetDailyCustomer(), font=self.font3, bg="#d0d0ca")
        self.lbDailyCustomer.place(x=120, y=420)
        self.lbLine3.place(x=0, y=380)
        self.animalListbox.place(x=160, y=12)

        self.btOK = tk.Button(self.Frame, text="확인", width=5, height=1, font=self.font2, command=self.Place)
        self.btOK.place(x=300, y=460)

    def Place(self):
        self.animalListbox.place_forget()
        self.btOK.place_forget()
        self.lb1.place_forget()
        self.lb2.place_forget()
        self.lb3.place_forget()
        self.lb4.place_forget()
        self.lb5.place_forget()
        self.lb6.place_forget()
        self.lb7.place_forget()
        self.lb8.place_forget()
        self.lb9.place_forget()
        self.lb10.place_forget()
        self.lb11.place_forget()
        self.lb12.place_forget()
        self.lb13.place_forget()
        self.lb14.place_forget()

        self.lbicCustomer.place_forget()
        self.lbicAnimalSell.place_forget()
        self.lbTotalIncome.place_forget()
        self.lbocAnimalBuy.place_forget()
        self.lbocBuyFood.place_forget()
        self.lbocBuyLand.place_forget()
        self.lbocAnimalCure.place_forget()
        self.lbTotalOutcome.place_forget()
        self.lbTotalCustomer.place_forget()
        self.lbDailyCustomer.place_forget()
        self.lbLine.place_forget()
        self.lbLine2.place_forget()
        self.lbLine3.place_forget()
        self.btSave.place(x=225, y=100)
        self.btStatus.place(x=225, y=200)
        self.btEnd.place(x=225, y=300)

    def Close(self):
        self.destroy()
        self.top.escFlag = 0

    # 상태를 저장
    def Save(self):
        types = [("zoo file", ".zoo")]
        file = filedialog.asksaveasfilename(filetypes=types, title="상태 저장", initialfile=str(self.zoo.date) + ".zoo")
        if file == "":
            self.top.escFlag = 0
            return
        with open(file, "wb") as F:
            pickle.dump(self.zoo, F, pickle.HIGHEST_PROTOCOL)
            self.top.escFlag = 0

    def ProgramExit(self):
        exit()