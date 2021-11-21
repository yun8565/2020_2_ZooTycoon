from Boundary import *
import datetime
import heapq
import math

class Zoo:
    maxGround = 0
    ground = []
    date = None
    money = 0
    DayCustomer = 0  # 하루 누적 고객수
    totalCustomer = 0  #누적 고객 수
    boundaryList = []
    weatherState = None
    time = 0
    buyLandCost = 100000000  # 초기에는 1억

    customerQueue = []  # 우선순위 큐를 이용한 현재 고객
    score = 0  # 현재 동물원의 점수
    maxInt = 100  # 고객이 올 확률을 조절

    def __init__(self):
        # 가로 1600픽셀, 세로 1600픽셀로 지정
        self.maxGround = 1600

        # ground는 2차원 list로
        # 해당 구역에 boundary가
        # 존재하는지, 존재하지 않는지 검사 하기 위함
        self.ground = []
        for i in range(self.maxGround):
            tmp = []
            for j in range(self.maxGround):
                tmp.append(False)
            self.ground.append(tmp)
        # date는 datetime.date라는 포맷을 이용
        self.date = datetime.date(2020, 12, 31)

        # 돈은 처음에 1억을 가지고 시작
        self.money = 100000000

        self.icAnimalSell = 0
        self.icCustomer = 0
        self.ocAnimalBuy = 0
        self.ocBuyFood = 0
        self.ocAnimalCure = 0
        self.ocBuyLand = 0

        self.DayCustomer = 0  # 일간 고객

        # Boundary객체를 저장하는 배열
        self.boundaryList = []

        # 현재 날씨 상태
        self.weatherState = "snow"
        ZooData.SetWeather(self)

        # time이 일정 수치가 되면 SetTomorrow를 하고 0으로 초기화
        # time은 초마다 증가함
        self.time = 0
        self.buyLandCost = 100000000

        self.customerQueue = []
        self.score = 0

    #만약 우리의 마지막 동물을 SellAnimal 할 경우 인지 체크
    def Remove(self):   #boundary를 삭제해야되면 True반환
        for i in range(len(self.boundaryList)-1, -1, -1):
            if len(self.boundaryList[i].animalList) == 0:
                self.BoundaryRemove(self.boundaryList[i])
                return True
        return False
    #Remove에서 불리는 함수로써, ground를 False로 다시 바꿔 구역을 비워줌
    def BoundaryRemove(self, boundary):
        for i in range(boundary.x1, boundary.x2):
            for j in range(boundary.y1, boundary.y2):
                self.ground[j][i] = False
        self.boundaryList.remove(boundary)

    #동물 구매
    def BuyAnimal(self, animalName, num, x, y):
        # 영역이 겹칠 경우 0
        # 영역을 벗어날 경우 1
        # 돈이 부족할 경우 2
        # 성공 했을 경우 생성 된 boundary 객체를 반환한다

        try:    #우리가 겹칠 경우
            for i in range(x, x + ZooData.GetBoundarySize(animalName)):
                for j in range(y, y + ZooData.GetBoundarySize(animalName)):
                    if self.ground[j][i] == True:
                        return 0
        except: #영역을 벗어날 경우
            return 1

        #돈이 부족할 경우
        if self.money < (ZooData.GetBuyCost(animalName) * num):
            return 2

        #구입에 성공할 경우
        self.money -= (ZooData.GetBuyCost(animalName) * num)
        self.ocAnimalBuy += (ZooData.GetBuyCost(animalName) * num)
        newBoundary = Boundary(animalName, num, x, y)
        self.boundaryList.append(newBoundary)
        x1 = newBoundary.x1
        y1 = newBoundary.y1
        x2 = newBoundary.x2
        y2 = newBoundary.y2
        #구입 하고 난 후 Zoo의 ground를 일부분을 True로 바꾸어 준다
        for i in range(x1, x2):
            for j in range(y1, y2):
                self.ground[j][i] = True
        return newBoundary
    #동물 추가
    def AddAnimal(self, boundary):
        index = self.boundaryList.index(boundary)
        cost = ZooData.GetBuyCost(boundary)
        if self.money <= cost:
            return -1, -1
        animal = self.boundaryList[index].AddAnimal()    #Boundary의 AddAnimal을 불러준다
        self.money -= cost  #비용만큼 money에서 빼준다
        self.ocAnimalBuy += cost
        return index, animal
    #동물 판매
    def SellAnimal(self, animal):
        #Zoo클래스내에서 삭제한 animal객체의
        #boundaryList내의 Index
        #그 boundary의 몇 번째 animal인지 Index를 반환 해준다.
        boundaryIndex = -1
        flag = False
        for boundary in self.boundaryList:
            boundaryIndex += 1
            for anim in boundary.animalList:
                if animal == anim:
                    self.money += ZooData.GetSellCost(animal)
                    self.icAnimalSell += ZooData.GetSellCost(animal)
                    index = self.boundaryList[boundaryIndex].SellAnimal(animal)
                    flag = self.Remove()
                    return boundaryIndex, index, flag
    #우리에 먹이주기
    def FeedBoundary(self, boundary):
        costSum = 0
        for animal in boundary.animalList:
            costSum += ZooData.GetFoodCost(animal)
        if self.money < costSum:    #돈이 부족해서 살 수 없을 경우
            return False
        else:                       #돈이 충분할 경우
            self.money -= costSum
            self.ocBuyFood += costSum
            for animal in boundary.animalList:
                animal.Feed()
    #우리에 씻겨주기
    def WashBoundary(self, boundary):
        for animal in boundary.animalList:
            animal.Wash()
    #동물에게 먹이주기
    def FeedAnimal(self, animal):
        cost = ZooData.GetFoodCost(animal)
        if self.money < cost:    #돈이 부족해서 살 수 없을 경우
            return False
        else:
            self.money -= cost
            self.ocBuyFood += cost
            animal.Feed()
    #동물 씻겨주기
    def WashAnimal(self, animal):
        animal.Wash()
    #동물 치료
    def Cure(self, animal):
        if self.money < ZooData.GetCureCost(animal):    #치료할 돈이 없으면
            return 1
        else:
            check = animal.Cure()   #질병에 걸린 상태가 아니면 False
            if check == False:
                return 2
            else:
                self.money -= ZooData.GetCureCost(animal)
                self.ocAnimalCure += ZooData.GetCureCost(animal)

    # 날짜를 내일로 변경
    def SetTomorrow(self):
        self.SetScore()
        ZooData.SetWeather(self)
        beforeMonth = self.date.month  # 바뀌기 전 month를 저장
        self.date += datetime.timedelta(days=1)

        oneHour = int(ZooData.maxTime // 24)
        self.maxInt = 100
        if oneHour * 18 <= self.time:  # 시간이 18시를 넘을 경우
            self.maxInt *= 2

        weekday = self.date.isoweekday()  # 요일에 따라 확률을 지정
        if 1 <= weekday <= 4:  # 월~목
            self.maxInt *= 5
        elif weekday == 5:  # 금
            self.maxInt *= 3
        elif weekday == 6:  # 토
            self.maxInt *= 1.5
        elif weekday == 7:  # 일
            self.maxInt *= 1

        # ["맑음", "흐림", "비", "구름조금", "구름많음", "눈", "천둥번개"]
        if self.weatherState == "맑음":
            self.maxInt *= 1
        elif self.weatherState == "흐림":
            self.maxInt *= 3
        elif self.weatherState == "비":
            self.maxInt *= 4
        elif self.weatherState == "구름조금":
            self.maxInt *= 1.5
        elif self.weatherState == "구름많음":
            self.maxInt *= 2
        elif self.weatherState == "눈":
            self.maxInt *= 5
        elif self.weatherState == "천둥번개":
            self.maxInt *= 10

        if beforeMonth != self.date.month and beforeMonth != 12:
            return 2  # month가 바뀜을 알림
        if beforeMonth == 12 and beforeMonth != self.date.month:
            return 3  # year이 바뀜을 알림
        else:
            return 1

    # 점수를 갱신
    def SetScore(self):
        self.score = 0
        numBoundary = len(self.boundaryList)  # boundary의 수
        numAnimal = {}  # 각 동물의 수를 저장하기 위한 dictionary
        for animalName in ZooData.nameList:
            numAnimal[animalName] = 0

        for boundary in self.boundaryList:  # 해당하는 dictionary에 동물의 수만큼 더해줌
            num = len(boundary.animalList)
            numAnimal[boundary.name] += num

        numSpecies = 0
        for name in numAnimal:
            if numAnimal[name] > 0:
                numSpecies += 1  # 해당 동물종이 있으면 +1
            self.score += (ZooData.GetScore(name) * numAnimal[name])  # 각 동물에 대하여 점수를 매겨줌

        self.score *= (numBoundary * (numSpecies ** 2))
        self.score = int(math.log2(self.score))

    # 현재 고객의 수를 반환
    def GetCustomer(self):
        return str(len(self.customerQueue)) + "명"

    # 날짜를 string 형태로 return
    def GetDate(self):
        weekday = self.date.isoweekday()
        if weekday == 1:
            weekday = "월요일"
        elif weekday == 2:
            weekday = "화요일"
        elif weekday == 3:
            weekday = "수요일"
        elif weekday == 4:
            weekday = "목요일"
        elif weekday == 5:
            weekday = "금요일"
        elif weekday == 6:
            weekday = "토요일"
        elif weekday == 7:
            weekday = "일요일"

        return self.date.isoformat() + " " + weekday

    #돈 표기, string으로 반환
    def GetMoney(self):
        return format(self.money, ",") + "원"
    def GetWeather(self):
        return self.weatherState
    def GetTime(self):
        hour, minute = ZooData.GetNowTime(self)
        return "%02d" % int(hour) + ":" + "%02d" % int(minute)

    # 시간의 흐름 내일로 바뀔경우 True반환 그렇지 않으면 False
    def TikTok(self):
        if self.time == ZooData.maxTime:  # 24시간마다
            check = self.SetTomorrow()
            self.DayCustomer = 0  # 일간 고객수를 0으로 초기화
            self.time = 0
            if check == 2:  # month가 바뀔 경우
                return 2
            elif check == 3:  # year이 바뀔 경우
                return 3
            else:
                return 1
        elif self.time % (ZooData.maxTime // 24) == 0:  # 정각마다
            self.Hour()
            self.time += 1
            return -1
        else:  # 그 외
            self.time += 1
            return 0
    #정각마다 동물들의 상태를 업데이트
    def Hour(self):
        for boundary in self.boundaryList:
            for animal in boundary.animalList:
                animal.Condition()

    def Month(self):
        for boundary in self.boundaryList:
            for animal in boundary.animalList:
                animal.Month()

    def BuyLand(self):
        beforeMaxGround = self.maxGround
        if self.money < self.buyLandCost:
            return -1, -1  # 실패 시 -1, -1을 반환
        else:
            self.money -= self.buyLandCost
            self.ocBuyLand += self.buyLandCost
            self.buyLandCost *= 2  # 토지확장 비용을 늘린다
            self.maxGround += 400  # 토지를 가로, 세로 400씩 늘린다

            tmpGround = []
            for y in range(self.maxGround):
                tmp = []
                for x in range(self.maxGround):
                    tmp.append(False)
                tmpGround.append(tmp)

            for y in range(beforeMaxGround):
                for x in range(beforeMaxGround):
                    tmpGround[y][x] = self.ground[y][x]

            self.ground = tmpGround

            return beforeMaxGround, self.maxGround  # 성공시 이전 영역크기, 현재 영역크기를 반환

    # 고객이 입장하거나 빠져나가는 함수
    def Enter(self):
        oneHour = ZooData.maxTime // 24  # maxTime으로부터 1시간을 계산
        if self.time == oneHour * 22:  # 동물원 문 닫는 시간이면
            self.customerQueue = []  # 고객이 전부 나감

        if (oneHour * 0 <= self.time <= oneHour * 6) or \
                (oneHour * 22 <= self.time <= oneHour * 24):
            return  # 당일22시 ~ 익일 6시까지는 문을 닫음
        else:
            while len(self.customerQueue) != 0 and self.customerQueue[0] == self.time:  # 고객이 빠져나갈 시간이면
                heapq.heappop(self.customerQueue)

            if self.time == oneHour * 18:  # 18시 이후로는 고객이 올 확률이 절반이 됨
                self.maxInt *= 2

            for i in range(self.score):  # 분당 score 횟수 만큼 고객이 올 수도 안 올수도 있음
                probability = random.randint(1, self.maxInt)
                if probability <= self.score:  # score보다 작으면 손님이 입장
                    self.money += 10000  # 고객 한명당 입장료 10,000원
                    self.icCustomer += 10000
                    self.totalCustomer += 1
                    self.DayCustomer += 1
                    stayTime = random.randint(1, 4)
                    stayTime = int((oneHour * stayTime) / 2)  # 고객은 30분 ~ 2시간 동안 머무름
                    heapq.heappush(self.customerQueue, (self.time + stayTime))  # 고객이 떠날 시간을 우선순위 큐에 추가

    def GetCurrentAnimal(self):
        total = ""
        for boundary in self.boundaryList:
            total += boundary.name + ": " + str(len(boundary.animalList)) + "마리\n"
        return total

    # 토지 확장 돈 표기
    def GetBuyLandCost(self):
        return format(self.buyLandCost, ",") + "원"
    def GeticCustomer(self):
        return format(self.icCustomer, ",")
    def GeticAnimalSell(self):
        return format(self.icAnimalSell, ",")
    def GetocAnimalBuy(self):
        return format(self.ocAnimalBuy, ",")
    def GetocBuyFood(self):
        return format(self.ocBuyFood, ",")
    def GetocBuyLand(self):
        return format(self.ocBuyLand, ",")
    def GetocAnimalCure(self):
        return format(self.ocAnimalCure, ",")
    def GetTotalIncome(self):
        total = self.icCustomer + self.icAnimalSell
        return format(total, ",")
    def GetTotalOutcome(self):
        total = self.ocBuyLand + self.ocBuyFood + self.ocAnimalCure + self.ocAnimalBuy
        return format(total, ",")
    def GetTotalCustomer(self):
        return format(self.totalCustomer, ",")+"명"
    def GetDailyCustomer(self):
        return format(self.DayCustomer, ",")+"명"
