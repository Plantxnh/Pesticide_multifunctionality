# Install the plspm package
# install.packages('devtools')
# devtools::install_github('gastonstat/plspm')

# Load the plspm package
library(plspm)

# Read data
# dat <- read.delim('environment_community.txt', sep = '\t')
dat <- read.csv("Demo_Non_farmland_full_factors.csv", header = TRUE, row.names = 1)

# Specify latent variables, stored as a list in R to represent the relationships between variables and latent variables
# You can specify column names directly, or specify column indexes. I prefer to specify column names personally
# There should be no comma after the last block. For example, there should be no comma after EMF = 'EMF' here
dat_blocks <- list(
    space = c('longitude', 'latitude'), 
    climate = c('Temp', 'PET', 'AI'), 
    soil = c('pH', 'OC', 'TN'), 
    community = 'species_richness', 
    Multifunctionality = 'EMF'
)

dat_blocks <- list(
  Climate = c('Annual_Mean_Temperature', 'Annual_Precipitation','Mean_Diurnal_Range'), 
  Human = c('Urban_Expansion', 'CO2_emissions__metric_tons_per_capita_', 'Energy_use__kg_of_oil_equivalent_per_capita_','GDP','GNI_PPP__current_international','Industry__including_construction','Population_density'), 
  Land_use = c('Pesticide_usage', 'Nitrogen_Fertilizer_Application', 'Phosphorus_Fertilizer_Application','Agriculture_Expansion','Agriculture_forestry_and_fishing_value_added','Terrestrial_and_marine_protected_areas','Crop_Harvested','CEC_9','CACO3_9','TN_9','BD_9'), 
  Pesticide_risk = 'PR', 
  Soil_nutrition = c('TS_9', 'TP_9', 'TK_9','TC_9','PHH2O_9','OC_9','ECE_9','CEC_9','CACO3_9','TN_9','BD_9'), 
  Multifunctionality = 'Multi_funcion_nokegg_noVB12'
)
dat_blocks

# Describe the associations between latent variables with a 0-1 matrix, where 0 means no association between variables, and 1 means there is an association
space <- c(0, 0, 0, 0, 0)
climate <- c(1, 0, 0, 0, 0)
soil <- c(1, 1, 0, 0, 0)
community <- c(1, 1, 1, 0, 0)
EMF <- c(1, 1, 1, 1, 0)


Climate <- c(0, 0, 0, 0, 0, 0)
Human <- c(0, 0, 0, 0, 0, 0)
Land_use <- c(0, 0, 0, 0, 0, 0)
Pesticide_risk <- c(0, 0, 0, 0, 0, 0)
Soil_nutrition <- c(1, 1, 1, 1, 0, 0)
Multifunctionality <- c(1, 1, 1, 1, 1, 0)


dat_path <- rbind(space, climate, soil, community, EMF)

dat_path <- rbind(Climate, Human,Land_use,Pesticide_risk, Soil_nutrition, Multifunctionality)
colnames(dat_path) <- rownames(dat_path)
dat_path

# Specify causal relationships, either A (column is the cause of the row) or B (row is the cause of the column)
# If there are n latent variables, change the number to n. Here, there are space, climate, soil, community, EMF, so the number is 5
dat_modes <- rep('A', 6)
dat_modes

## A simple PLS-PM, for more parameter details, check ?plspm
dat_pls <- plspm(dat, dat_path, dat_blocks, modes = dat_modes)
dat_pls
summary(dat_pls)

# The result contains a lot of content, for detailed parts please refer to the user manual of the plspm package:
# Full version manual, 235 pages: https://www.gastonsanchez.com/PLS_Path_Modeling_with_R.pdf
# Short version manual, 10 pages: https://rdrr.io/cran/plspm/f/inst/doc/plspm_introduction.pdf

# The following only shows a relatively important part

# View parameter estimates of path coefficients and related statistical information
dat_pls$path_coefs
dat_pls$inner_model

# View the causal relationship path diagram, details ?innerplot
innerplot(dat_pls, colpos = 'red', colneg = 'blue', show.values = TRUE, lcol = 'gray', box.lwd = 0)

# View the status of exogenous latent variables and endogenous latent variables
dat_pls$inner_summary

# View the influence status between variables
dat_pls$effects

# View the relationship between observed variables and latent variables, you can use outerplot() to draw a graph similar to the path diagram, details ?outerplot
dat_pls$outer_model
outerplot(dat_pls, what = 'loadings', arr.width = 0.1, colpos = 'red', colneg = 'blue', show.values = TRUE, lcol = 'gray')
outerplot(dat_pls, what = 'weights', arr.width = 0.1, colpos = 'red', colneg = 'blue', show.values = TRUE, lcol = 'gray')

# Goodness-of-fit values can help evaluate model adequacy
dat_pls$gof

# View latent variable scores, which can be understood as standardized values of latent variables
dat_pls$scores

# Output values of latent variables
# latent <- data.frame(dat_pls$scores)
# latent <- cbind(dat$site, latent)
# write.csv(latent, 'latent.csv')
