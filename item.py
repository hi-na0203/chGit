from dataclasses import dataclass

@dataclass
class Item:
    chArea: str
    date: str
    startTime: str
    endTime: str
    title: str

    def __init__(self, chArea, date, startTime, endTime, title):
        self.chArea = chArea
        self.date = date
        self.startTime = startTime
        self.endTime = endTime
        self.title = title