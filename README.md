# rclone_scripts
## upload.py
主要解决了当种子文件太大，导致无法一次性下载到本地硬盘时，可以边下载，边上传已完全下载的文件到云，并删除成功上传的文件，达到将远大于本地硬盘大小的种子文件上传到云的目的。

**请谨慎使用，边下边删有违BT/PT精神，甚至可能违反TOS**
### 用法
需要将qbittorrent做以下设置
1. 打开给未完成的文件添加!qB后缀的选项。
2. 由于未使用service account，需限制全局下载速度到8.5MB及以下。
3. 限制全局最大下载数为1。
4. 禁止种子上传，具体做法是开启Seed limits中When ratio reaches 0。

然后自行配置好rclone，并将upload.py中的SOURCE_PATH_LIST修改为qb的下载路径，DESTINATION_PATH_LIST修改为云端的路径。

最后配置crontab，每2分钟执行一次python3 upload.py即可。
## rclone_gd.service
这里是rclone挂载google drive的systemd配置，挂载参数对流媒体播放做了一些优化，可以自行使用。
