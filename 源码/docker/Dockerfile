# 基础镜像
FROM phusion/baseimage
# 软件源加速
COPY sources.list /etc/apt/sources.list
# 支持SSH
RUN rm -f /etc/service/sshd/down
RUN sed -ri 's/^#?PermitRootLogin\s+.*/PermitRootLogin yes/' /etc/ssh/sshd_config

# 安装（如php apache mysql等
RUN apt update
RUN apt-get install python3-pip -y --option=Dpkg::Options::=--force-confdef
RUN pip3 install flask tensorflow==1.12.3 -i https://pypi.tuna.tsinghua.edu.cn/simple some-package
# 添加普通用户ciscn与设置密码
RUN groupadd ciscn && \
	useradd -g ciscn ciscn -m && \
	password=$(openssl passwd -1 -salt 'abcdefg' '123456') && \
	sed -i 's/^ciscn:!/ciscn:'$password'/g' /etc/shadow

# 缺省flag
RUN echo "flag{flag_test}" > "/flag"
RUN chmod 644 /flag

# 复制源码
COPY ./source /var/www/html

# 修改权限
WORKDIR /var/www/html
RUN chown -R ciscn:ciscn . && \
	chmod -R 750 .

# 启动项
COPY ./start.sh /etc/my_init.d/
RUN chmod 755 /etc/my_init.d/start.sh
# USER ciscn
CMD /etc/my_init.d/start.sh