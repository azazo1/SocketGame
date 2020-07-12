# coding=utf-8


class MessageTransfer:
    """以字典形式保存信息"""

    def __init__(self):
        self.dict = {}

    def get(self, char_name: str) -> dict:
        return self.dict[char_name]

    def get_all(self) -> dict:
        return self.dict

    def pop(self, char_name: str) -> dict:
        get = self.get(char_name)
        self.set(char_name)  # 清空
        return get

    def set(self, char_name, data: dict = None):
        if data is None:
            data = {}
        self.dict[char_name] = data

    def __bool__(self) -> bool:
        return bool(self.dict[0])


if __name__ == '__main__':
    print(not MessageTransfer())
