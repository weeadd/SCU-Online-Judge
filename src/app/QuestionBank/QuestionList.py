from flask import request, Blueprint,g

from ..Utils import get_all_questions
from .Filter import filter,sort

# 创建路由蓝图
questionbank_blue = Blueprint('questionbank', __name__)

@questionbank_blue.route('/')
def get_list():
    # 获取搜索文本参数
    query = request.args.get('query')
    # 获取排序和筛选相关参数
    sortBy = request.args.get('sortBy')
    language_condition = request.args.get('language')

    questions_df = get_all_questions()

    # 根据题目进行模糊查询
    if query is not None and query != '':
        questions_df = questions_df[questions_df['title'].str.contains(query, case=False)]

    # 处理筛选条件
    filter_conditions = {}

    if language_condition is not None and language_condition != '':
        filter_conditions['language'] = language_condition

    # 根据条件进行筛选
    questions_df = filter(questions_df, filter_conditions)

    # 根据条件进行排序
    if sortBy is not None and sortBy != '':
        questions_df = sort(questions_df, sortBy)

    # 返回最终题目列表
    json_res = questions_df.to_json(orient='records')

    return json_res

# 创建动态路由，匹配题目名字作为子路由
@questionbank_blue.route('/<question>')
def question_detail(question):
    # 在这里可以根据题目名字做相应的处理，比如返回特定的题目信息
    return f"This is the detail page for {question}"