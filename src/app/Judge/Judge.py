import paramiko
import tempfile
import os
from flask import Blueprint, jsonify, request

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

    return ssh,connection_status

def compile(ssh, connection_status, local_file_path, language):
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

        stdin, stdout, stderr = ssh.exec_command(command)

        # 获取命令的输出
        output = stdout.read().decode()
        errors = stderr.read().decode()

        print("Output:", output)
        print("Errors:", errors)

        # 删除代码文件
        sftp.remove(target_folder)

        # 关闭连接
        sftp.close()
        ssh.close()

        res = jsonify({
            "connection_status": connection_status,
            "output": output,
            "errors": errors
        })
    else:
        res = jsonify({
            "connection_status": connection_status
        })

    return res

@judge_blue.route('/submit', methods=['POST'])
def judge():
    data = request.json
    print(data)
    pid = data.get('pid')
    code = data.get('code')
    language = data.get('language')

    if not all([pid, code, language]):
        return jsonify({"status": 400, "message": "Missing required parameters"}), 400

    project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..'))
    tmp_dir = os.path.join(project_root, 'tmp')

    if not os.path.exists(tmp_dir):
        os.makedirs(tmp_dir)

    with tempfile.NamedTemporaryFile(delete=False, suffix=".py" if language == 'python' else ".c", dir=tmp_dir) as temp_file:
        temp_file.write(code.encode())
        temp_file_path = temp_file.name

    # 设置SSH连接
    ssh,connection_status = connect_ssh()
    res = compile(ssh, connection_status, temp_file_path, language)

    os.remove(temp_file_path)

    print(res)
    return res