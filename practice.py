import geojson
import json
folder = "WA"
num = "53"
out = "SimpleCD.json"
original = "/" + folder + "_" + "final.json"
cd = "/BlockAssign_ST" + num + "_" +folder + "_CD.txt"
vtd = "/BlockAssign_ST" + num + "_" +folder + "_VTD.txt"
with open(folder + original, "r") as f:
    gj = geojson.load(f)
blockToCd = {}
blockToVtd = {}
vtdToCd = {}
with open(folder + cd, "r") as file:
    for line in file:
        tokens = line.split(",")
        blockToCd[tokens[0].strip()] = tokens[1].strip()

with open(folder + vtd, "r") as file:
    for line in file:
        tokens = line.split(",")
        blockToVtd[tokens[0].strip()] = (tokens[1].strip(), tokens[2].strip())

for blockId in blockToCd:
    vtdToCd[blockToVtd[blockId]] = blockToCd[blockId ]
features = gj["features"]
cdToColor = {
    "01":"red",
    "02":"black",
    "03":"yellow",
    "04":"blue",
    "05":"green",
    "06":"orange",
    "07":"pink",
    "08":"gold",
    "09":"navy",
    "10":"grey",
    "11":"aqua",
    "12": "azure",
    "13": "bisque",
    "14": "blueviolet",
    "15": "hotpink",
    "16": "brown",
    "17": "chartreuse",
    "18": "coral",
    "19": "darkgoldenrod",
    "20": "darkgreen"
}

new_features = []
for feat in features:
    props = feat["properties"]
    new_props = {}
    new_props["districtID"] = vtdToCd[(props["COUNTYFP10"], props["VTDST10"])]
    new_props["precinctID"] = props["VTDST10"]
    new_props["precinctName"] = props["NAME10"]
    new_props["county"] = props["COUNTYFP10"]
    new_props["stateID"] = props["STATEFP10"]
    if "TOTPOP" in props.keys():
        new_props["population"] = props["TOTPOP"]
    elif "POP10" in props.keys():
        new_props["population"] = props["POP10"]
    elif "POP100" in props.keys():
        new_props["population"] = props["POP100"]

    if "PRS08_REP" in props.keys():
        new_props["election08Rep"] = props["PRS08_REP"]
    elif "MCCAIN" in props.keys():
        new_props["election08Rep"] = props["MCCAIN"]
    elif "PRES_RVOTE" in props.keys():
        new_props["election08Rep"] = props["PRES_RVOTE"]
    elif "USP_R_08" in props.keys():
        new_props["election08Rep"] = props["USP_R_08"]
    else:
        new_props["election08Rep"] = 0

    if "PRS08_DEM" in props.keys():
        new_props["election08Dem"] = props["PRS08_DEM"]
    elif "OBAMA" in props.keys():
        new_props["election08Dem"] = props["OBAMA"]
    elif "PRES_DVOTE" in props.keys():
        new_props["election08Dem"] = props["PRES_DVOTE"]
    elif "USP_D_08" in props.keys():
        new_props["election08Dem"] = props["USP_D_08"]
    else:
        new_props["election08Dem"] = 0

    if "PRS08_OTH" in props.keys():
        new_props["election08Oth"] = props["PRS08_OTH"]
    elif "BARR" in props.keys():
        new_props["election08Oth"] = props["BARR"]
    elif "USP_O_08" in props.keys():
        new_props["election08Oth"] = props["USP_O_08"]
    else:
        new_props["election08Oth"] = 0

    if "TOTAL_08" in props.keys():
        new_props["totalVotes"] = props["TOTAL_08"]
    elif "TOTAL_PVOT" in props.keys():
        new_props["totalVotes"] = props["TOTAL_PVOT"]
    else:
        new_props["totalVotes"] = new_props["election08Dem"] + new_props["election08Rep"] + new_props["election08Oth"]

    new_props["fill"] = cdToColor[new_props["districtID"]]
    new_props["votingAgePop"] = props["VAP"]
    feat["properties"] = new_props
    new_features.append(feat)
gj["features"] = new_features

nf = open(folder+out, "w")
nf.write(json.dumps(gj))
