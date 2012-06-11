library(cluster)

# Chargement et épuration des données.
seal <- read.csv('constant.csv',sep='$',header=FALSE)
mydata <- seal[,2:length(seal)]
g <- length(mydata[,1])
mydata <- mydata[1:g-1,]




nbre_cluster <- 20
# Normalisation des données
for(i in 1:length(mydata))
    mydata[,i]=mydata[,i]/max(mydata[,i])
 mydata[,1]=mydata[,1]^(1/17)


#Clustering classique avec les k-means.
KMEANS <- kmeans(mydata, nbre_cluster)

plotcluster <-function(Data, Algo,nbre_cluster){

plot(Data[,1:2], col = Algo$cluster)
points(Algo$centers, col = 1:nbre_cluster, pch = 8)
return(0)}

plotclustering <- function(Data, Algo, nbre_cluster){

plot(Data[,1:2], col = Algo$clustering)
points(Algo$medoids, col = 1:nbre_cluster, pch = 8)
return(0)
}
print('plotting KMEANS')
plotcluster(mydata, KMEANS, nbre_cluster)

#mydata <-mydata[1:1000,]
# Hierarchical clustering
#mydist <- dist(mydata)
#HCLUST <- hclust(mydist)
#plot(HCLUST)

# Agglomerative Nesting

#AGNES <- agnes(mydata, diss = FALSE, metric = "euclidean",stand = FALSE)

#print(AGNES)

# Dissimilarity Matrix

#DAISY<-daisy(mydata, metric = c("euclidean", "manhattan", "gower"),stand = FALSE, type = list())

# Divisive analysis clustering
#DIANA<-diana(mydata, diss=FALSE, metric = "euclidean", stand = FALSE)

# Fuzzy Analysis clustering

FANNY <- fanny(mydata, nbre_cluster, diss=FALSE, memb.exp = 1.2,metric = c("euclidean", "manhattan", "SqEuclidean"),stand = FALSE, iniMem.p = NULL, cluster.only = FALSE)

print('plotting FANNY')
plotclustering(mydata, FANNY, nbre_cluster)
# Partionning around Medoids

PAM <-pam(mydata, nbre_cluster, FALSE, metric = "euclidean",medoids = NULL, stand = FALSE, cluster.only = FALSE)

print('plotting PAM')
plotclustering(mydata, PAM, nbre_cluster)
