import json
import os
from ntcore import *

class Build:
    ntInst = NetworkTableInstance.getDefault()
    
    def buildInitConfig(self):
        tbl = self.ntInst.getTable("InitConfig")
        override:bool = tbl.getBoolean(".override", False)
        self.build(tbl, "build/config/", persist=True, override=override)
        tbl.putBoolean(".override", False)
        tbl.setPersistent(".override")

    def buildVariables(self):
        tbl = self.ntInst.getTable("Variables")
        override:bool = tbl.getBoolean(".override", False)
        self.build(tbl, "build/variables/", persist=True, override=override)
        tbl.putBoolean(".override", False)
        tbl.setPersistent(".override")

    def build(self, ntTable, folderPath, persist=False, override=False):
        files = os.listdir( folderPath )
        for file in files:
            # Only Load Json Files
            if not file.endswith(".json"):
                continue
            # Loop Through Files
            fullPath = os.path.join( os.getcwd(), folderPath, file )
            with open(f"{fullPath}", 'r') as f:
                content = json.load( f )
                for top in content:
                    self.loadLoop(ntTable, "", content, persist, override)

    def loadLoop(self, table:NetworkTable, path, content, persist=True, override=False):
        for key in content:
            if path == "":
                thisPath = f"{key}"
            else:
                thisPath = f"{path}/{key}"

            if type( content[key] ) != dict:
                if not override:
                    entry = table.getEntry( thisPath )
                    entryType = entry.getType()
                    if entryType != NetworkTableType.kUnassigned:
                        return
                table.putValue( thisPath, content[key] )
                if persist:
                    table.setPersistent( thisPath )
                else:
                    table.clearPersistent( thisPath )
            else:
                self.loadLoop( table, thisPath, content[key], persist, override)
