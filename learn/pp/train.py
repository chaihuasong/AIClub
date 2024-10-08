# https://blog.csdn.net/weixin_72787227/article/details/135569544
import paddle

# 指定在 CPU 上训练
paddle.device.set_device('cpu')

# 指定在 GPU 第 0 号卡上训练
#paddle.device.set_device('gpu:0')


from paddle.vision.transforms import Normalize

######################数据准备########################################
#####################################################################
transform = Normalize(mean=[127.5], std=[127.5], data_format='CHW')
# 加载 MNIST 训练集和测试集
train_dataset = paddle.vision.datasets.MNIST(mode='train', transform=transform)
test_dataset = paddle.vision.datasets.MNIST(mode='test', transform=transform)
######################模型组网########################################
#####################################################################
# 模型组网，构建并初始化一个模型 mnist
mnist = paddle.nn.Sequential(
    paddle.nn.Flatten(1, -1),
    paddle.nn.Linear(784, 512),
    paddle.nn.ReLU(),
    paddle.nn.Dropout(0.2),
    paddle.nn.Linear(512, 10)
)
######################封装模型########################################
######################！paddle.Model！################################
# 封装模型为一个 model 实例，便于进行后续的训练、评估和推理
model = paddle.Model(mnist)
######################配置训练准备参数#################################
######################！Model.prepare！###############################
# 为模型训练做准备，设置优化器及其学习率，并将网络的参数传入优化器，设置损失函数和精度计算方式
model.prepare(optimizer=paddle.optimizer.Adam(learning_rate=0.001, parameters=model.parameters()),
              loss=paddle.nn.CrossEntropyLoss(),
              metrics=paddle.metric.Accuracy())
######################训练模型#######################################
#####################！Model.fit！###################################
# 启动模型训练，指定训练数据集，设置训练轮次，设置每次数据集计算的批次大小，设置日志格式
model.fit(train_dataset,
          epochs=5,  # 循环次数
          batch_size=64,  # 每批次的数量
          verbose=1)  # 日志

######################评估模型#######################################
#####################！Model.evaluate！##############################
# 用 evaluate 在测试集上对模型进行验证
eval_result = model.evaluate(test_dataset, verbose=1)
print(eval_result)
######################执行推理#######################################
#####################！Model.predict！##############################

# 用 predict 在测试集上对模型进行推理
###############
###############
test_result = model.predict(test_dataset)
###############
###############
# 由于模型是单一输出，test_result的形状为[1, 10000]，10000是测试数据集的数据量。这里打印第一个数据的结果，这个数组表示每个数字的预测概率
print(len(test_result))
print(test_result[0][0])

# 从测试集中取出一张图片
img, label = test_dataset[0]

# 打印推理结果，这里的argmax函数用于取出预测值中概率最高的一个的下标，作为预测标签
pred_label = test_result[0][0].argmax()
print('true label: {}, pred label: {}'.format(label[0], pred_label))

# 使用matplotlib库，可视化图片
from matplotlib import pyplot as plt
import pylab
plt.imshow(img[0])
# 解决imshow无法显示问题
pylab.show()
