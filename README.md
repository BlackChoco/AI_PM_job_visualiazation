AI产品经理实习岗位职责和岗位需求的可视化项目： 

processed_job_details.csv：职位数据   
job_analysis.ipynb：用于可视化的jupyter脚本   
requirements.txt：必要安装的库   

可视化结果：   
description_visual.html：岗位职责的3D可视化   
descriptions_triple_graph.png：岗位职责的实体图可视化   
requirement_visual.html：岗位需求的3D可视化   
requirements_triple_graph.png：岗位需求的实体图可视化   

！！！运行job_analysis.ipynb时   
1.安装requirements.txt中必要的库   
2.另外配置.env文件，使用阿里云百炼平台，内容包括：   
API_KEY= "your_api_key（填写你的apikey）"   
BASE_URL= https://dashscope.aliyuncs.com/compatible-mode/v1   
MODEL_NAME= "model_name（填写你使用的model名字）"   
3.使用huggingface的jina_embeddingv3进行embed，所以需要梯来下载模型

目标公司：
1.美团（已爬）
2.字节（已爬）
3.腾讯（很少关于AI产品经理实习的信息）
4.淘天（已爬）
5.阿里云（已爬）
6.蚂蚁（没有）
7.百度（已爬）
8.网易（已爬）
9.小红书（已爬）
10.快手（已爬）
11.小米（已爬）


分析思路：   
1.将所有requirement和description通过embedmodel进行聚类   
2.将实体以及实体关系提取出来，并进行graph的可视化   

