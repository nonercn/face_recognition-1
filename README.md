### 使用
#### 端口
~~~
8888 正式服务端口
8887 开发测试端口
~~~

#### 方法
> /encode GET
~~~
作用: 扫描并解析 /opt/face 目录下人脸
参数: 无
返回值: 人脸对象数组 
    eg. [{"name":"李三","encode":[1,2,3,4,5,6...]},"name":"王二","encode":[]]
~~~
> /encode POST
~~~
作用: 解析 传入 人脸
参数: file 未知人脸 图片
返回值: 人脸对象 
~~~

> /distance POST
~~~
作用: 从kowns 获得与 unkown 的对比值
参数: unkown 未知人脸 encode 码
      kowns 已知人脸 encode 码 数组
返回值: 对比值数组
~~~

### 打包
> 推荐 daoCloud 云打包 (由于网络原因)

https://dashboard.daocloud.io

### 离线部署
#### 下载
> 拉取 daoCloud 打好的镜像
~~~
docker pull xx
~~~
> 保存离线镜像
~~~
docker save -o xx.docker xx
~~~
> 下载离线docker

~~~
curl -L https://github.com/wyp0596/docker-installer/releases/download/v1.1.0/RPM-based.tar.gz > RPM-based.tar.gz
~~~
#### 部署
> 安装离线docker
~~~
tar -xzf RPM-based.tar.gz 
cd RPM-based/docker
sudo sh install.sh
~~~
> 加载离线镜像
~~~
docker load -i xx.docker
~~~
> 运行离线镜像
~~~
docker run -d -p 8888:8888 -p 8887:8887 --name face -v /本机人脸路径:/opt/face xx
~~~

#### 开发测试
> 挂载 测试代码
~~~
docker run -d -p 8888:8888 -p 8887:8887 --name face -v /本机人脸路径:/opt/face -v /本机测试代码:/opt/run xx
~~~
> 进入容器
~~~
docker exec -it xx bash
cd /opt/run
~~~
> 启动测试代码
~~~
python xxx.py
~~~