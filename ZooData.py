from PIL import ImageTk, Image
import pandas as pd
import random
import datetime

class ZooData:
    nameList = ["호랑이", "사자", "원숭이", "곰",
                "북극곰", "공작", "악어", "코끼리",
                "판다", "사슴", "독수리", "물개", "토끼"]
    boundarySizeList = [3, 3, 2, 3,
                        4, 2, 3, 5,
                        4, 3, 2, 4, 2]
    colorList = ["#f4ac1e", "#f4ac1e", "#f4ac1e", "#dedfa3",
                 "#b8dce4", "#37cc17", "#c4b36f", "#f4ac1e",
                 "#7cd10a", "#f4ac1e", "#95e0fd", "#39e4fd", "#37cc17"]
    buyCostList = [5000000, 5000000, 1000000, 3000000,
                   10000000, 2000000, 2500000, 20000000,
                   15000000, 500000, 1000000, 1500000, 200000]
    maxAgeList = [30, 30, 20, 30,
                  30, 20, 50, 60,
                  30, 20, 35, 30, 10]
    imageSizeList = [[2, 2, 5], [2, 3, 4], [2, 3, 3], [2, 3, 5],
                     [2, 3, 5], [2, 2, 3], [2, 3, 4], [4, 5, 6],
                     [2, 4, 4], [2, 2, 3], [2, 3, 3], [2, 3, 4], [1, 2, 2]]
    foodCostList = [[2000, 3000, 5000], [2000, 3000, 5000], [1000, 1500, 2000], [2000, 3000, 5000],
                    [2000, 3000, 5000], [500, 1000, 1500], [1500, 2500, 4000], [5000, 10000, 20000],
                    [2500, 4000, 6000], [500, 1000, 1500], [500, 500, 100], [1500, 2500, 4000], [100, 200, 300]]

    weather = ["맑음", "흐림", "비", "구름조금", "구름많음", "눈", "천둥번개"]

    weatherProbability = pd.read_excel("weather.xlsm", sheet_name = "Result").values.tolist()
    maxTime = 24 * 20  # 24 * n에서 (n/2)초에 1시간이 흐름, 즉 maxTime초/2 만큼이 하루임
    @staticmethod
    def GetIndex(animal):
        try:        #Animal객체또는 Boundary객체를 받을 경우
            return ZooData.nameList.index(animal.name)
        except:     #animalName을 인자로 받을 경우
            return ZooData.nameList.index(animal)
    @staticmethod
    def GetName(animal):
        return ZooData.nameList[ZooData.GetIndex(animal)]
    @staticmethod
    def GetSex(animal):
        if animal.sex == 0:
            return "수컷"
        else:
            return "암컷"
    @staticmethod
    def GetBoundarySize(animal):
        return ZooData.boundarySizeList[ZooData.GetIndex(animal)] * 80
    @staticmethod
    def GetColor(animal):
        return ZooData.colorList[ZooData.GetIndex(animal)]
    @staticmethod
    def GetBuyCost(animal):
        return ZooData.buyCostList[ZooData.GetIndex(animal)]
    @staticmethod
    def GetMaxAge(animal):
        return ZooData.maxAgeList[ZooData.GetIndex(animal)]
    @staticmethod
    def GetImageSize(animal):
        select = 0
        if animal.age <= int(ZooData.GetMaxAge(animal) * 0.1):
            select = 1
        elif animal.age <= int(ZooData.GetMaxAge(animal) * 0.3):
            select = 2
        else:
            select = 3
        return ZooData.imageSizeList[ZooData.GetIndex(animal)][select-1] * 15
    @staticmethod
    def GetPhoto(animal):
        select = 0
        if animal.age <= int(ZooData.GetMaxAge(animal) * 0.1):
            select = 1
        elif animal.age <= int(ZooData.GetMaxAge(animal) * 0.3):
            select = 2
        else:
            select = 3

        #사자 일 경우 m과 f를 나눔
        lion = ""
        if animal.name == "사자" and select >= 2:
            if animal.sex == 0:
                lion = "m_"
            else:
                lion = "f_"

        return "./image/" + lion + animal.name + str(select) + ".png"

    @staticmethod
    def GetPreviewPhoto(name):
        if name == "사자":
            image = ImageTk.PhotoImage(Image.open("./image/m_" + name + "3.png").resize((80,80),Image.ANTIALIAS))
        else:
            image = ImageTk.PhotoImage(Image.open("./image/"+name+"3.png").resize((80,80), Image.ANTIALIAS))
        return image
    @staticmethod
    def SetWeather(zoo):
        probability = random.randint(1, 100)               #1~100의 수를 생성
        tmpTime = datetime.date(zoo.date.year, 1, 1)
        timeInterval = zoo.date - tmpTime
        gap5 = 1 + ( (timeInterval.days)//5)               #zoo.date의 날짜를 일 형식으로 바꾸고 5일 간격으로 나눔 ex)2019.02.02 -> 1월*30 + 2월 2 -> 31 // 5
        accumulation = ZooData.weatherProbability[0][gap5]*5
        accumulation = int(accumulation)
        if probability <= accumulation:                        #sunny
            zoo.weatherState = ZooData.weather[0]
        else:
            accumulation += (ZooData.weatherProbability[1][gap5]*5)
            if probability <= accumulation:                    #cloudy
                zoo.weatherState = ZooData.weather[1]
            else:
                accumulation += (ZooData.weatherProbability[2][gap5]*5)
                if probability <= accumulation:                #rainy
                    lightningProbability = random.randint(1, 100)
                    if lightningProbability <= 10:             #lightning
                        zoo.weatherState = ZooData.weather[6]
                    else:
                        zoo.weatherState = ZooData.weather[2]
                else:
                    accumulation += (ZooData.weatherProbability[3][gap5]*5)
                    if probability <= accumulation:            #bitCloudy
                        zoo.weatherState = ZooData.weather[3]
                    else:
                        accumulation += (ZooData.weatherProbability[4][gap5] * 5)
                        if probability <= accumulation:        #manyCloudy
                            zoo.weatherState = ZooData.weather[4]
                        else:                                  #snow
                            zoo.weatherState = ZooData.weather[5]
        return
    @staticmethod
    def GetWeather(zoo):
        return zoo.weatherState
    @staticmethod
    def GetSellCost(animal):
        #동물의 bebornHealth가 높을수록 가격 증가
        #동물의 bebornHunger가 낮을수록 가격 증가
        #동물의 나이가 Maxage의 절반에 가까울수록 가격 증가
        cost = ZooData.GetBuyCost(animal)*0.8
        cost += ZooData.GetBuyCost(animal)*0.4*(animal.bebornHealth * 0.3)
        cost -= ZooData.GetBuyCost(animal)*0.4*(animal.bebornHunger * 0.1)
        cost -= ZooData.GetBuyCost(animal)*(abs(animal.age - (ZooData.GetMaxAge(animal)//2))*0.01)
        cost = int(cost)
        return cost
    @staticmethod
    def GetNowTime(zoo):
        now = 1440 * (zoo.time / ZooData.maxTime)
        hour = now // 60
        minute = now % 60
        return hour, minute
    @staticmethod
    def GetFoodCost(animal):
        select = 0
        if animal.age <= int(ZooData.GetMaxAge(animal) * 0.1):
            select = 0
        elif animal.age <= int(ZooData.GetMaxAge(animal) * 0.3):
            select = 1
        else:
            select = 2
        return ZooData.foodCostList[ZooData.GetIndex(animal)][select]
    @staticmethod
    def GetCureCost(animal):
        return int(ZooData.GetBuyCost(animal) * 0.1)
    @staticmethod
    def GetScore(animal):
        return (int(ZooData.GetBuyCost(animal)) * 0.00001)