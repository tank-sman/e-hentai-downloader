import sys, os, json


def resource_path():
    """Get absolute path to resource, works for dev and for PyInstaller"""
    base_path = getattr(sys, "_MEIPASS", os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_path)


settingsfilename = resource_path() + "\data.json"
datas = {
    "savePath": "Downloads/",
    "ipb_member_id": "",
    "ipb_pass_hash": "",
    "ipb_session_id": "",
    "sk": "",
    "proxy":""
}


def readSetting(datas=datas) -> dict:
    try:
        export = json.load(open(settingsfilename))
        datas = export
    except FileNotFoundError:
        if datas["ipb_member_id"] == "":
            memberid = input("enter from cookies (ipb_member_id):")
            passhash = input("enter from cookies (ipb_pass_hash):")
            sessionID = input("enter from cookies (ipb_session_id):")
            sk = input("enter from cookies (sk):")
            if memberid != "" or passhash != "":
                datas["ipb_member_id"] = memberid
                datas["ipb_pass_hash"] = passhash
                datas["ipb_session_id"] = sessionID
                datas["sk"] = sk
        json.dump(datas, open(settingsfilename, "x"), indent=4)
    os.environ["userdata"]=json.dumps(datas)
    # return datas

datas = readSetting()


def editsettings(key, newValue):
    datas[key] = newValue
    json.dump(datas, open(settingsfilename, "w"), indent=4)
