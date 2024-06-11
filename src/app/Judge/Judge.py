import datetime
import time
import paramiko
import tempfile
import os
from flask import Blueprint, jsonify, request, g
from .AST import get_ast_analysis
from ..DB_models.models import SubmitRecords

judge_blue = Blueprint('judge', __name__)


def connect_ssh():
    # 设置SSH连接参数
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    try:
        # 尝试连接到服务器
        ssh.connect('47.236.92.108', username='root', password='aliserver')
        connection_status = "SSH connection successful."
    except paramiko.AuthenticationException:
        connection_status = "Authentication failed, please verify your credentials."
    except paramiko.BadHostKeyException as badHostKeyException:
        connection_status = f"Unable to verify server's host key: {badHostKeyException}"
    except paramiko.SSHException as sshException:
        connection_status = f"Unable to establish SSH connection: {sshException}"
    except Exception as e:
        connection_status = f"Exception in connecting to the server: {e}"

    return ssh, connection_status


def compile(ssh, connection_status, local_file_path, language, expected_output):
    if "successful" in connection_status:
        # 设置源文件路径和目标路径
        target_folder = '/opt/code/code.py' if language == 'python' else '/opt/code/code.c'

        # 使用SFTP传输文件
        sftp = ssh.open_sftp()

        try:
            sftp.put(local_file_path, target_folder)
        except Exception as e:
            print("Error:", e)

        # 运行Docker命令
        if language == 'python':
            command = 'docker run --rm -v /opt/code:/judge judge python3 /judge/code.py'
        elif language == 'c':
            command = 'docker run --rm -v /opt/code:/judge judge gcc /judge/code.c -o /judge/code && /judge/code'
        else:
            command = 'echo "Unsupported language"'

        start_time = time.time()

        stdin, stdout, stderr = ssh.exec_command(command)

        # 获取命令的输出
        output = stdout.read().decode().strip()
        errors = stderr.read().decode().strip()

        end_time = time.time()

        memory_usage = "2000KB"

        # 删除代码文件
        sftp.remove(target_folder)

        # 关闭连接
        sftp.close()
        ssh.close()

        # 判断编译和运行结果
        if errors:
            status = "Compilation Error" if "error" in errors.lower() else "Runtime Error"
        else:
            status = "Accepted" if output == expected_output else "Wrong Answer"

        execution_time = end_time - start_time

    else:
        status = "Connection Error"

    return output, memory_usage, execution_time, status


def get_expected_output(question_id):
    expected_outputs = {
        "2": "0.4054\n-0.1019\n0.1172\n0.0936",
        "3": "[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 21, 22, 23, 24]",
        "4": "C\nD\nE\nerror\nA",
        "5": "128425485935180313",
        "6": "4.3478\n20.0000\nZeroDivisionError: division by zero\n1.3158\nTypeError: unsupported operand type(s) for /: 'int' and 'str'\n1.5152",
        "7": "3\n['HELLO', 'SEVEN', ['MON', ['H', 'KELLY'], 'ALL'], 123, 446]",
        "8": "The,recommended,price,of,the,jacket,is,223344000,CNY,but,today,all,goods,90%,~,99%,off,the,recommended,rice,Now,the,estimated,sale,price,of,the,jacket,is,only,112556,CNY.",
        "9": "{0, 6, 7, 8, 9}",
        "10": "[1, 4, 6, 8, 9, 10, 12, 14, 15, 16, 18, 20, 21, 22, 24, 25, 26, 27, 28, 30, 32, 33, 34, 35, 36, 38, 39, 40, 42, 44, 45, 46, 48, 49, 50, 51, 52, 54, 55, 56, 57, 58, 60, 62, 63, 64, 65, 66, 68, 69, 70, 72, 74, 75, 76, 77, 78, 80, 81, 82, 84, 85, 86, 87, 88, 90, 91, 92, 93, 94, 95, 96, 98, 99, 100]",
    }
    return expected_outputs[question_id]


def get_judge_result(code, language, question_id):
    project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..'))
    tmp_dir = os.path.join(project_root, 'tmp')

    if not os.path.exists(tmp_dir):
        os.makedirs(tmp_dir)

    with tempfile.NamedTemporaryFile(delete=False, suffix=".py" if language == 'python' else ".c",
                                     dir=tmp_dir) as temp_file:
        temp_file.write(code.encode())
        temp_file_path = temp_file.name

    # 获取预期输出
    expected_output = get_expected_output(question_id)

    # 设置SSH连接
    ssh, connection_status = connect_ssh()
    output, memory_usage, execution_time, status = compile(ssh, connection_status, temp_file_path, language, expected_output)

    #获取ast分析
    ast_status, ast_advice = get_ast_analysis(question_id, temp_file_path, language)

    res = {
        "connection_status": connection_status,
        "output": output,
        "execution_time": execution_time,
        "memory_usage": memory_usage,
        "submit_time": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "ast_status": ast_status,
        "ast_advice": ast_advice,
        "status": status
    }

    os.remove(temp_file_path)

    return res


def write_submission_to_database(submission_record):
    with g.sql_session.create_session() as session:
        session.add(submission_record)
        session.commit()


@judge_blue.route('/submit', methods=['POST'])
def judge():
    data = request.json
    question_id = data.get('question_id')
    student_id = data.get('student_id')
    submitter = data.get('submitter')
    code = data.get('code')
    language = data.get('language')

    if not all([question_id, code, language]):
        return jsonify({"status": 400, "message": "Missing required parameters"}), 400

    res = get_judge_result(code, language, question_id)
    res["question_id"] = question_id
    res["submitter"] = submitter

    # 创建数据库记录
    submission_record = SubmitRecords(
        submission_id=None,
        question_id=question_id,
        student_id=student_id,
        submitter=submitter,
        code=code,
        memory=res['memory_usage'],
        execution_time=res['execution_time'],
        status=res['status'],
        ast_status=res['ast_status'],
        ast_advice=res['ast_advice'],
        output=res['output'],
        submit_time=res['submit_time']
    )

    # 将提交记录写入数据库
    write_submission_to_database(submission_record)


    return res
