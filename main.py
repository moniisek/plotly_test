from pathlib import Path
import os
import json

DFQ_files_dir = Path(__file__).parents[0] / "DFQ_test"
lines = []

for file in os.listdir(DFQ_files_dir):
    with open(DFQ_files_dir / file, encoding="utf-8") as fh:
        for x in fh:
            lines = [x.strip() for x in fh]




curveObj = {"x": [], "y": []}
curveObj["points"] = {}
curveObj['steps'] = []
points = []
steps = []

for i in range(len(lines)):
    x = lines[i]
    if "K0001/1" in x:
        line_split = x.split(" ")
        curveObj["x"].append(float(line_split[1]))

    if "K0001/2" in x:
        line_split = x.split(" ")
        curveObj["y"].append(float(line_split[1]))

    if "important point" in x:
        points.append(lines[i:i+12])

    if "tightening step" in x:
        line_split = lines[i+1].split(" ")
        curveObj["points"][" ".join(line_split[1:])] = {"x": None, "y": None, "lower": {"x": None, "y": None}, "upper": {"x": None, "y": None}}
        curveObj["steps"].append(float(lines[i+10].split(" ")[1]))


for char in points:
    K2002_split = [x.strip() for x in " ".join(char[1].split(" ")[1:]).split("-")]

    if "angle" in K2002_split:
        curveObj["points"][K2002_split[0]]["x"] = float(char[-1].split(" ")[1])

    if "torque" in K2002_split:
        curveObj["points"][K2002_split[0]]["y"] = float(char[-1].split(" ")[1])

    if "angle" in K2002_split and char[5].split(" ")[1] == "1":
        curveObj["points"][K2002_split[0]]['lower']["x"] = float(char[3].split(" ")[1])

    if "torque" in K2002_split and char[5].split(" ")[1] == "1":
        curveObj["points"][K2002_split[0]]['lower']["y"] = float(char[3].split(" ")[1])

    if "angle" in K2002_split and char[6].split(" ")[1] == "1":
        curveObj["points"][K2002_split[0]]['upper']["x"] = float(char[4].split(" ")[1])

    if "torque" in K2002_split and char[6].split(" ")[1] == "1":
        curveObj["points"][K2002_split[0]]['upper']["y"] = float(char[4].split(" ")[1])


with open("curveObjOut.json", 'w') as fh:
    json.dump(curveObj, fh)





