# unit_converter.py
class UnitConverter:
    @staticmethod
    def length(value: float, from_unit: str, to_unit: str) -> float:
        factors = {'m':1.0,'km':1000.0,'cm':0.01,'mm':0.001,'inch':0.0254,'ft':0.3048}
        if from_unit not in factors or to_unit not in factors:
            raise ValueError("Unsupported units")
        meters = value * factors[from_unit]
        return meters / factors[to_unit]

    @staticmethod
    def weight(value: float, from_unit: str, to_unit: str) -> float:
        factors = {'kg':1.0,'g':0.001,'lb':0.45359237}
        if from_unit not in factors or to_unit not in factors:
            raise ValueError("Unsupported units")
        kg = value * factors[from_unit]
        return kg / factors[to_unit]

    @staticmethod
    def temp(value: float, from_unit: str, to_unit: str) -> float:
        f = from_unit.lower(); t = to_unit.lower()
        if f == t:
            return value
        if f == "c":
            c = value
        elif f == "f":
            c = (value - 32) * 5.0/9.0
        elif f == "k":
            c = value - 273.15
        else:
            raise ValueError("Unsupported temp unit")
        if t == "c":
            return c
        elif t == "f":
            return c * 9.0/5.0 + 32
        elif t == "k":
            return c + 273.15
        else:
            raise ValueError("Unsupported temp unit")
