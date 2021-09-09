import xml.etree.ElementTree as ET
import traceback

class CsynthFile:

    def __init__(self, file_name: str,) -> None:
        self.root = ET.parse(file_name).getroot()
        self.properties = {}
        try:
            self.properties["latency"] = int(self.root.find("./PerformanceEstimates/SummaryOfOverallLatency/Average-caseLatency").text)
            self.properties["dsp"] = int(self.root.find("./AreaEstimates/Resources/DSP").text)
            self.properties["ff"] = int(self.root.find("./AreaEstimates/Resources/FF").text)
            self.properties["lut"] = int(self.root.find("./AreaEstimates/Resources/LUT").text)
            self.properties["bram"] = int(self.root.find("./AreaEstimates/Resources/BRAM_18K").text)
            self.properties["uram"] = int(self.root.find("./AreaEstimates/Resources/URAM").text)
        except AttributeError:
            print(traceback.format_exc())
            print("Csynth XML file missing property")
            exit()
        
    @property
    def latency(self):
        return self.properties["latency"]

    @property
    def dsp(self):
        return self.properties["dsp"]
    
    @property
    def ff(self):
        return self.properties["ff"]

    @property
    def lut(self):
        return self.properties["lut"]

    @property
    def bram(self):
        return self.properties["bram"]
    
    @property
    def uram(self):
        return self.properties["uram"]


    

