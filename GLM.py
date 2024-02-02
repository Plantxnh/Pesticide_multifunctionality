import pandas as pd
import statsmodels.api as sm

# Read CSV data with tab delimiter
data = pd.read_csv('/Volumes/HanCloud1/01农药_土壤多功能性/01数据计算结果/多功能性_因子计算/1017_GLM结果/Farmland_MF_Factors.csv', delimiter=',')

# Define independent variables (explanatory variables) and dependent variable (response variable)
X = data[['PR', 'Climate', 'Soil', 'Human', 'Land_use']]
y = data['Multifunctionality']

# Add a constant term (intercept term)
X = sm.add_constant(X)

# Create a generalized linear model
model = sm.GLM(y, X, family=sm.families.Gaussian())

# Fit the model
results = model.fit()

# Print model summary
print(results.summary())
