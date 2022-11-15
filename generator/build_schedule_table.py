#!/usr/bin/env python3
"""Builds a csv file of the schedule from the 'LHS Daily Schedules' public Google Calendar.
"""

import pickle
import ics
import requests

# Public address in iCal format of the 'LHS Daily Schedules' Google Calendar:
ICAL_URL = "https://calendar.google.com/calendar/ical/phrlfon4jhttr410mqdjat14ug%40group.calendar.google.com/public/basic.ics"
BEGIN_YEAR = 2022   # Year to begin generating the table. Dates before this year will not be included in the table.

class DailySchedule:
    def __init__(self, event) -> None:
        self.date = event.begin.date()
        eventName = event.name.strip()

        self.day_num = None
        self.rotation = None
        self.day_type = None

        if eventName.startswith("Day"):
            self.day_type = "regular"
            self.day_num = int(eventName[4])
            self.rotation = eventName[eventName.index(": ")+1:]
        elif eventName.startswith("Midterm Exam"):
            self.rotation = eventName[eventName.index(": ")+1:]
        elif eventName.startswith("Final Exam"):
            self.day_type = "Final Exam"
            self.rotation = eventName[eventName.index(": ")+1:]
        elif eventName.startswith("All Periods"):
            self.day_type = "All Periods"
            


class YearCalendar:
    def __init__(self) -> None:
        self.dailySchedules = []

    def buildCalendar(self, cal, beginYear) -> None:
        sorted_events = sorted(cal.events, reverse=True)    # Sort from newest to oldest

        for event in sorted_events:
            eventName = event.name.strip()

            if event.begin.date().year < beginYear:
                break

            daySchedule = DailySchedule(event)
            self.dailySchedules.append(daySchedule)

        self.dailySchedules.reverse()

    def printCalendar(self) -> None:
        for dailySchedule in self.dailySchedules:
            print(f"Day #{dailySchedule.day_num}; rotation {dailySchedule.rotation}; date {dailySchedule.date}")


def main() -> None:
    print("Getting calendar...")
    cal = ics.Calendar(requests.get(ICAL_URL).text)
    print("Calendar got.")


    # yearCalendar = YearCalendar()
    # yearCalendar.buildCalendar(cal, 2022)
    # yearCalendar.printCalendar()

if __name__ == "__main__":
    main()
