import json
from pathlib import Path
from datetime import datetime
from collections import deque

# file path for save
SAVE_PATH = Path("saves/city.json")

def timestamp():
    return("- (" + datetime.now().strftime("%H:%M") + ") ") 

class Person:
    def __init__(self, name, title):
        self.name = name
        self.title = title

    def __repr__(self):
        return f"Person(name={self.name!r}, title={self.title!r})"

    def to_dict(self):
        return {"name": self.name, "title": self.title}

    @classmethod
    def from_dict(cls, data):
        return cls(name=data.get("name", ""), title=data.get("title", ""))

class City:
    # list of valid buildings (not saved/loaded)
    building_list = ["Granary", "Smith", "Carpenter"]

    def __init__(self):
        self.name = "Jaine"
        self.wealth = 3
        self.stability = 3
        self.buildings = []  # list of building names
        self.characters = [Person("Jeoffrey Klingleton", "Head Elder")] # list of Person instances
        self.speaker = self.characters[0]

    def add_building(self, building_name):
        if building_name in City.building_list:
            self.buildings.append(building_name)
        else:
            raise ValueError(f"Unknown building: {building_name}")

    def __repr__(self):
        return (
            f"City(name={self.name!r}, wealth={self.wealth}, "
            f"stability={self.stability}, buildings={self.buildings!r}, "
            f"characters={self.characters!r}, speaker={self.speaker!r})"
        )

    # returns data to easily put in a json
    def to_dict(self):
        return {
            "wealth": self.wealth,
            "stability": self.stability,
            "buildings": list(self.buildings),
            "characters": [p.to_dict() for p in self.characters],
            "speaker": self.speaker.to_dict()
        }

    # Reads a city from json
    @classmethod
    def from_dict(cls, data):
        city = cls()
        city.wealth = data.get("wealth", city.wealth)
        city.stability = data.get("stability", city.stability)
        city.buildings = data.get("buildings", []).copy()
        city.characters = [Person.from_dict(d) for d in data.get("characters", [])]
    
        speaker_data = data.get("speaker")
        if speaker_data:
            for person in city.characters:
                if person.name == speaker_data.get("name"):
                    city.speaker = person
                    break
            else:
                # fallback: if no match, default to first character if any
                city.speaker = city.characters[0] if city.characters else None
        else:
            city.speaker = city.characters[0] if city.characters else None

        return city
    
    # assign a speaker to a character in the city. Is a pointer so changes to speaker will reflect in the character. 
    def assign_speaker(self, name):
        # loop through characters in the city
        for person in self.characters:
            if person.name == name:
                self.speaker = person
                return person

# Load the saved city from disk. If no save exists, create a new City and head-elder Person.
def load_city():
    if not SAVE_PATH.exists():
        # no save → just return the default City()
        return "None"
    raw = json.loads(SAVE_PATH.read_text())
    return City.from_dict(raw)

# Serialize the City to JSON, including buildings and characters.
def save_city(city):
    SAVE_PATH.parent.mkdir(exist_ok=True)
    SAVE_PATH.write_text(json.dumps(city.to_dict(), indent=2))

#describes things that are stored as scaled numbers
def Scale_descriptions(type, number):
    match type:
        # The stability in the city is ...
        case "stability":
            if number == 0:
                return "tumultuous"
            if number == 1:
                return "very bad"
            if number == 2:
                return "poor"
            if number == 3:
                return "alright"
            if number == 4:
                return "decent"
            if number == 5:
                return "incredible"

# options for the questions panel
def Questions(index):
    ID, page = index
    match ID:
        case "Main":
            if page == 0:
                return [
                    "1: Who are you?",
                    "2: How is the city doing in general?",
                    "3: What is the latest news?",
                    "4: How many people are in the city??",
                    "5: (next...)"
                ]
            elif page == 1:
                return [
                    "1: How are ongoing constructions?",
                    "2: How is city health?",
                    "3: How happy are the people?",
                    "4: Are there any other concerns?",
                    "5: (back...)"
                ]
    return []

def question_responses(index, key, city: City):
    page = index[0]
    level = index[1]
    match page,level,key:
        case "Main",0,"1":
            return f"I am {city.speaker.name}, the {city.speaker.title}."
        case "Main",0,"2":
            return f"My lord, the stability in the city is {Scale_descriptions("stability",city.stability)}!"
        case "Main",0,"3":
            return f"Not much has happened my lord. "
        case "Main",0,"4":
            return f"Not many my lord."
        case "Main",1,"1":
            return f"Nothing is being built right now my lord."
        case "Main",1,"2":
            return f"Everyone is healthy enough right now my lord."
        case "Main",1,"3":
            return f"They are alright my lord. "
        case "Main",1,"4":
            return f"No my lord."

# the options for the commands panel
def Commands(index):
    ID, page = index
    match ID:
        case "Main":
            if page == 0:
                return [
                    "q: Assign citizens to farming",
                    "w: Begin building project",
                    "e: Send scouting party",
                    "r: Enforce new trade policy",
                    "t: (next...)"
                ]
            elif page == 1:
                return [
                    "q: Hold public speech",
                    "w: Send diplomats to neighbors",
                    "e: Investigate unrest",
                    "r: Cut taxes for the poor",
                    "t: (back...)"
                ]
    return []