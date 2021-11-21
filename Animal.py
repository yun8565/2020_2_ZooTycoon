from ZooData import *
import random
import tkinter.messagebox

class Animal:
    def __init__(self, name, index):
        #name은 "lion", "tiger" 이런 식으로 string임
        self.name = name
        self.nameIndex = name+str(index)

        #age는 1달에 1씩 올라가며 0부터 시작
        self.age = 0
        #1이면 암컷, 0이면 수컷
        self.sex = random.randint(0, 1)

        #값이 높을수록 건강
        self.hungry = 100
        self.health = 100
        self.dirty = 100

        #동물의 우리 내에서의 위치를 표시,
        # 생성시에는 우리 내에서 랜덤한 위치에 존재
        self.x = random.randint(0, ZooData.GetBoundarySize(self) - ZooData.GetImageSize(self) - 10)
        self.y = random.randint(0, ZooData.GetBoundarySize(self) - ZooData.GetImageSize(self) - 10)

        #값이 높을 수록 값의 변동이 커지는 것임
        self.bebornHunger = random.randint(0, 5)    #hungry와 연관
        self.bebornHealth = random.randint(0, 5)    #health와 연관
        self.personality = random.randint(0, 5)     #hungry, dirty와 연관
        
        #GUI에서 사진을 쓰기 위해
        self.photo = ZooData.GetPhoto(self)

        self.disease = False

    def Month(self):
        self.age += 1
        self.photo = ZooData.GetPhoto(self)

    #hungry, dirty, health 등을 1시간에 따라 조정해준다.
    def Condition(self):
        if self.personality == 0:   #활발한
            randomHungry = random.randint(3, 3 + (self.bebornHunger))
        elif self.personality == 1: #얌전한
            randomHungry = random.randint(1, 1 + (self.bebornHunger))
        else:
            randomHungry = random.randint(2, 2 + (self.bebornHunger))

        randomHungry = (randomHungry // 2) + 1

        if (self.hungry - randomHungry) > 0:
            self.hungry -= randomHungry
        else:
            self.hungry = 0

        if self.personality == 2:   #지저분한
            randomDirty = random.randint(3, 6)
        elif self.personality == 3: #깔끔한
            randomDirty = random.randint(1, 2)
        else:
            randomDirty = random.randint(2, 4)

        self.dirty -= randomDirty
        if self.dirty < 0:
            self.dirty = 0

        if self.hungry > 50 and self.dirty > 50:
            self.health += (2 + self.bebornHealth)//2
        if self.health > 100:
            self.health = 100

        if self.health <= 50 and self.bebornHealth <= 2:
            randomDisease = random.randint(1, 100)
            if randomDisease <= 2 and self.disease == False:  #2퍼센트의 확률로 질병
                self.disease = True
                tkinter.messagebox.showwarning("알림", self.nameIndex + "이 병에 걸렸습니다.")

        if self.hungry == 0:
            self.health -= (7 - self.bebornHealth)//2
        if self.dirty == 0:
            self.health -= (7 - self.bebornHealth)//2

    #성격요소 string으로 반환
    def GetPersonality(self):
        if self.personality == 0:
            return "활발한"
        elif self.personality == 1:
            return "얌전한"
        elif self.personality == 2:
            return "지저분한"
        else:
            return "깔끔한"
    
    #x, y 좌표를 이동
    def Move(self):
        # 움직이기 전 좌표
        x1 = self.x
        y1 = self.y

        # 움직일지 가만히 있을지 결정
        move = random.randint(0, 5)

        #병에 걸릴 경우 가만히 있음
        if self.disease:
            return x1, y1, x1, y1

        if self.personality == 0:
            self.x += random.randint(-20, 20)
        elif self.personality == 1:
            if move == 0:
                self.x += random.randint(-8, 8)
        else:
            self.x += random.randint(-10, 10)
        if self.x > ZooData.GetBoundarySize(self) - ZooData.GetImageSize(self) - 10:
            self.x = ZooData.GetBoundarySize(self) - ZooData.GetImageSize(self) - 10
        elif self.x < 0:
            self.x = 0

        if self.personality == 0:
            self.y += random.randint(-20, 20)
        elif self.personality == 1:
            self.y += random.randint(-3, 3)
        else:
            self.y += random.randint(-8, 8)
        if self.y > ZooData.GetBoundarySize(self) - ZooData.GetImageSize(self) - 10:
            self.y = ZooData.GetBoundarySize(self) - ZooData.GetImageSize(self) - 10
        elif self.y < 0:
            self.y = 0

        return x1, y1, self.x, self.y

    #먹이주기
    def Feed(self):
        self.hungry += 50
        if self.hungry > 100:
            self.hungry = 100
    #씻겨주기
    def Wash(self):
        self.dirty = 100
    #치료하기
    def Cure(self):
        if self.disease == False:
            return False
        self.disease = False
        self.health = 100
        self.hungry = 100
        self.dirty = 100
