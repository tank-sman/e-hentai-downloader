import sys, os, json


def resource_path():
    """Get absolute path to resource, works for dev and for PyInstaller"""
    base_path = getattr(sys, "_MEIPASS", os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_path)


settingsfilename = resource_path() + "/data.json"
datas = {
    "savePath": "Downloads/",
    "ipb_member_id": "",
    "ipb_pass_hash": "",
    "ipb_session_id": "",
    "event":"",
    "sk": "",
    "rewriteInfo" : True,
    "Perview" : True,
    "proxy":"",
    "core":"1"
}


def readSetting(datas=datas) -> dict:
    try:
        export = json.load(open(settingsfilename))
        datas = export
    except Exception as e:
        print(e)
        if datas["ipb_member_id"] == "" and datas["ipb_pass_hash"] == "":
            memberid = input("enter from cookies (ipb_member_id):")
            passhash = input("enter from cookies (ipb_pass_hash):")
            sessionID = input("enter from cookies (ipb_session_id)(Leave empty if not exist):")
            event = input("enter from cookies (event)(Leave empty if not exist):")
            sk = input("enter from cookies (sk):")
            if memberid != "" or passhash != "":
                datas["ipb_member_id"] = memberid
                datas["ipb_pass_hash"] = passhash
                datas["ipb_session_id"] = sessionID
                datas["event"] = event
                datas["sk"] = sk
        json.dump(datas, open(settingsfilename, "x"), indent=4)
    os.environ["userdata"]=json.dumps(datas)
    # return datas

readSetting()


def editsettings(key, newValue):
    print(key,newValue)
    datas=json.loads(os.environ["userdata"])
    datas[key] = newValue
    json.dump(datas, open(settingsfilename, "w"), indent=4)
    readSetting()
