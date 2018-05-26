
配置新网站
=========

## 需要安装的包：

* Nginx
* Python3
* Git
* pip
* virtualenv
* libmysqlclient-dev

以Ubuntu为例，可以执行下面的命令安装：

    sudo update
	sudo apt install nginx git python3 python3-pip libmysqlclient-dev
	sudo pip3 install virtualenv

## 配置Nginx虚拟主机

* 参考nginx.template.conf
* 把SITENAME替换成所需的域名，例如staging.my-domain.com
* 把USERNAME替换为服务器的用户名，例如my_name

## Supervisor任务

* 参考gunicorn-supervisor.template.conf
* 把SITENAME替换成所需的域名，例如staging.my-domain.com
* 把USERNAME替换为服务器的用户名，例如my_name

## 文件夹结构：

假设有用户账户，家目录为/home/username

	/home/username
	└─	sites
		└─	SITENAME
			├─	database
			├─	media
			├─	source
			├─	static
			└─	virtualenv
