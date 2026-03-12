from fastapi import FastAPI
from database import SessionLocal
from models import Journal

app = FastAPI()


# Emotion detection function
def detect_emotion(text):

    text = text.lower()

    if "calm" in text or "peace" in text:
        return "calm"

    if "happy" in text or "joy" in text:
        return "happy"

    if "sad" in text:
        return "sad"

    return "neutral"


# Home route
@app.get("/")
def home():
    return "Home"


# Get all journals
@app.get("/api/journal")
def get_journals():

    db = SessionLocal()

    journals = db.query(Journal).all()

    return journals


# Create journal entry
@app.post("/api/journal")
def create_journal(entry: dict):

    db = SessionLocal()

    emotion = detect_emotion(entry["text"])

    journal = Journal(
        userId=entry["userId"],
        ambience=entry["ambience"],
        text=entry["text"],
        emotion=emotion
    )

    db.add(journal)
    db.commit()

    return {
        "message": "Journal saved",
        "emotion": emotion
    }


# Insights API
@app.get("/api/journal/insights/{userId}")
def get_insights(userId: str):

    db = SessionLocal()

    journals = db.query(Journal).filter(Journal.userId == userId).all()

    total_entries = len(journals)

    emotions = {}
    ambience = {}

    for j in journals:

        emotions[j.emotion] = emotions.get(j.emotion, 0) + 1
        ambience[j.ambience] = ambience.get(j.ambience, 0) + 1

    top_emotion = max(emotions, key=emotions.get) if emotions else None
    top_ambience = max(ambience, key=ambience.get) if ambience else None

    return {
        "totalEntries": total_entries,
        "topEmotion": top_emotion,
        "mostUsedAmbience": top_ambience
    }