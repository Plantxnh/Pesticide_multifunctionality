import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import math

def calculate_hedges_g(meano, meanp, stdo, stdp, no, np):
    """
    Calculate Hedges' g value

    Parameters:
    meano (float): Mean of the first group
    meanp (float): Mean of the second group
    stdo (float): Standard deviation of the first group
    stdp (float): Standard deviation of the second group
    no (int): Sample size of the first group
    np (int): Sample size of the second group

    Returns:
    hedges_g (float): Hedges' g value
    """
    meano, meanp, stdo, stdp, no, np = float(meano), float(meanp), float(stdo), float(stdp), float(no), float(np)

    # Calculate pooled standard deviation
    pooled_std = math.sqrt(((no - 1) * stdo ** 2 + (np - 1) * stdp ** 2) / (no + np - 2))

    # Calculate Hedges' g
    hedges_g = (meano - meanp) / pooled_std

    # Calculate unbiased correction factor
    j = 1 - 3 / (4 * (no + np - 2) - 1)

    # Apply unbiased correction
    hedges_g *= j

    # Variance
    hedges_g_std = (no + np) / (no * np) + (hedges_g**2) / (2 * (no + np))

    # 95% confidence interval
    hedges_g_95_F = hedges_g + 1.96 * math.sqrt(hedges_g_std)
    hedges_g_95_P = hedges_g - 1.96 * math.sqrt(hedges_g_std)

    return hedges_g, hedges_g_std, hedges_g_95_F, hedges_g_95_P

def interaction_effect_size(mean1, mean2, meanu, std1, std2, stdu, number1, number2):
    return (mean1 - meanu) + (mean2 - meanu) + meanu, std1 + std2 - stdu, number1 + number2

def data_process(file):
    df = pd.read_csv(file)
    columns_to_read = ["Pesticide_Risk", "CO2_emissions", "Energy_use", "Industry"]
    y = df["New_MF"]
    x = df[columns_to_read]
    return x, y

def data_paramer(data):
    mean = np.mean(np.array(data), axis=0)
    std = np.std(np.array(data), axis=0)
    if len(np.array(data.shape)) > 1:
        number = [np.array(data.shape, dtype=np.float64)[0] for _ in range(np.array(data.shape)[1])]
    else:
        number = np.array(data.shape, dtype=np.float64)[0]
    return mean, std, number

def drow_mean(names, means, stds, hedges_gs, save_path=None):
    font0 = {'family': 'Times New Roman', 'weight': 'normal'}
    font1 = {'family': 'Times New Roman', 'weight': 'normal', 'size': 19}
    font2 = {'family': 'Times New Roman', 'weight': 'normal', 'size': 16}
    fig = plt.figure(figsize=(10, 14))
    x = range(len(means) + 1)
    for id, (mean, std, hedges_g) in enumerate(zip(means, stds, hedges_gs)):
        plt.plot([mean - std, mean + std], [id + 1, id + 1], color="black")
        plt.scatter(mean, id + 1, color="black")
        plt.text(mean + std + 0.01, id + 0.7, abs(int(hedges_g)), font=font2)
    plt.plot([0, 0], [-1, len(means) + 1], linestyle="--", color="black")

    mean_ = sum(means) / len(means)
    std_ = sum(stds) / len(stds)
    plt.plot([mean_ - std_, mean_ + std_], [0, 0], color="black")
    plt.scatter(mean_, 0, color="black")
    plt.text(mean_ + std_ + 0.01, -0.5, np.sum(np.abs(np.array(hedges_gs, dtype=np.int8))), font=font2)
    names.insert(0, "Overall")
    plt.xlabel(r"Effect size", font=font1)
    plt.yticks(x, names, font=font2)
    plt.yticks(font=font2)
    plt.xticks(font=font2)
    plt.gca().spines['top'].set_visible(False)
    plt.gca().spines['right'].set_visible(False)
    if save_path:
        plt.savefig(save_path, dpi=600, bbox_inches='tight', pad_inches=0.1)

    plt.show()

def single_hedges(x_means, x_stds, x_numbers, y_mean, y_std, y_number, feature_names=["Pesticide_Risk", "CO2_emissions", "Energy_use", "Industry"]):
    names = []
    hedges_gs = []
    hedges_g_stds = []
    hedges_g_95_Fs = []
    hedges_g_95_Ps = []
    for (name, x_mean, x_std, x_number) in zip(feature_names, x_means, x_stds, x_numbers):
        hedges_g, hedges_g_std, hedges_g_95_F, hedges_g_95_P = calculate_hedges_g(meano=x_mean, meanp=y_mean, stdo=x_std, stdp=y_std, no=x_number, np=y_number)
        names.append(name)
        hedges_gs.append(hedges_g)
        hedges_g_stds.append(hedges_g_std)
        hedges_g_95_Fs.append(hedges_g_95_F)
        hedges_g_95_Ps.append(hedges_g_95_P)
        print(name, hedges_g, hedges_g_std, hedges_g_95_F, hedges_g_95_P)
    return names, hedges_gs, hedges_g_stds, hedges_g_95_Fs, hedges_g_95_Ps

def double_hedges(x_means, x_stds, x_numbers, y_mean, y_std, y_number, feature_names):
    names = []
    means = []
    stds = []
    hedges_gs = []
    hedges_g_stds = []
    hedges_g_95_Fs = []
    hedges_g_95_Ps = []
    for x in feature_names:
        for y in feature_names:
            id_x = feature_names.index(x)
            id_y = feature_names.index(y)
            x_mean, x_std, x_number = interaction_effect_size(x_means[id_x], x_means[id_y], y_mean, x_stds[id_x], x_stds[id_y], y_std, x_numbers[id_x], x_numbers[id_y])
            hedges_g, hedges_g_std, hedges_g_95_F, hedges_g_95_P = calculate_hedges_g(meano=x_mean, meanp=y_mean, stdo=x_std, stdp=y_std, no=x_number, np=y_number)
            names.append(x + "-" + y)
            means.append(x_mean)
            stds.append(x_std)
            hedges_gs.append(hedges_g)
            hedges_g_stds.append(hedges_g_std)
            hedges_g_95_Fs.append(hedges_g_95_F)
            hedges_g_95_Ps.append(hedges_g_95_P)
    for name, mean, std, hedges_g, hedges_g_std, hedges_g_95_F, hedges_g_95_P in zip(names, means, stds, hedges_gs, hedges_g_stds, hedges_g_95_Fs, hedges_g_95_Ps):
        print(name, mean, std, hedges_g, hedges_g_std, hedges_g_95_F, hedges_g_95_P)
    return names, means, stds, hedges_gs, hedges_g_stds, hedges_g_95_Fs, hedges_g_95_Ps

if __name__ == "__main__":
    file_path = "/Users/test.csv"
    x, y = data_process(file_path)
    x_means, x_stds, x_numbers = data_paramer(x)
    feature_number = x_means.shape[0]
    y_mean, y_std, y_number = data_paramer(y)
    feature_names = ["Pesticide_Risk", "CO2_emissions", "Energy_use", "Industry"]
    # y_name = ["Multi_funcion_no_kegg"]
    # for (name, x_mean, x_std, x_number) in zip(x_names, x_means, x_stds, x_numbers):
    #     hedges_g = calculate_hedges_g(meano=x_mean, meanp=y_mean, stdo=x_std, std
