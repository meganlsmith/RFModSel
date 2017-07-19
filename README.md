# RFModSel
Demographic Model Selection using Random Forests and the Site Frequency Spectrum

Introduction:
SFS_ABC.py will generate site frequency spectra under user-defined models and will use Random Forests to select the best model for an empirical dataset. 


Requirements:
SFS_ABC.py uses fastsimcoal2 (Excoffier et al. 2013) and R version 3.3.0 (R Core Team 2016).
The user will want to download these two programs.  The user may specify a path to call 
fastsimcoal2. R should be installed such that Rscript can be run from the command line. 
This script is written to run on Mac OS X. 


Input: 
As input, SFS_ABC.py requires two things: 
1.  The user must provide .tpl and .est files to define the models.  The format for these
    files is explained in the fastsimcoal2 documentation. These should be named 
    'PROJNAME_Model#', where PROJNAME is a user-specified string, and the Model#s
    are sequential integers from 1 to n. 
2.  The user must provide an observed multidimensional site frequency spectrum.  This 
    file should be one line, with the bins of the SFS in the same arrangement as specified 
    in the fastsimcoal2 documentation.
These files should be present in the working directory with the SFS_ABC.py script and
the RandomForest_SFS.R script.  

Usage: 
Unzip the SFS_ABC_RF folder.  Both the SFS_ABC.py script and the RandomForest_SFS.R scripts
are present in this directory.  Place your .tpl and .est files, along with your observed SFS
file in this directory. 

example usage: 
python SFS_ABC.py -p Example -n 4 -O Observed.txt -N 10000

For information on required and optional arguments, run:
python SFS_ABC.py -h

Output: 
The script will create a directory for each of the specified models, which will contain
information on the parameters used to generate each SFS.  The script will also create a 
reference table ('Full_Prior.txt').  The 'Rout.txt' file generated will have information on 
the best model, the posterior probability of that model, and the prior error rates.  
Additionally, two pdfs will be generated.  'Errors.pdf' contains a plot of the error rate 
as a function of the number of trees in the forest.  'RF.pdf' includes a plot of variable
importance and a plot of the first two axes of the LDA.

If you have any questions or comments, please email me at megansmth67@gmail.com.

Please refer to: Smith ML, Ruffley MR, Espíndola AE, Tank DC, Sullivan J, Carstens BC. Demographic model selection using random forests and the site frequency spectrum. Molecular Ecology.

References: 
Excoffier, L., et al. Robust Demographic Inference from Genomic and SNP Data. PLoS 
    Genet. 9, e1003905 (2013).
Marin, Jean-Michel, Pierre Pudlo and Louis Raynal (2016). abcrf: Approximate Bayesian 
    Computation via Random Forests. R package version 1.3. 
    https://CRAN.R-project.org/package=abcrf
R Core Team (2016). R: A language and environment for statistical computing. R Foundation 
    for Statistical Computing, Vienna, Austria. URL https://www.R-project.org/.
