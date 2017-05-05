#Rscript
#See if the package optparse is installed. If, not install it.  Then call the library.
if(!require(optparse)){
    install.packages("optparse")
    library(optparse)
}


#Set up the user options and the help menu.# 
option_list = list(
    make_option(c("-o", "--observed"), type="character", default=NULL, 
              help="observed SFS file name", metavar="character"),
    make_option(c("-T", "--trees"), type="integer", default=NULL, 
              help="number of trees in forest", metavar="integer"),
    make_option(c("-l", "--lda"), type="character", default=NULL, 
              help="lda true or false, to include or not to include lda axes in RF", metavar="character")
); 


#Parse the user options.
opt_parser = OptionParser(option_list=option_list);
opt = parse_args(opt_parser);

observed <- opt$observed
trees <- opt$trees
lda <- opt$lda

#Error message of the user fails to enter the name of the observed file.
if (is.null(opt$observed)){
  print_help(opt_parser)
  stop("At least one argument must be supplied (input file)", call.=FALSE)
}

#See if the package abcrf is installed. If, not install it.  Then call the library.
if(!require(abcrf)){
    install.packages("abcrf")
    library(abcrf)
}

#Read in the prior and remove columns with no variation in the prior. Also remove model indices from reference table (to be used in a later step)
Prior <- read.csv('Full_Prior.txt', header = FALSE, sep = "\t")
Prior <- as.data.frame(Prior)
Prior_noMods <- subset(Prior, select = -c(V1))
Prior_Reduced <- Prior_noMods[sapply(Prior_noMods, function(x) length(levels(factor(x)))>1)]

#Set up a list of model indices.
Models <- as.factor(Prior$V1)
summary(Models)

#Read in your observed data and remove columns that were removed from the prior due to a lack of variation.
Observed <- read.csv(observed, header = FALSE, sep = "\t")
names(Observed) <- names(Prior_noMods)
tokeep <- as.vector(names(Prior_Reduced))
Observed_Reduced <- subset(Observed, select = c(tokeep))

#Construct the Random Forest, and plot the variable importance and the first two axes of the LDA, if included.
ABC_SFS <- abcrf(Models, Prior_Reduced, ntree=trees, paral = TRUE, lda = lda)
ABC_SFS
pdf("RF.pdf")
plot(ABC_SFS)
dev.off()

#Calculate out of the bag error using different number of trees, and plot these errors.
pdf("Errors.pdf")
Errors <- err.abcrf(ABC_SFS)
dev.off()
write.table(Errors, file = 'Errors.txt')

#Choose the best model and estimate the posterior probability of the selected model for your observed data.
Prediction <- predict(ABC_SFS,Observed_Reduced, paral = TRUE)
summary(Prediction)
Prediction
