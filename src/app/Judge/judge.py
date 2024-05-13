import paramiko

# 设置SSH连接参数
ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

try:
    # 尝试连接到服务器
    ssh.connect('47.236.92.108', username='root', password='aliserver')
    print("SSH connection successful.")
except paramiko.AuthenticationException:
    print("Authentication failed, please verify your credentials.")
except paramiko.BadHostKeyException as badHostKeyException:
    print("Unable to verify server's host key: %s" % badHostKeyException)
except paramiko.SSHException as sshException:
    print("Unable to establish SSH connection: %s" % sshException)
except Exception as e:
    print("Exception in connecting to the server: %s" % e)

# 设置源文件路径和目标路径
source_file = './code.py'
target_folder = '/opt/code/code.py'

# 使用SFTP传输文件
sftp = ssh.open_sftp()
try:
    sftp.put(source_file, target_folder)
except Exception as e:
    print("Error:", e)

# 运行Docker命令
stdin, stdout, stderr = ssh.exec_command('docker run --rm -v /opt/code:/judge judge python3 /judge/code.py')

# 获取命令的输出
output = stdout.read().decode()
errors = stderr.read().decode()

print("Output:", output)
print("Errors:", errors)

# 删除代码文件
sftp.remove('/opt/code/code.py')

# 关闭连接
sftp.close()
ssh.close()
