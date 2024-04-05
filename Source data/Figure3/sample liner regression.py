import pandas as pd
import matplotlib.pyplot as plt
import statsmodels.api as sm

# 读取Excel文件
df = pd.read_excel('/Users/xnh/Desktop/factor_SMW.xlsx')

# 获取因变量列和自变量列的名称
y_column = df.columns[-1]  # 最后一列是因变量
x_columns = df.columns[:-1]  # 假设除最后一列外的其他列都是自变量

# 循环计算每个自变量与因变量的简单线性回归
for x_column in x_columns:
    # 获取因变量和自变量的数据
    y_data = df[y_column]
    x_data = df[x_column]

    # 执行线性回归
    x_data = sm.add_constant(x_data)  # 添加常数项
    model = sm.OLS(y_data, x_data).fit()  # 拟合模型

    # 提取回归模型参数、显著性和R方值
    params = model.params
    pvalues = model.pvalues
    r_squared = model.rsquared

    # 输出回归模型参数、显著性和R方值
    print(f'{y_column} = {params[0]:.4f} + {params[1]:.4f} * {x_column}')
    print(model.summary())

    # 绘制图表
    fig, ax = plt.subplots()
    ax.scatter(x_data[x_column], y_data)
    ax.plot(x_data[x_column], model.predict(), color='red')
    ax.set_xlabel(x_column)
    ax.set_ylabel(y_column)
    ax.text(0.05, 0.9, f'p-value: {pvalues[1]:.4f}', transform=ax.transAxes)
    ax.text(0.05, 0.8, f'R-squared: {r_squared:.4f}', transform=ax.transAxes)
    plt.savefig(f'{y_column}_vs_{x_column}.pdf')
    plt.show()
