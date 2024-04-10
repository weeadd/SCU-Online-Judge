import datetime
from flask import Blueprint
from ..DataAnalyse.SQLSession import get_session
from ..DB_models import AbnormalPoseRecord


# 创建路由蓝图
workbench_blue = Blueprint('workbench', __name__)



@workbench_blue.route('/')
def workbench():
    print('workbench')
    return 'workbench'


# 将不良坐姿数据写入数据库
def write_bad_posture_to_db(bad_poses):
    with get_session() as session:
        # 创建一个新的 AbnormalPoseRecord 对象，并添加到数据库会话中
        abnormal_pose_record = AbnormalPoseRecord(
            timestamp=datetime.now(),
            head_left='1' if 'head_left' in bad_poses else None,
            head_right='1' if 'head_right' in bad_poses else None,
            hunchback='1' if 'hunchback' in bad_poses else None,
            chin_in_hands='1' if 'chin_in_hands' in bad_poses else None,
            body_left='1' if 'body_left' in bad_poses else None,
            body_right='1' if 'body_right' in bad_poses else None,
            neck_forward='1' if 'neck_forward' in bad_poses else None,
            shoulder_left='1' if 'shoulder_left' in bad_poses else None,
            shoulder_right='1' if 'shoulder_right' in bad_poses else None,
            twisted_head='1' if 'twisted_head' in bad_poses else None
        )
        session.add(abnormal_pose_record)
        session.commit()