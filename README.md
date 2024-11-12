# BUCT_Lecture_Fetch
抢讲座python脚本
ctrl+shift_i,打开开发者工具。
在实践创新活动页，随便点击一个讲座的报名可以看到如下图展示的信息。
![屏幕截图 2024-11-10 143555](https://github.com/user-attachments/assets/e6e6940c-f4f0-4f06-8064-872ee880d4c3)

点击第一个，复制为cURL(bash),复制到https://curlconverter.com
转换为python代码。其中的有些元素可以注释掉，具体方法是注释掉一个看看还能不能成功访问。当然，什么都不管也没有问题。

对于不同的讲座，用同一个不变的cookie和header也是能正常访问的，真正重要的是讲座的id和pprid，而params在函数get_params_list用一个伪请求获取了全部讲座的param

在wait_until函数中，处于对网络的不信任做了一个微小的延时（0.3s），可以自行调整

![屏幕截图 2024-11-10 145209](https://github.com/user-attachments/assets/384efc51-4341-498c-8899-288817faedb9)

结构图如下
![抢讲座脚本-241110232016](https://github.com/user-attachments/assets/151814ff-9829-4919-95f3-91c93ae8bb07)
