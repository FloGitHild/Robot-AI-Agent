from Tasks import *

if __name__ == "__main__":

    # -----------------------------
    # GOALS
    # -----------------------------
    goal_balance = create_task(
        name="Balance Robot stabilisieren",
        description="Langfristiges Ziel",
        task_type="Agent",
        category="Goal",
        priority=5,
        target_time="2026-05-19 23:59:00"
    )

    goal_vision = create_task(
        name="Vision System verbessern",
        description="Kamera + AI",
        task_type="Agent",
        category="Goal",
        priority=4,
        target_time="2026-05-25 12:00:00"
    )

    # -----------------------------
    # PROCESSES
    # -----------------------------
    create_task(
        name="PID Tuning",
        description="Stabilität einstellen",
        task_type="Agent",
        category="Process",
        parent_goal_name=goal_balance,
        priority=4,
        target_time="2026-05-19 20:00:00"
    )

    create_task(
        name="Sensor Noise Filter",
        description="Gyro smoothing",
        task_type="Agent",
        category="Process",
        parent_goal_name=goal_balance,
        priority=3,
        target_time="2026-05-19 18:30:00"
    )

    # -----------------------------
    # USER TASKS
    # -----------------------------
    create_task(
        name="Wecker",
        description="Aufstehen",
        task_type="User",
        category="None",
        priority=2,
        target_time="2026-05-20 07:00:00"
    )

    print("\n================ TASK LIST ================\n")
    list_tasks()