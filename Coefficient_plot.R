
#森林图的绘制
#调用R包
library(ggthemes)
library(ggplot2)
#读取数据
dataset <- read.csv(file.choose(),header = T)
dataset <- read.csv("/Volumes/HanCloud1/01农药_土壤多功能性/01数据计算结果/多功能性_因子计算/240201_GLM结果/farmland_GLM.csv",header = T)
#森林图绘制
a<-ggplot(dataset, aes(Coefficient, Index))+
  geom_point(size=2,color = "black")+
  geom_errorbarh(aes(xmax = Coefficient +`SD`, xmin = Coefficient -`SD`),size= 0.2,height = 0.2, colour = "black") +
  scale_x_continuous(limits= c(-0.2, 0.2))+
  geom_vline(aes(xintercept = 0),color="gray",linetype="dashed", size = 0.6) +
  xlab('Coefficient')+ 
  ylab(' ')+
  theme_few()+
  theme(axis.text.x = element_text(size = 20, color = "black"))+
  theme(axis.text.y = element_text(size = 20, color = "black"))+
  theme(title=element_text(size=20))+
  theme_bw()+
  theme(axis.ticks.length=unit(-0.25, "cm"), 
        axis.text.x = element_text(margin=unit(c(0.5,0.5,0.5,0.5), "cm")), 
        axis.text.y = element_text(margin=unit(c(0.5,0.5,0.5,0.5), "cm")) )
#查看图a
a
