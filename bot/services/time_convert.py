from datetime import datetime
import pytz

TZ_NAMES = {
    "moscow": "в Москве",
    "perm": "в Перми",
    # можешь добавлять сколько угодно
}

# Словарь для быстрого доступа по названию
TIMEZONES = {
    "perm": pytz.timezone("Asia/Yekaterinburg"),
    "moscow": pytz.timezone("Europe/Moscow"),
}

def convert_time(time_str: str, from_tz="perm", to_tz="moscow") -> str:
    try:
        time_obj = datetime.strptime(time_str, "%H:%M")
    except ValueError:
        try:
            time_obj = datetime.strptime(time_str, "%H")
        except ValueError:
            return "Я не понял, сколько времени ты имел в виду. Напиши в формате HH или HH:MM."

    now = datetime.now()
    input_time = datetime(
        now.year, now.month, now.day,
        time_obj.hour, time_obj.minute
    )

    from_zone = TIMEZONES.get(from_tz.lower())
    to_zone = TIMEZONES.get(to_tz.lower())

    if not from_zone or not to_zone:
        return "Я не знаю такой часовой пояс."

    input_time = from_zone.localize(input_time)
    converted = input_time.astimezone(to_zone)

    from_name = TZ_NAMES.get(from_tz.lower(), from_tz)
    to_name = TZ_NAMES.get(to_tz.lower(), to_tz)

    return f"{to_name} будет {converted.strftime('%H:%M')}, если {from_name} {time_obj.strftime('%H:%M')}."


