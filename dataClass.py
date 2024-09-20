import json
from dataclasses import dataclass
from datetime import datetime, timedelta
from typing import List
import config

JSON_DATA = config.JSON_DATA
JSON_CALENDAR = config.JSON_CALENDAR
WEEKS = config.WEEKS

@dataclass
class User:
    username: str
    chat_id: str
    week: str
    time: str

class UserManager:
    def __init__(self, filename=JSON_DATA):
        self.json_file = filename
        self.users = self.load_users()


    def load_users(self) -> List[User]:
        with open(self.json_file, 'r', encoding='utf-8') as file:
            json_data = file.read()
        return self.json_to_users(json_data)


    def json_to_users(self, json_data: str) -> List[User]:
        data = json.loads(json_data)
        return [User(**item) for item in data]


    def find_user_by_username(self, username: str) -> User:
        return next((user for user in self.users if user.username == username), None)


    def add_week_to_user(self, username: str, week: str) -> bool:
        user = self.find_user_by_username(username)
        if user:
            if week not in user.week:
                user.week.append(week)
                self.save_users()
            return True
        return False


    def save_users(self):
        with open(self.json_file, 'w', encoding='utf-8') as file:
            json.dump([user.__dict__ for user in self.users], file, ensure_ascii=False, indent=4)


class CalendarGentetar:
    def __init__(self, FilePathCalendar=JSON_CALENDAR, FilePathUsers=JSON_DATA):
        self.FilePathCalendar = FilePathCalendar
        self.FilePathUsers = FilePathUsers
        self.weeks = CalendarGentetar.load_json(self.FilePathCalendar)


    def get_week_range(self, start_date):
        """Возвращает строку с диапазоном дат для недели."""
        end_date = start_date + timedelta(days=6)
        return f"{start_date.strftime('%d-%m-%Y')} - {end_date.strftime('%d-%m-%Y')}"


    def get_next_four_weeks(self):
        today = datetime.today()
        start_date = today - timedelta(days=today.weekday())
        weeks = {}
        for i in range(4):
            week_range = self.get_week_range(start_date + timedelta(weeks=i))
            weeks[f"{i+1}_week"] = {
                "available": True,  # По умолчанию устанавливаем доступность в True
                "dates": week_range
            }
        return weeks


    def save_weeks(self):
        with open(self.FilePathCalendar, 'w', encoding='utf-8') as file:
            json.dump(self.weeks, file, ensure_ascii=False, indent=4)


    def update_weeks(self):
        self.weeks = self.get_next_four_weeks()
        self.save_weeks()


class CalendarData:
    def __init__(self, FilePathCalendar=JSON_CALENDAR, FilePathUsers=JSON_DATA):
        self.FilePathCalendar = FilePathCalendar
        self.FilePathUsers = FilePathUsers
        self.weeks = CalendarData.load_json(self.FilePathCalendar)


    @staticmethod
    def load_json(file_path):
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                return json.load(file)
        except FileNotFoundError:
            return {}


    @staticmethod
    def get_week(week_number):
        weeks = CalendarData.load_json(JSON_CALENDAR)
        week_key = f"{week_number}_week"
        if week_key in weeks:
            return weeks[week_key]
        else:
            raise IndexError("Invalid week number")

    def remove_week_from_data(self):
        calendar_data = CalendarData.load_json(self.FilePathCalendar)
        users_data = CalendarData.load_json(self.FilePathUsers)

        # Получаем значение ключа 1_week
        week_to_remove = calendar_data.get('1_week')

        if not week_to_remove:
            return

        # Удаляем значение week_to_remove из users_data
        updated_users_data = []
        for user in users_data:
            if user['week'] == week_to_remove['dates']:
                user['week'] = ''  # Удаляем значение week
            updated_users_data.append(user)

        # Записываем обновленные данные обратно в users.json
        with open(self.FilePathUsers, 'w', encoding='utf-8') as users_file_obj:
            json.dump(updated_users_data, users_file_obj, indent=4, ensure_ascii=False)

    @staticmethod
    def get_all_weeks():
        """Возвращает все недели в виде списка из JSON."""
        weeks = CalendarData.load_json(JSON_CALENDAR)
        return list(weeks.values())



## Пример использования
#manager = UserManager()
#manager.add_week_to_user("Гриша", week="Неделя 1")


## Пример использования класса Calendar
#calendar = Calendar()
#
## Обновляем данные о неделях
#calendar.update_weeks()
#calendar.remove_week_from_data()
#
#
## Получаем данные о второй неделе
#for i in (range(WEEKS)):
#    print(calendar.get_all_weeks()[i]["dates"])
#
#
## Получаем данные о третьей неделе
#print(calendar.get_week(2))
