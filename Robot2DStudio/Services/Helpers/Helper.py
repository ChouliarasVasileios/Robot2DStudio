class Helper:
    @staticmethod
    def ToCamelCase(string :str) -> str:
        string = string[0].lower() + string[1:]
        return string