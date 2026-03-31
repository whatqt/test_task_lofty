import os
import argparse
import requests
from dotenv import load_dotenv



load_dotenv()

def get_weather(city: str) -> None:
    """
    Получает данные о погоде через OpenWeatherMap API и выводит их в консоль.
    
    :param city: Название города
    """
    api_key = os.getenv("OPENWEATHER_API_KEY")
    
    if not api_key:
        print("Ошибка: API ключ не найден в .env файле.")
        return

    url = "https://api.openweathermap.org/data/2.5/weather"
    params = {
        "q": city,
        "appid": api_key,
        "units": "metric",
        "lang": "ru"
    }

    try:
        response = requests.get(url, params=params)
        
        if response.status_code == 404:
            print(f"Ошибка: Город '{city}' не найден.")
            return
        
        response.raise_for_status()
        
        data = response.json()
        
        temp = data["main"]["temp"]
        description = data["weather"][0]["description"]
        
        print(f"Погода в {city.capitalize()}:")
        print(f"Температура: {temp}°C")
        print(f"Описание: {description}")

    except requests.exceptions.ConnectionError:
        print("Ошибка: Не удалось подключиться к серверу. Проверьте интернет-соединение.")
    except requests.exceptions.HTTPError as http_err:
        print(f"Произошла ошибка HTTP: {http_err}")
    except Exception as e:
        print(f"Произошла непредвиденная ошибка: {e}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Утилита для получения текущей погоды.")
    parser.add_argument("city", help="Название города, для которого нужно узнать погоду")
    
    args = parser.parse_args()
    
    get_weather(args.city)