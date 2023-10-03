import json

with open("data.json", "r", encoding="utf8") as read_file:
    data = json.load(read_file)

cards = data["r"]["dbiAccessorRes"]["tables"][20]["data_rows"] # Cards
lessons = data["r"]["dbiAccessorRes"]["tables"][18]["data_rows"] # Lessons info
daydefs = data["r"]["dbiAccessorRes"]["tables"][4]["data_rows"] # Day Definitions
classrooms = data["r"]["dbiAccessorRes"]["tables"][11]["data_rows"] # Classes
groups = data["r"]["dbiAccessorRes"]["tables"][15]["data_rows"] # Groups
classes = data["r"]["dbiAccessorRes"]["tables"][12]["data_rows"] # Classes
subjects = data["r"]["dbiAccessorRes"]["tables"][13]["data_rows"] # Subject

daysOfWeek = {
    "100000": "Monday",
    "010000": "Tuesday",
    "001000": "Wednesday", 
    "000100": "Thursday",
    "000010": "Friday",
    "000001": "Saturday", 
}

periods = {
    "0": "09:30",
    "1": "10:00",
    "2": "10:30",
    "3": "11:00",
    "4": "11:30",
    "5": "12:00",
    "6": "12:30",
    "7": "13:00",
    "8": "13:30",
    "9": "14:00",
    "10": "14:30",
    "11": "15:00",
    "12": "15:30",
    "13": "16:00",
    "14": "16:30",
    "15": "17:00",
    "16": "17:30",
    "17": "18:00",
    "18": "18:30",
    "19": "19:00",
    "20": "19:30"
}

def timetable(classid):
    week = {}
    week["Monday"] = []
    week["Tuesday"] = []
    week["Wednesday"] = []
    week["Thursday"] = []
    week["Friday"] = []
    week["Saturday"] = []

    groupList = []
    cardList = []
    subjectList = []
    subjectDict = {}
    lessonList = []
    lessonSubjectDict = {}
    lessonPeriodDict = {}
    classroomList = []
    classroomDict = {}
    classData = {}

    for classElem in classes:
        if classElem["id"] == classid:
            week["groupName"] = classElem["name"]

    for group in groups:
        if group["classid"] == classid:
            groupList.append(group["id"])

    for lesson in lessons:
        for lessonGroup in lesson["groupids"]:
            if lessonGroup in groupList:
                a = int(lesson["durationperiods"])/int(lesson["count"])*2
                b = int(lesson["durationperiods"])/int(lesson["count"])
                lessonSubjectDict[lesson["id"]] = lesson["subjectid"]
                lessonPeriodDict[lesson["id"]] = a if a > 1.0 else b
                lessonList.append(lesson["id"])
                subjectList.append(lesson["subjectid"])
    
    for subject in subjects:
        if subject["id"] in subjectList:
            subjectDict[subject["id"]] = subject["name"]
    
    for card in cards:
        if card["lessonid"] in lessonList:
            classroomList.append(card["classroomids"][0])
            # print(f'{daysOfWeek[card["days"]]} - {periods[str(int(card["period"])-1)]} - {subjectDict[lessonSubjectDict[card["lessonid"]]]} - {card["classroomids"][0]}')
    
    for classroom in classrooms:
        if classroom["id"] in classroomList:
            classroomDict[classroom["id"]] = classroom["short"]
   
    for card in cards:
        classData = {}
        if card["lessonid"] in lessonList:
            classData["start"] = periods[str(int(card["period"])-1)]
            classData["period"] = lessonPeriodDict[card["lessonid"]]
            classData["subject"] = subjectDict[lessonSubjectDict[card["lessonid"]]]
            classData["classroom"] =  classroomDict[card["classroomids"][0]]
            
            if daysOfWeek[card["days"]] == "Monday":
                week["Monday"].append(classData)
            
            if daysOfWeek[card["days"]] == "Tuesday":
                week["Tuesday"].append(classData)
            
            if daysOfWeek[card["days"]] == "Wednesday":
                week["Wednesday"].append(classData)
            
            if daysOfWeek[card["days"]] == "Thursday":
                week["Thursday"].append(classData)
            
            if daysOfWeek[card["days"]] == "Friday":
                week["Friday"].append(classData)
            
            if daysOfWeek[card["days"]] == "Saturday":
                week["Saturday"].append(classData)
            
    print(week)

timetable("*13")
