from app import app
from models import db, User, Task

with app.app_context():
    print("Clearing database...")

    db.session.query(Task).delete()
    db.session.query(User).delete()
    db.session.commit()

    print("Creating users...")

    jane = User(username="jane")
    jane.password = "12345"

    favour = User(username="favour")
    favour.password = "password"

    db.session.add_all([jane, favour])
    db.session.commit()

    print("Creating tasks...")

    task1 = Task(
        title="Finish Flask Lab",
        description="Complete the summative assignment",
        completed=False,
        due_date="2026-08-01",
        user_id=jane.id
    )

    task2 = Task(
        title="Push to GitHub",
        description="Upload final version",
        completed=True,
        due_date="2026-08-02",
        user_id=jane.id
    )

    task3 = Task(
        title="Study React",
        description="Prepare for frontend integration",
        completed=False,
        due_date="2026-08-03",
        user_id=favour.id
    )

    db.session.add_all([task1, task2, task3])
    db.session.commit()

    print("Database seeded successfully!")