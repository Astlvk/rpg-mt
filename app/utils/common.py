import os
import sys


def get_resource_path(resource_path: str = ""):
    """
    获取资源路径，
    打包后运行时，资源会在 sys._MEIPASS 目录中（单文件与非单文件打包位置不同，但都可以sys._MEIPASS获取），
    开发环境下，获取根目录中的资源

    :param resource_path: 资源路径
    :return: 资源路径
    """
    if getattr(sys, "frozen", False):
        # 打包后运行时，资源会在 sys._MEIPASS 目录中
        base_path = getattr(sys, "_MEIPASS", os.path.dirname(os.path.abspath(__file__)))
        # print(base_path)
    else:
        # 开发环境下，资源在当前脚本所在目录
        base_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../"))
        # print(base_path)
    return os.path.join(base_path, resource_path)


if __name__ == "__main__":
    get_resource_path()
