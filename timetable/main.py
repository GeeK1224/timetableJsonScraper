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

    groupList = []
    cardList = []
    subjectList = []
    subjectDict = {}
    subjectColorDict = {}
    lessonList = []
    lessonSubjectDict = {}
    lessonPeriodDict = {}
    classroomList = []
    classroomDict = {}
    classroomDict['no_class'] = 'no class'

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
                lessonSubjectDict[lesson["id"]] = lesson["subjectid"]
                lessonList.append(lesson["id"])
                subjectList.append(lesson["subjectid"])
                lessonPeriodDict[lesson["id"]] = int(lesson["durationperiods"])/2
                    

    for subject in subjects:
        if subject["id"] in subjectList:
            subjectDict[subject["id"]] = subject["short"]
            subjectColorDict[subject["id"]] = subject["color"]
    
    for card in cards:
        if card["lessonid"] in lessonList:
            try:
                classroomList.append(card["classroomids"][0])
            except IndexError:
                classroomList.append("no_class")
            # print(f'{daysOfWeek[card["days"]]} - {periods[str(int(card["period"])-1)]} - {subjectDict[lessonSubjectDict[card["lessonid"]]]} - {card["classroomids"][0]}')
    
    for classroom in classrooms:
        if classroom["id"] in classroomList:
            classroomDict[classroom["id"]] = classroom["name"]
   
    for card in cards:
        classData = {}
        if card["lessonid"] in lessonList:
            try:
                classData["start"] = periods[str(int(card["period"])-1)]
            except ValueError:
                classData["start"] = ""
            classData["period"] = lessonPeriodDict[card["lessonid"]]
            classData["subject"] = subjectDict[lessonSubjectDict[card["lessonid"]]]
            classData["color"] = subjectColorDict[lessonSubjectDict[card["lessonid"]]]
            try:
                classData["classroom"] =  classroomDict[card["classroomids"][0]]
            except:
                classData["classroom"] =  classroomDict["no_class"]
            
            if card["days"] != '':
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
            
    return week

classes = data["r"]["dbiAccessorRes"]["tables"][12]["data_rows"] # Classes
def groupIter():
    groupList = []
    for classElem in classes:
        print(f"{classElem['name']}:{classElem['id']}")

tim = timetable("*13")
print(tim)
# groupIter()
# print(tim)
# print(classes)