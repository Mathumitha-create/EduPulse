from sqlalchemy.orm import Session
from models import Achievement, Notification
from datetime import datetime

# Define standard badges
BADGES = {
    "first_login": {"name": "First Step", "desc": "Logged in for the first time.", "icon": "🚀"},
    "first_task": {"name": "Task Master", "desc": "Completed your first task.", "icon": "✅"},
    "low_risk": {"name": "Safe Zone", "desc": "Achieved Low Risk status.", "icon": "🛡️"},
    "top_scorer": {"name": "Top Scorer", "desc": "Achieved exam score \u003e 90.", "icon": "🏆"},
}

def create_notification(db: Session, user_id: int, message: str):
    notification = Notification(user_id=user_id, message=message)
    db.add(notification)
    db.commit()
    db.refresh(notification)
    return notification

def check_and_award_badge(db: Session, user_id: int, badge_key: str):
    if badge_key not in BADGES:
        return None

    # Check if already awarded
    existing = db.query(Achievement).filter(
        Achievement.user_id == user_id, 
        Achievement.badge_name == BADGES[badge_key]["name"]
    ).first()

    if not existing:
        badge_info = BADGES[badge_key]
        achievement = Achievement(
            user_id=user_id,
            badge_name=badge_info["name"],
            description=badge_info["desc"],
            icon_name=badge_info["icon"]
        )
        db.add(achievement)
        create_notification(db, user_id, f"🏆 You earned a new badge: {badge_info['name']}!")
        db.commit()
        db.refresh(achievement)
        return achievement
    return None

def get_user_achievements(db: Session, user_id: int):
    return db.query(Achievement).filter(Achievement.user_id == user_id).all()

def get_unread_notifications(db: Session, user_id: int):
    return db.query(Notification).filter(Notification.user_id == user_id, Notification.is_read == False).all()

def mark_notifications_read(db: Session, user_id: int):
    db.query(Notification).filter(Notification.user_id == user_id, Notification.is_read == False).update({"is_read": True})
    db.commit()
