from flask import request, Blueprint, g
from sqlalchemy import text

from ..Utils import toJSON
from ..DB_models.models import Students
from flask_jwt_extended import jwt_required, get_jwt_identity
from ..Utils.FormatConversion import toDataFrame

# 创建路由蓝图
rank_blue = Blueprint('rank', __name__)


@rank_blue.route('/', methods=['GET'])
def get_rank():
    with g.sql_session.create_session() as session:
        # 定义SQL查询字符串
        query = text("""
                    SELECT
                        student_id AS username,
                        COUNT(submission_id) AS submission_count,
                        SUM(CASE WHEN status = 'Accepted' THEN 1 ELSE 0 END) / COUNT(submission_id) AS pass_rate
                    FROM
                        submit_records
                    WHERE
                        student_id IS NOT NULL
                    GROUP BY
                        student_id
                    ORDER BY
                        pass_rate DESC

                """)

        # 执行查询
        res = session.execute(query)

        df_res = toDataFrame(res)
        print(df_res)
        # 将查询结果转换为JSON
        json_res = df_res.to_json(orient='records')

        # 返回JSON响应
        return json_res