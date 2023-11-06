import pandas as pd
import matplotlib.pyplot as plt

# 读取数据
path_china = r'heliostrome\jip_project\results\sensitivity_Mean_China_soil.xlsx'
path_bangladesh = r'heliostrome\jip_project\results\sensitivity_Mean_Bangladesh_soil.xlsx'
path_morocco = r'heliostrome\jip_project\results\sensitivity_Mean_Morocco_soil.xlsx'

# 用Pandas读取数据
data_china = pd.read_excel(path_china)
data_bangladesh = pd.read_excel(path_bangladesh)
data_morocco = pd.read_excel(path_morocco)

# 定义一个绘图函数
def plot_data(data, country_name):
    fig, ax1 = plt.subplots(figsize=(12, 6))

    # 设置横轴标签
    soil_types = data['soil type']
    index = range(len(soil_types))
    
    # 绘制柱状图
    ax1.bar(index, data['Yield'], width=0.4, label='Yield', color='darkorange', align='center')
    ax1.set_xlabel('Soil Type')
    ax1.set_ylabel('Yield', color='darkorange')
    ax1.tick_params('y', colors='darkorange')
    ax1.set_xticks(index)
    ax1.set_xticklabels(soil_types, rotation=90)

    # 设置第二个y轴
    ax2 = ax1.twinx()
    ax2.bar([i+0.2 for i in index], data['Water Used'], width=0.4, label='Water Used', color='g', align='center',alpha=0.8)
    ax2.set_ylabel('Water Used', color='g')
    ax2.tick_params('y', colors='g')

    # 绘制折线图（均值）
    ax1.plot(index, [data['Yield Actually'].mean()]*len(index), color='brown', linestyle='--', label='Yield Actually')
    ax2.plot(index, [data['Water Used Actually'].mean()]*len(index), color='y', linestyle='--', label='Water Used Actually')

    # 标题和图例
    plt.title(f'Soil Type Sensitivity Analysis for {country_name}')

    # 设置图例位置
    ax1.legend(loc='upper left', bbox_to_anchor=(1.1, 1))
    ax2.legend(loc='upper left', bbox_to_anchor=(1.1, 0.85))

    fig.tight_layout()
    # 显示图表
    plt.show()

# 分别为三个国家绘图
plot_data(data_china, 'China')
plot_data(data_bangladesh, 'Bangladesh')
plot_data(data_morocco, 'Morocco')
