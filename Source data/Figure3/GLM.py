import pandas as pd
import statsmodels.api as sm

# Read CSV data with tab delimiter
data = pd.read_csv('Demo_factor_cultivated.csv', delimiter=',')

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
