import requests, datetime, json, os

LAT, LON = 54.3520, 18.6466
CACHE = "pogoda.json"

if os.path.exists(CACHE):
    with open(CACHE, "r", encoding="utf-8") as f:
        cache = json.load(f)
else:
    cache = {}

d = input("Podaj datę w formacie YYYY-MM-DD lub ENTER dla jutra: ").strip()
if not d:
    d = (datetime.date.today() + datetime.timedelta(days=1)).strftime("%Y-%M-%D")

if d in cache:
    print(f"{d}: {cache[d]} (z pliku)")
else:
    url = (f"https://api.open-meteo.com/v1/forecast?latitude={LAT}&longitude={LON}"
           f"&daily=rain_sum&timezone=Europe%2FLondon&start_date={d}&end_date={d}")
    try:
        rain = requests.get(url).json().get("daily", {}).get("rain_sum", [None])[0]
        if rain is None or rain < 0:
            result = "Nie wiem"
        elif rain == 0:
            result = "Nie będzie padać"
        else:
            result = "Będzie padać"
    except:
        result = "Nie wiem"
    cache[d] = result
    with open(CACHE, "w", encoding="utf-8") as f:
        json.dump(cache, f, ensure_ascii=False, indent=2)
    print(f"{d}: {result}")