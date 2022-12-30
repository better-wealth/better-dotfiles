import requests

formulae30 = requests.get(
    "https://formulae.brew.sh/api/analytics/install/30d.json"
).json()["items"]
formulae90 = requests.get(
    "https://formulae.brew.sh/api/analytics/install/90d.json"
).json()["items"]
formulae365 = requests.get(
    "https://formulae.brew.sh/api/analytics/install/365d.json"
).json()["items"]


for i in formulae30:
    i["count"] = int(i["count"].replace(",", ""))
    i["percent"] = float(i["percent"])

for i in formulae90:
    i["count"] = int(i["count"].replace(",", ""))
    i["percent"] = float(i["percent"])

for i in formulae365:
    i["count"] = int(i["count"].replace(",", ""))
    i["percent"] = float(i["percent"])

# EX: {'name': [] }
names365 = [i["formula"] for i in formulae365]
names90 = [i["formula"] for i in formulae90]
names30 = [i["formula"] for i in formulae30]
formulae = {
    i: {
        "index365": None,
        "index90": None,
        "index30": None,
        "percent365": 0,
        "percent90": 0,
        "percent30": 0,
        "change365to90": 0,
        "change90to30": 0,
        "changeRate": 0,
    }
    for i in list(set(names365 + names90 + names30))
}

for (a, b, c) in zip(formulae365, formulae90, formulae30):
    formulae[a["formula"]]["index365"] = a["number"] - 1
    formulae[a["formula"]]["percent365"] = a["percent"]
    formulae[b["formula"]]["index90"] = b["number"] - 1
    formulae[b["formula"]]["percent90"] = b["percent"]
    formulae[c["formula"]]["index30"] = c["number"] - 1
    formulae[c["formula"]]["percent30"] = c["percent"]


for formula, values in formulae.items():
    if values["percent365"] != 0:
        formulae[formula]["change365to90"] = (
            values["percent90"] - values["percent365"]
        ) / (values["percent365"])
    else:
        formulae[formula]["change365to90"] = 1
    if values["percent90"] != 0:
        formulae[formula]["change90to30"] = (
            values["percent30"] - values["percent90"]
        ) / (values["percent90"])
    else:
        formulae[formula]["change90to30"] = 1
    if formulae[formula]["change365to90"] != 0:
        formulae[formula]["changeRate"] = (
            formulae[formula]["change90to30"] - formulae[formula]["change365to90"]
        ) / (formulae[formula]["change365to90"])
    else:
        formulae[formula]["changeRate"] = 1

# the rate of change of slope =(y2 – y1) / (x2 – x1)
# (values["percent90"] - values["percent365"]) / (365-90)
# (values["percent30"] - values["percent365"]) / (365-30)
# (values["percent30"] - values["percent90"]) / (90-30)
