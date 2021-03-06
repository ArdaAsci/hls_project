import xml.etree.ElementTree as ET
from dataclasses import dataclass
from typing import Dict, List

from src.loops import Loop


@dataclass
class CsynthModule:
    """
    A dataclass to holds all information of a module present in the csynth file
    """

    name: str
    data: dict[str, int]

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
    def available_area(self) -> dict[str, int]:
        return {
            "avail_dsp": self.data["avail_dsp"],
            "avail_ff": self.data["avail_ff"],
            "avail_lut": self.data["avail_lut"],
            "avail_bram": self.data["avail_bram"],
            "avail_uram": self.data["avail_uram"],
        }

    @property
    def used_area(self) -> dict[str, int]:
        return {
            "dsp": self.data["dsp"],
            "ff": self.data["ff"],
            "lut": self.data["lut"],
            "bram": self.data["bram"],
            "uram": self.data["uram"],
        }

    @property
    def used_area_ratio(self) -> dict[str, int]:
        ratios = {
            "dsp_ratio": None,
            "ff_ratio": None,
            "lut_ratio": None,
            "bram_ratio": None,
            "uram_ratio": None,
        }
        if self.data["avail_dsp"] != 0:
            ratios["dsp_ratio"] = self.data["dsp"] / self.data["avail_dsp"]
        if self.data["avail_ff"] != 0:
            ratios["ff_ratio"] = self.data["ff"] / self.data["avail_ff"]
        if self.data["avail_lut"] != 0:
            ratios["lut_ratio"] = self.data["lut"] / self.data["avail_lut"]
        if self.data["avail_bram"] != 0:
            ratios["bram_ratio"] = self.data["bram"] / self.data["avail_bram"]
        if self.data["avail_uram"] != 0:
            ratios["uram_ratio"] = self.data["uram"] / self.data["avail_uram"]
        return ratios

    def __str__(self) -> str:
        return self.name + " " + str(self.data)


class Csynth:
    """
    For handling all reading operations concerning the csynth.xml file
    No write operations are supported (or required as each vitis_hls call will overwrite previous data)
    """

    modules: List[CsynthModule]
    root: ET.Element
    top_name: str

    def __init__(self, file_name: str) -> None:
        self.csynth_file_name = file_name
        _ = self.update_modules(reconfigure_root=True)

    def configure(self) -> None:
        """
        Loads/reloads the root and TopModule/ModuleName of the csynth file into instance variables.
        """
        self.root = ET.parse(self.csynth_file_name).getroot()
        self.top_name = self.root.findtext("./RTLDesignHierarchy/TopModule/ModuleName")

    def update_modules(self, reconfigure_root=True) -> List[CsynthModule]:
        """
        Finds all the available information for all modules present in the csynth file.
        """
        if reconfigure_root:
            self.configure()
        modules = []
        module_names = self.check_module_names()
        for module_name in module_names:
            modules.append(self.read_module_from_file(module_name))
        self.modules = modules
        return modules

    def check_module_names(self) -> List[str]:
        """
        Find and return all available ModuleNames in the csynth report.
        Note that these names are all auto generated by Vitis.
        """
        module_list_element = self.root.find(
            "./RTLDesignHierarchy/TopModule/InstancesList"
        )
        module_list = []
        for inst in module_list_element:
            module_list.append(inst.findtext("./ModuleName"))
        return module_list

    def read_module_from_file(self, module_name: str) -> CsynthModule:
        """
        Returns a CsynthModule instance for the corresponding module_name with all the available data.
        """
        module_info_element = self.root.find("./ModuleInformation")
        module_data = {}
        for module in module_info_element:
            if module.findtext("./Name") == module_name:
                module_data["latency"] = int(
                    module.findtext(
                        "./PerformanceEstimates/SummaryOfOverallLatency/Average-caseLatency"
                    )
                )
                module_data["dsp"] = int(
                    module.findtext("./AreaEstimates/Resources/DSP")
                )
                module_data["ff"] = int(module.findtext("./AreaEstimates/Resources/FF"))
                module_data["lut"] = int(
                    module.findtext("./AreaEstimates/Resources/LUT")
                )
                module_data["bram"] = int(
                    module.findtext("./AreaEstimates/Resources/BRAM_18K")
                )
                module_data["uram"] = int(
                    module.findtext("./AreaEstimates/Resources/URAM")
                )
                module_data["avail_dsp"] = int(
                    module.findtext("./AreaEstimates/Resources/AVAIL_DSP")
                )
                module_data["avail_ff"] = int(
                    module.findtext("./AreaEstimates/Resources/AVAIL_FF")
                )
                module_data["avail_lut"] = int(
                    module.findtext("./AreaEstimates/Resources/AVAIL_LUT")
                )
                module_data["avail_bram"] = int(
                    module.findtext("./AreaEstimates/Resources/AVAIL_BRAM")
                )
                module_data["avail_uram"] = int(
                    module.findtext("./AreaEstimates/Resources/AVAIL_URAM")
                )
                return CsynthModule(name=module_name, data=module_data)

    def get_module_data_from_loop(self, loop: Loop):
        """
        The names of the loops are not the same as the module names in the csynth file.
        This method is meant to bridge that gap by returning the corresponding CsynthModule
        instance of the given loop_name.
        """

        def get_module_from_name(loop_name: str, instances_in_modules: dict):
            found_module_name = ""
            for module_name in instances_in_modules:
                if loop_name in instances_in_modules[module_name]:
                    found_module_name = module_name
                    break
            return found_module_name

        instances_in_modules = self.instances_in_modules
        target_module_name = get_module_from_name(loop.name, instances_in_modules)
        if target_module_name == "":  # Rety with parent loops
            while loop.parent_loop is not None:
                loop = loop.parent_loop
                target_module_name = get_module_from_name(
                    loop.name, instances_in_modules
                )
                if target_module_name != "":
                    break

        if target_module_name == "":
            return None
        for csynth_module in self.modules:
            if target_module_name == csynth_module.name:
                return csynth_module
        return None

    @property
    def instances_in_modules(self) -> dict[str, list[str]]:
        """
        Find the loop names that are present in the auto-generated csynth module name
        The module names generally follow the pattern:
            top_name + "_Pipeline_" + loop_names
        """

        def cleanup(names: List[str]):
            """
            The module name will include "_Pipeline_" if a pipelining pragma is present in the module.
            Which is not useful for us.
            """
            if "Pipeline" in names:
                names.remove("Pipeline")

        data = {}
        for module in self.modules:
            instance_names = module.name.split("_")[1:]  # First name always = $top_name
            data[module.name] = instance_names
            cleanup(data[module.name])
        return data

    @property
    def top_module_data(self):
        return self.read_module_from_file(self.top_name)

