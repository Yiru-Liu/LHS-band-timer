#!/usr/bin/env python3
"""Builds a csv file of the schedule from the 'LHS Daily Schedules' public Google Calendar.
"""

import pickle
import ics
import requests
import json

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
            self.rotation = eventName[eventName.index(": ")+2:]
        elif eventName.startswith("Midterm Exam"):
            self.day_type = "Midterm Exam"
            self.rotation = eventName.split("Midterm Exam ")[1]     # Get string after "Midterm Exam "
        elif eventName.startswith("Final Exam"):
            self.day_type = "Final Exam"
            self.rotation = eventName[eventName.index(": ")+2:]
        elif eventName.startswith("All Periods"):
            self.day_type = "All Periods"
            self.rotation = "ABCDEFG"

    def to_dict(self) -> dict:
        d = {
            "date": self.date.strftime("%Y-%m-%d"),
            "day_type": self.day_type,
            "rotation": self.rotation
        }
        if self.day_num is not None:
            d["day_num"] = self.day_num
        return d


class YearCalendar:
    def __init__(self) -> None:
        self.dailySchedules = []

    def buildCalendar(self, cal, beginYear) -> None:
        sorted_events = sorted(cal.events, reverse=True)    # Sort from newest to oldest

        for event in sorted_events:
            if event.begin.date().year < beginYear:
                break

            daySchedule = DailySchedule(event)
            self.dailySchedules.append(daySchedule)

        self.dailySchedules.reverse()

    def printCalendar(self) -> None:
        for dailySchedule in self.dailySchedules:
            print(json.dumps(dailySchedule.to_dict()))

    def to_js_object(self) -> None:
        obj = {}
        for dailySchedule in self.dailySchedules:
            d = dailySchedule.to_dict()
            date = d["date"]
            d.pop("date")
            obj[date] = d
        print(json.dumps(obj))
            


def main() -> None:
    print("Getting calendar...")
    cal = ics.Calendar(requests.get(ICAL_URL).text)
    print("Calendar got.")


    yearCalendar = YearCalendar()
    yearCalendar.buildCalendar(cal, 2022)
    # yearCalendar.printCalendar()
    yearCalendar.to_js_object()

if __name__ == "__main__":
    main()
