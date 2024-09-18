class Activity:
    def __init__(self, name, duration, resources, start_time=None):
        self.name = name
        self.duration = duration
        self.resources = resources
        self.start_time = start_time

    def __repr__(self):
        return f"{self.name} (Duration: {self.duration}h, Start: {self.start_time}h)"

class ConservationScheduler:
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
        if activity.name == "Feeding the Lions" and start_time >= 12:
            return False  # Must be before noon
        if activity.name == "Health Check for Elephants" and start_time < 15:
            return False  # Must be after 3 PM
        if activity.name == "Rehabilitation for Birds":
            if not all(res in self.resources_available() for res in activity.resources):
                return False  # Requires all resources to be available
        if activity.name == "Maintenance of Habitats":
            if not any(a.name == "Feeding the Lions" and a.start_time <= start_time < a.start_time + a.duration for a in self.schedule):
                return False  # Must happen while feeding lions
        if activity.name == "Education Workshop":
            if not any(a.name == "Rehabilitation for Birds" and a.start_time + a.duration <= start_time for a in self.schedule):
                return False  # Must follow bird rehabilitation
        return True

    def resources_available(self):
        return ["Staff", "Vehicle", "Veterinary Staff", "Volunteers", "Equipment", "Tools", "Presentation Materials"]

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
        print("\nFinal Conservation Schedule:")
        for activity in self.schedule:
            print(activity)

def get_user_input():
    activities = []
    print("Welcome to the Wildlife Conservation Scheduler!")
    while True:
        name = input("Enter the activity name (or type 'done' to finish): ")
        if name.lower() == 'done':
            break
        duration = int(input("Enter the duration in hours: "))
        resources = input("Enter required resources (comma-separated): ").split(", ")
        activities.append(Activity(name, duration, resources))
    return activities

# Get user input for activities
user_activities = get_user_input()

# Create a conservation scheduler
conservation_scheduler = ConservationScheduler(user_activities)

# Schedule activities
conservation_scheduler.schedule_all_activities()

# Display the final schedule
conservation_scheduler.display_schedule()
