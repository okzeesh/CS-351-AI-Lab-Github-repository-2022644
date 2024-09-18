class Activity:
    def __init__(self, name, duration, resources, start_time=None):
        self.name = name
        self.duration = duration
        self.resources = resources
        self.start_time = start_time

    def __repr__(self):
        return f"{self.name} (Duration: {self.duration}h, Start: {self.start_time}h)"

class EventScheduler:
    def __init__(self, activities):
        self.activities = activities
        self.schedule = []

    def can_schedule(self, activity, start_time):
        # Check resource availability and timing constraints
        for res in activity.resources:
            for scheduled in self.schedule:
                if res in scheduled.resources:
                    # Check if the scheduled activity overlaps
                    if not (scheduled.start_time + scheduled.duration <= start_time or
                            scheduled.start_time >= start_time + activity.duration):
                        return False
        # Additional specific constraints
        if activity.name == "Cooking Workshop" and start_time >= 12:
            return False  # Kitchen is not available
        if activity.name == "Art Exhibition" and start_time < 12:
            return False  # Exhibition Hall is not available
        if activity.name == "Outdoor Sports" and start_time < 13:  # Assume nice weather in the afternoon
            return False
        if activity.name == "Live Music Performance":
            if not any(a.name == "Art Exhibition" and a.start_time + a.duration <= start_time for a in self.schedule):
                return False  # Must be after Art Exhibition
        return True

    def schedule_activity(self, activity, start_time):
        if self.can_schedule(activity, start_time):
            activity.start_time = start_time
            self.schedule.append(activity)
            return True
        return False

    def schedule_all_activities(self):
        time = 0
        while self.activities:
            for activity in self.activities[:]:  # Iterate over a copy of the activity list
                if self.schedule_activity(activity, time):
                    self.activities.remove(activity)
                    time += activity.duration  # Move time forward by activity duration
                    print(f"Scheduled {activity.name} at {activity.start_time}h")
                    break
            else:
                # If no activity can be scheduled, increment time
                time += 1

    def display_schedule(self):
        print("\nFinal Event Schedule:")
        for activity in self.schedule:
            print(activity)


# Define activities with their durations and required resources
activities = [
    Activity("Yoga Class", duration=1, resources=["Community Hall"]),
    Activity("Cooking Workshop", duration=2, resources=["Kitchen"]),
    Activity("Art Exhibition", duration=3, resources=["Exhibition Hall"]),
    Activity("Outdoor Sports", duration=2, resources=["Park"]),
    Activity("Live Music Performance", duration=2, resources=["Community Hall"])
]

# Create an event scheduler
event_scheduler = EventScheduler(activities)

# Schedule activities
event_scheduler.schedule_all_activities()

# Display the final schedule
event_scheduler.display_schedule()
