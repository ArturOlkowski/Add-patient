from datetime import date, datetime
from datetime import timedelta
import copy
import json
import os.path
from termcolor import colored
import os
os.system('color')

dates = [
    date(2022, 6, 16),
    date(2022, 8, 15),
    date(2022, 11, 1),
    date(2022, 11, 11),
    date(2022, 12, 25),
    date(2022, 12, 26),
    date(2023, 1, 1),
    date(2023, 1, 6),
    date(2023, 4, 6),
    date(2023, 4, 10),
    date(2023, 5, 1),
    date(2023, 5, 3),
    date(2023, 5, 28),
    date(2023, 6, 8),
    date(2023, 8, 15),
    date(2023, 11, 1),
    date(2023, 11, 11),
    date(2023, 12, 25),
    date(2023, 12, 26)
]


def create_finish_time(begin):
    left = 40
    end = copy.deepcopy(begin)
    while left > 0:
        day_of_week = end.weekday()
        if day_of_week < 5 and not (end in dates):
            left -= 1
        end = end + timedelta(days=1)
    return end


def create_new_patient():
    patient = {}
    patient["firstname"] = input("Podaj imie: ")
    patient["lastname"] = input("Podaj nazwisko: ")
    patient["register_date"] = datetime.fromisoformat(input("Podaj datę rozpoczęcia zabiegu 'YYYY-MM-DD': ")).date()
    patient["finish_date"] = create_finish_time(patient["register_date"])
    return patient


def read_patients_from_file(filepath):
    if not os.path.exists(filepath):
        return []
    with open(filepath, "r") as file:
        file_data = file.read()
        return json.loads(file_data)


def update_database(filepath, db):
    with open(filepath, "w") as file:
        file.write(json.dumps(db, indent=4, sort_keys=True, default=str))


def show_list(db):
    for i in db:
        finish_date = datetime.fromisoformat(i["finish_date"]).date()
        if finish_date < date.today():
            continue
        print("Imie:", i["firstname"])
        print("Nazwisko: ", i["lastname"])
        print("data wprowadzenia pacjenta: ", colored(i["register_date"], "green"))
        print("data zakończenia cyklu zabiegowego: ", colored(i["finish_date"], "cyan"))
        if alert_when_close_to_finish(end=i["finish_date"]) < date.today():
            print(colored("Uwaga! zbliża się koniec cyklu zabiegowego!",  "red"))


def alert_when_close_to_finish(end):
    left = 7
    alert = datetime.fromisoformat(copy.deepcopy(end)).date()
    while left > 0:
        day_of_week = alert.weekday()
        if day_of_week < 5 and not (alert in dates):
            left -= 1
        alert = alert + timedelta(days=-1)
    return alert


filepath = "pacjenci.json"
database = read_patients_from_file(filepath)
show_list(database)


print(colored("Pacjent dodany do bazy", "green", "on_white", ["reverse"]))
while True:
    p = create_new_patient()
    database.append(p)
    update_database(filepath, database)


