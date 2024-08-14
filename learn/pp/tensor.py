# 创建一维Tensor
import paddle

# 1.1指定数据创建
ndim_1_Tensor = paddle.to_tensor([2.0, 3.0, 4.0])

# 创建二维Tensor
ndim_2_Tensor = paddle.to_tensor([[1.0, 2.0, 3.0],
                                  [4.0, 5.0, 6.0]])
# 创建三维Tensor
ndim_3_Tensor = paddle.to_tensor([[[1, 2, 3, 4, 5],
                                   [6, 7, 8, 9, 10]],
                                  [[11, 12, 13, 14, 15],
                                   [16, 17, 18, 19, 20]]])

print(ndim_1_Tensor)
print(ndim_2_Tensor)
print(ndim_3_Tensor)

# output:
"""
Tensor(shape=[3], dtype=float32, place=Place(cpu), stop_gradient=True,
       [2., 3., 4.])
Tensor(shape=[2, 3], dtype=float32, place=Place(cpu), stop_gradient=True,
       [[1., 2., 3.],
        [4., 5., 6.]])
Tensor(shape=[2, 2, 5], dtype=int64, place=Place(cpu), stop_gradient=True,
       [[[1 , 2 , 3 , 4 , 5 ],
         [6 , 7 , 8 , 9 , 10]],

        [[11, 12, 13, 14, 15],
         [16, 17, 18, 19, 20]]])
"""

# 1.2指定形状创建
# paddle.zeros([m, n])             # 创建数据全为 0，形状为 [m, n] 的 Tensor
# paddle.ones([m, n])              # 创建数据全为 1，形状为 [m, n] 的 Tensor
# paddle.full([m, n], 10)          # 创建数据全为 10，形状为 [m, n] 的Tensor
# paddle.empty(shape=[3, 2])       # 创建数据全为 1，形状为 [3, 2] 的Tensor

# 1.3指定区间创建
# paddle.arange(start, end, step)
# 创建以步长 step 均匀分隔区间[start, end)的 Tensor

# paddle.linspace(start, stop, num)
# 创建以元素个数 num 均匀分隔区间[start, stop)的 Tensor


# 1.4指定对象创建
"""
创建一个与其他 Tensor 具有相同 shape 与 dtype 的 Tensor，可通过 paddle.ones_like 、 paddle.zeros_like 、 paddle.full_like 、paddle.empty_like 实现
拷贝并创建一个与其他 Tensor 完全相同的 Tensor，可通过 paddle.clone 实现。
"""
#y = paddle.ones_like(x)
#y = paddle.clone(x)

# 创建一个满足特定分布的 Tensor
# 服从均匀分布的、范围在[low, high)的随机 Tensor，形状为 shape
#out1 = paddle.randint(low=-5, high=5, shape=[2, 3])

# 符合均匀分布的、范围在[0, 1)的 Tensor，形状为 shape
#out1 = paddle.rand(shape=[2, 3])

# 符合标准正态分布的随机 Tensor，形状为 shape
#out1 = paddle.randn(shape=[2, 3])

# 直接将 PIL.Image 格式的数据转为 Tensor
from PIL import Image
import paddle
import paddle.vision.transforms as T
import paddle.vision.transforms.functional as F

img_arr = ((paddle.rand((4, 5, 3)) * 255.).astype('uint8')).numpy()
fake_img = Image.fromarray(img_arr)
# 将形状为 （H x W x C）的输入数据
# PIL.Image 或 numpy.ndarray 转换为 (C x H x W)
transform = T.ToTensor()
tensor = transform(fake_img)
