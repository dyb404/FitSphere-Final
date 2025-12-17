"""
Clear all data and re-seed the database
This script clears existing data and creates fresh sample data
"""
from sqlalchemy.orm import Session
from sqlalchemy import text
from app.db.database import SessionLocal, engine, Base
from app.models.models import User, Workout, Assignment, ProgressLog, HealthTip
from app.core.security import get_password_hash
from datetime import date, timedelta

def clear_and_seed():
    print("=" * 60)
    print("Clearing and Seeding Database")
    print("=" * 60)
    
    db = SessionLocal()
    
    try:
        # Create tables first if they don't exist
        print("\n1. Creating tables...")
        Base.metadata.create_all(bind=engine)
        print("   [OK] Tables created/verified")
        
        # Clear all data (in correct order to respect foreign keys)
        print("\n2. Clearing existing data...")
        try:
            # Delete in reverse order of dependencies
            db.query(ProgressLog).delete()
            db.query(Assignment).delete()
            db.query(Workout).delete()
            db.query(HealthTip).delete()
            db.query(User).delete()
            db.commit()
            print("   [OK] All data cleared")
        except Exception as e:
            # If tables don't exist, that's fine - we'll create them
            db.rollback()
            print(f"   [INFO] No existing data to clear: {e}")
        
        print("\n3. Creating users...")
        
        # Create users
        trainer1 = User(
            name="John Trainer",
            email="trainer@fitsphere.com",
            password_hash=get_password_hash("trainer123"),
            role="trainer"
        )
        
        trainer2 = User(
            name="Sarah Fitness",
            email="sarah@fitsphere.com",
            password_hash=get_password_hash("trainer123"),
            role="trainer"
        )
        
        client1 = User(
            name="Mike Client",
            email="client@fitsphere.com",
            password_hash=get_password_hash("client123"),
            role="client"
        )
        
        client2 = User(
            name="Emma Wilson",
            email="emma@fitsphere.com",
            password_hash=get_password_hash("client123"),
            role="client"
        )
        
        client3 = User(
            name="David Brown",
            email="david@fitsphere.com",
            password_hash=get_password_hash("client123"),
            role="client"
        )
        
        admin = User(
            name="Admin User",
            email="admin@fitsphere.com",
            password_hash=get_password_hash("admin123"),
            role="admin"
        )
        
        db.add_all([trainer1, trainer2, client1, client2, client3, admin])
        db.commit()
        print("   [OK] Users created")
        
        # Refresh to get IDs
        db.refresh(trainer1)
        db.refresh(trainer2)
        db.refresh(client1)
        db.refresh(client2)
        db.refresh(client3)
        
        print("\n4. Creating workouts...")
        # Create workouts
        workout1 = Workout(
            trainer_id=trainer1.id,
            title="Full Body Strength Training",
            description="A comprehensive full-body workout focusing on compound movements. Includes squats, deadlifts, bench press, and overhead press. Perfect for building overall strength and muscle mass."
        )
        
        workout2 = Workout(
            trainer_id=trainer1.id,
            title="Cardio Blast",
            description="High-intensity cardio session designed to burn calories and improve cardiovascular health. Includes running, cycling, and HIIT exercises."
        )
        
        workout3 = Workout(
            trainer_id=trainer1.id,
            title="Core Strength & Stability",
            description="Targeted core workout to improve stability and strength. Includes planks, crunches, Russian twists, and leg raises."
        )
        
        workout4 = Workout(
            trainer_id=trainer2.id,
            title="Yoga & Flexibility",
            description="Gentle yoga flow focusing on flexibility, balance, and relaxation. Suitable for all fitness levels. Helps reduce stress and improve mobility."
        )
        
        workout5 = Workout(
            trainer_id=trainer2.id,
            title="Upper Body Power",
            description="Intense upper body workout targeting chest, back, shoulders, and arms. Includes pull-ups, push-ups, and weight training exercises."
        )
        
        workout6 = Workout(
            trainer_id=trainer2.id,
            title="Leg Day Intensive",
            description="Comprehensive lower body workout focusing on quads, hamstrings, glutes, and calves. Includes squats, lunges, leg presses, and calf raises."
        )
        
        db.add_all([workout1, workout2, workout3, workout4, workout5, workout6])
        db.commit()
        print("   [OK] Workouts created")
        
        # Refresh to get IDs
        db.refresh(workout1)
        db.refresh(workout2)
        db.refresh(workout3)
        db.refresh(workout4)
        db.refresh(workout5)
        db.refresh(workout6)
        
        print("\n5. Creating assignments...")
        # Create assignments
        assignment1 = Assignment(client_id=client1.id, workout_id=workout1.id)
        assignment2 = Assignment(client_id=client1.id, workout_id=workout2.id)
        assignment3 = Assignment(client_id=client2.id, workout_id=workout4.id)
        assignment4 = Assignment(client_id=client2.id, workout_id=workout5.id)
        assignment5 = Assignment(client_id=client3.id, workout_id=workout3.id)
        assignment6 = Assignment(client_id=client3.id, workout_id=workout6.id)
        
        db.add_all([assignment1, assignment2, assignment3, assignment4, assignment5, assignment6])
        db.commit()
        print("   [OK] Assignments created")
        
        print("\n6. Creating progress logs...")
        # Create progress logs
        today = date.today()
        
        progress1 = ProgressLog(
            client_id=client1.id,
            date=today - timedelta(days=7),
            weight=75.5,
            calories=2500,
            notes="Feeling strong after full body workout. Increased weights this week."
        )
        
        progress2 = ProgressLog(
            client_id=client1.id,
            date=today - timedelta(days=3),
            weight=75.2,
            calories=2300,
            notes="Good cardio session. Maintained weight, feeling more energetic."
        )
        
        progress3 = ProgressLog(
            client_id=client1.id,
            date=today,
            weight=74.8,
            calories=2400,
            notes="Great progress! Lost some weight while maintaining strength."
        )
        
        progress4 = ProgressLog(
            client_id=client2.id,
            date=today - timedelta(days=5),
            weight=65.0,
            calories=2000,
            notes="Yoga session was very relaxing. Improved flexibility noticed."
        )
        
        progress5 = ProgressLog(
            client_id=client2.id,
            date=today - timedelta(days=2),
            weight=64.8,
            calories=2100,
            notes="Upper body workout was challenging but rewarding."
        )
        
        progress6 = ProgressLog(
            client_id=client3.id,
            date=today - timedelta(days=4),
            weight=82.0,
            calories=2800,
            notes="Core workout was intense. Feeling stronger in the midsection."
        )
        
        progress7 = ProgressLog(
            client_id=client3.id,
            date=today - timedelta(days=1),
            weight=81.5,
            calories=2700,
            notes="Leg day was tough but completed all sets. Good form maintained."
        )
        
        db.add_all([progress1, progress2, progress3, progress4, progress5, progress6, progress7])
        db.commit()
        print("   [OK] Progress logs created")
        
        print("\n7. Creating health tips...")
        # Create health tips
        tip1 = HealthTip(
            title="Stay Hydrated",
            content="Drink at least 8 glasses of water daily. Proper hydration is essential for optimal performance, recovery, and overall health. Water helps transport nutrients, regulate body temperature, and flush out toxins."
        )
        
        tip2 = HealthTip(
            title="Get Enough Sleep",
            content="Aim for 7-9 hours of quality sleep each night. Sleep is crucial for muscle recovery, hormone regulation, and mental clarity. Poor sleep can negatively impact your fitness progress and overall well-being."
        )
        
        tip3 = HealthTip(
            title="Warm Up Before Exercise",
            content="Always start your workout with a 5-10 minute warm-up. This prepares your muscles, increases blood flow, and reduces the risk of injury. Include light cardio and dynamic stretching."
        )
        
        tip4 = HealthTip(
            title="Eat Balanced Meals",
            content="Include a mix of protein, carbohydrates, and healthy fats in every meal. Protein supports muscle repair, carbs provide energy, and fats are essential for hormone production and nutrient absorption."
        )
        
        tip5 = HealthTip(
            title="Listen to Your Body",
            content="Pay attention to your body's signals. Rest when you're tired, and don't push through pain. Overtraining can lead to injuries and burnout. Recovery is just as important as training."
        )
        
        tip6 = HealthTip(
            title="Set Realistic Goals",
            content="Set achievable, measurable goals with specific timelines. Break large goals into smaller milestones. Celebrate your progress along the way to stay motivated and maintain consistency."
        )
        
        tip7 = HealthTip(
            title="Include Strength Training",
            content="Don't skip strength training! Building muscle helps boost metabolism, improve bone density, and enhance daily functional movements. Aim for 2-3 strength sessions per week."
        )
        
        tip8 = HealthTip(
            title="Track Your Progress",
            content="Keep a record of your workouts, measurements, and how you feel. Tracking progress helps identify what's working, keeps you accountable, and provides motivation when you see improvements."
        )
        
        tip9 = HealthTip(
            title="Stretch Regularly",
            content="Incorporate stretching into your routine, especially after workouts. Stretching improves flexibility, reduces muscle tension, and can help prevent injuries. Hold stretches for 20-30 seconds."
        )
        
        tip10 = HealthTip(
            title="Stay Consistent",
            content="Consistency is key to achieving fitness goals. It's better to do moderate exercise regularly than intense workouts sporadically. Find a routine that fits your lifestyle and stick to it."
        )
        
        db.add_all([tip1, tip2, tip3, tip4, tip5, tip6, tip7, tip8, tip9, tip10])
        db.commit()
        print("   [OK] Health tips created")
        
        print("\n" + "=" * 60)
        print("[SUCCESS] Database cleared and seeded successfully!")
        print("=" * 60)
        print("\nDemo Accounts Created:")
        print("   Trainer: trainer@fitsphere.com / trainer123")
        print("   Client:  client@fitsphere.com / client123")
        print("   Admin:   admin@fitsphere.com / admin123")
        print("\nYou can now login with these accounts!")
        
    except Exception as e:
        print(f"\n[ERROR] {e}")
        db.rollback()
        import traceback
        traceback.print_exc()
    finally:
        db.close()

if __name__ == "__main__":
    clear_and_seed()

