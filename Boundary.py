from ZooData import *
from Animal import *
class Boundary:
    def __init__(self, name, num, x, y):
        #animalList에 Animal객체가 append 되어서 들어감
        self.animalList = []
        self.animalCount = 0
        #name은 어떤 동물의 우리인지 나타냄 ex)"lion", "tiger" ...
        self.name = name

        #왼쪽위는 (x1, y1), 오른쪽 아래는 (x2, y2)
        self.x1 = x
        self.y1 = y
        self.x2 = x + ZooData.GetBoundarySize(self)
        self.y2 = y + ZooData.GetBoundarySize(self)

        for i in range(num):
            self.animalCount += 1
            self.animalList.append(Animal(name, self.animalCount))

    #animalList에서 Animal객체를 삭제 후 삭제한 index값을 반환
    def SellAnimal(self, animal):
        index = self.animalList.index(animal)
        self.animalList.remove(animal)
        return index

    #Zoo의 AddAnimal에서 불러주는 함수
    def AddAnimal(self):
        self.animalCount += 1
        animal = Animal(self.name, self.animalCount)
        self.animalList.append(animal)
        return animal
