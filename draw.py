import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator

# 网络名称列表
networks = ['alexnet','mrsa_A', 'vgg16','resnet18']
# best_epe值列表
best_epe_values = [582.6384207, 615.6519859, 337.0406386, 328.6992296]
# epe值列表
epe_values = [386.7932885, 429.1290246, 300.9881132, 170.5108364]
# 提高比率值列表
# improvement_ratios = [0.506330224, 0.434654732, 0.119780562, 0.927732199]
improvement_ratios = [(best - epe) / epe for best, epe in zip(best_epe_values, epe_values)]

# 设置柱状图的宽度
bar_width = 0.2

# 设置x轴的位置
r1 = range(len(networks))
r2 = [x + bar_width for x in r1]

# 创建第一个坐标系并绘制柱状图
fig, ax1 = plt.subplots()

# 设置柱状图颜色为浅蓝色
bar_color1 = 'lightblue'
bar_color2 = 'cornflowerblue'

ax1.bar(r1, best_epe_values, width=bar_width, label='Best_EPE', color=bar_color1)
ax1.bar(r2, epe_values, width=bar_width, label='EPE', color=bar_color2)

ax1.set_xlabel('Network')
ax1.set_ylabel('Values')
ax1.set_title('Comparison of Best_EPE and EPE')
ax1.set_xticks([r + bar_width / 2 for r in range(len(networks))])
ax1.set_xticklabels(networks)
ax1.legend(loc='upper left')

# 创建第二个坐标系并绘制折线图
ax2 = ax1.twinx()

# 设置折线图颜色为深蓝色
line_color = 'navy'

ax2.plot(r1, improvement_ratios, marker='o', label='Improvement Ratio', color=line_color)

ax2.set_ylabel('Improvement Ratio')
ax2.legend(loc='upper right')

# 设置y轴刻度为整数
ax1.yaxis.set_major_locator(MaxNLocator(integer=True))
ax2.yaxis.set_major_locator(MaxNLocator(integer=True))

# 调整布局
fig.tight_layout()

# 显示图形
plt.show()