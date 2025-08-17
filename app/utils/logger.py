import os
import traceback
import logging


class LoggerConfig:
    """可动态配置日志路径的日志管理器"""

    def __init__(self, log_path: str | None = None):
        # 设置默认日志路径（如果未指定）
        self.log_path = log_path or os.path.abspath("logs")
        self._create_log_dir()

        # 日志格式
        self.log_format = (
            "%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s: %(message)s"
        )

        # 初始化日志配置
        self._configure_logging()

    def _create_log_dir(self):
        """创建日志目录（如果不存在）"""
        if not os.path.exists(self.log_path):
            os.makedirs(self.log_path, exist_ok=True)

    def _configure_logging(self):
        """配置 logging 模块"""
        # 重置根日志记录器（避免重复添加处理器）
        root_logger = logging.getLogger()
        root_logger.handlers.clear()

        # 基础配置
        logging.basicConfig(
            level=logging.INFO,
            format=self.log_format,
            handlers=[
                self._create_error_handler(),
                self._create_info_handler(),
                self._create_console_handler(),  # 可选：启用控制台输出
            ],
        )

    def _create_error_handler(self) -> logging.Handler:
        """创建错误日志处理器"""
        handler = logging.FileHandler(
            os.path.join(self.log_path, "error.log"), encoding="utf-8"
        )
        handler.setLevel(logging.ERROR)
        handler.setFormatter(logging.Formatter(self.log_format))
        handler.addFilter(ErrorFilter())
        return handler

    def _create_info_handler(self) -> logging.Handler:
        """创建信息日志处理器"""
        handler = logging.FileHandler(
            os.path.join(self.log_path, "info.log"), encoding="utf-8"
        )
        handler.setLevel(logging.INFO)
        handler.setFormatter(logging.Formatter(self.log_format))
        handler.addFilter(InfoFilter())
        return handler

    def _create_console_handler(self) -> logging.Handler:
        """创建控制台处理器（可选）"""
        console = logging.StreamHandler()
        console.setLevel(logging.DEBUG)
        console.setFormatter(logging.Formatter(self.log_format))
        return console


# 定义过滤器（保持原逻辑）
class ErrorFilter(logging.Filter):
    def filter(self, record):
        return record.levelno == logging.ERROR


class InfoFilter(logging.Filter):
    def filter(self, record):
        return record.levelno == logging.INFO


def log_exception(e: Exception, bubbling: bool = False):
    """
    记录错误日志，并使用print输出，可选的继续抛出异常

    :param e: 异常对象
    :param bubbling: 是否继续抛出异常
    """
    error_msg = traceback.format_exc()
    error_msg = "".join(error_msg)
    print(error_msg)
    logging.exception(e)
    if bubbling:
        raise e


def clear_log_file(log_path: str):
    """清空指定日志文件内容"""
    if os.path.exists(log_path):
        with open(log_path, "w") as f:
            f.truncate(0)  # 清空文件内容
        print(f"日志文件 {log_path} 已清空")
    else:
        print(f"日志文件 {log_path} 不存在")


def clear_log(log_dir: str):
    """
    清空日志文件

    :param log_dir: 日志目录路径
    """
    # 清空错误日志
    clear_log_file(log_dir + "/error.log")


# 使用示例 -----------------------------------------------------------------
if __name__ == "__main__":
    # 动态设置不同日志路径
    logger1 = LoggerConfig(log_path="./logs/app1_logs")
    logger2 = LoggerConfig(log_path="./logs/app2_logs")
    logger3 = LoggerConfig(log_path="./logs/app3_logs")

    # 测试日志输出
    logging.error("This is an error message")
    logging.info("This is an info message")
