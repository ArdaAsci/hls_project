from typing import List
import xml.etree.ElementTree as ET


class CsynthModule:
    def __init__(self, module_name: str, module_data: dict) -> None:
        self.name = module_name
        self.data = module_data

    @property
    def latency(self):
        return self.data["latency"]

    @property
    def dsp(self):
        return self.data["dsp"]

    @property
    def ff(self):
        return self.data["ff"]

    @property
    def lut(self):
        return self.data["lut"]

    @property
    def bram(self):
        return self.data["bram"]

    @property
    def uram(self):
        return self.data["uram"]

    @property
    def available_area(self):
        return {
            "avail_dsp": self.data["avail_dsp"],
            "avail_ff": self.data["avail_ff"],
            "avail_lut": self.data["avail_lut"],
            "avail_bram": self.data["avail_bram"],
            "avail_uram": self.data["avail_uram"]
        }

    def __str__(self) -> str:
        return self.name + " " + str(self.data)


class Csynth:
    def __init__(self, file_name: str) -> None:
        self.csynth_file_name = file_name
        self.modules: List[CsynthModule]
        self.root: ET.Element
        self.top_name: str
        self.configure()
        self.update_modules()

    def configure(self):
        self.root = ET.parse(self.csynth_file_name).getroot()
        self.top_name = self.root.findtext(
            "./RTLDesignHierarchy/TopModule/ModuleName")

    def update_modules(self, update_root=True) -> List[CsynthModule]:
        if update_root:
            self.configure()
        modules = []
        module_names = self.check_module_names()
        for module_name in module_names:
            modules.append(self.get_module(module_name))
        self.modules = modules
        return modules

    def check_module_names(self) -> List[str]:
        module_list_element = self.root.find(
            "./RTLDesignHierarchy/TopModule/InstancesList")
        module_list = []
        for inst in module_list_element:
            module_list.append(inst.findtext("./ModuleName"))
        return module_list

    def get_module(self, module_name: str) -> CsynthModule:
        module_info_element = self.root.find("./ModuleInformation")
        module_data = {}
        for module in module_info_element:
            if module.findtext("./Name") == module_name:
                module_data["latency"] = int(
                    module.findtext(
                        "./PerformanceEstimates/SummaryOfOverallLatency/Average-caseLatency"
                    ))
                module_data["dsp"] = int(
                    module.findtext("./AreaEstimates/Resources/DSP"))
                module_data["ff"] = int(
                    module.findtext("./AreaEstimates/Resources/FF"))
                module_data["lut"] = int(
                    module.findtext("./AreaEstimates/Resources/LUT"))
                module_data["bram"] = int(
                    module.findtext("./AreaEstimates/Resources/BRAM_18K"))
                module_data["uram"] = int(
                    module.findtext("./AreaEstimates/Resources/URAM"))
                module_data["avail_dsp"] = int(
                    module.findtext("./AreaEstimates/Resources/AVAIL_DSP"))
                module_data["avail_ff"] = int(
                    module.findtext("./AreaEstimates/Resources/AVAIL_FF"))
                module_data["avail_lut"] = int(
                    module.findtext("./AreaEstimates/Resources/AVAIL_LUT"))
                module_data["avail_bram"] = int(
                    module.findtext("./AreaEstimates/Resources/AVAIL_BRAM"))
                module_data["avail_uram"] = int(
                    module.findtext("./AreaEstimates/Resources/AVAIL_URAM"))
                return CsynthModule(module_name=module_name,
                                    module_data=module_data)

    @property
    def instances_in_modules(self):
        """
        Find the loop names that are present in the auto-generated csynth module name
        """
        data = {}
        for module in self.modules:
            instance_names = module.name.split("_")[2:]
            data[module.name] = instance_names
        return data