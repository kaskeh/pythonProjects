from django.core.files.storage import Storage
from fdfs_client.client import Fdfs_client, get_tracker_conf


class FastDFSStorage(Storage):
    """ 自定义文件存储系统类 """

    def __init__(self):
        pass

    def _open(self, name, mode="rb"):
        """
        用来打开文件的，但是我们自定义文件存储系统的目的是为了实现存储到远程的FastDFS服务器，不需要打开文件，所以此方法重写后什么也不做
        :param name:
        :param mode:
        :return:
        """

    def _save(self, name, content):
        """
        文件存储时调用此方法，但是此方法默认是向本地存储，在此重写方法实现文件存储到远程的FastDFS服务器
        :param name: 要上传的文件名
        :param content: 以rb模式打开的文件对象，将来通过content.read() 就可以读取到文件的二进制数据
        :return: file_id
        """

        # 1. 创建FastDFS 客户端
        tracker_path = get_tracker_conf('meiduo_mail/utils/fastdfs/client.conf')
        client = Fdfs_client(tracker_path)

        # 2. 通过客户端调用上传文件的方式上传文件到fastDFS服务器
        # client.upload_by_filename("要写上传文件的绝对路径") 只能通过文件绝对路径进行上传，此方式上传的文件会有后缀
        # upload_by_buffer 可以通过文件二进制数据进行上传 上传后的文件没有后缀
        ret = client.upload_by_buffer(content.read())

        # 3. 判断文件是否上传成功
        if ret.get("Status") != "Upload successd.":
            raise Exception("Upload fiel failed")

        # 3.1 获取file_id
        file_id = ret.get("Remote file_id")

        # 4. 返回file_id
        return file_id

    def exists(self, name):
        pass

    def url(self, name):
        pass