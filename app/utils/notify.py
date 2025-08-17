from windows_toasts import WindowsToaster, Toast, ToastDisplayImage, ToastDuration
from app.utils.common import get_resource_path

newToast = Toast()


def notify(
    title: str,
    msg: str,
    notice_title: str = "CrmPlugin",
    duration: ToastDuration = ToastDuration.Short,
    launch_action: str | None = None,
):
    """
    弹出系统通知
    :param title: 通知标题
    :param msg: 通知正文
    :param notice_title: 通知栏标题
    :param duration: 通知持续时间
    :param launch_action: 通知点击后执行的动作
    """
    toaster = WindowsToaster(notice_title)
    # Set the body of the notification
    newToast.text_fields = [title, msg]
    newToast.AddImage(
        ToastDisplayImage.fromPath(get_resource_path("resources/logo.ico"))
    )
    newToast.duration = duration
    if launch_action:
        newToast.launch_action = launch_action
    # And display it!
    toaster.show_toast(newToast)
