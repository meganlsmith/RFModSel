#/usr/bin/python2.7

from sys import argv
from subprocess import call
import os
from optparse import OptionParser
from optparse import OptionGroup



"""Set up help menu for when script is run with -h, and set up user options."""
desc=""
parser = OptionParser(description=desc)
group = OptionGroup(parser, "Required Arguments",
                    "")
group.add_option("-p",
                  help="Specify project name (prefix of model files)", action = "store", type = "string", dest = "projname")
group.add_option("-n",
                  help="Specify how many models you will test.  These should be labelled projname_1,...,projname_n, and should be in the working directory", action = "store", type = "string", dest = "nmods")
group.add_option("-O",
                  help="Name of file containing observed SFS", action = "store", type = "string", dest = "observed")
group.add_option("-N",
                  help="Specify how many SFS you want to simulate for each model?", action = "store", type = "string", dest = "nreps")
parser.add_option_group(group)

group = OptionGroup(parser, "Optional Arguments",
                    "")
group.add_option("-T",
                  help="Specify how many trees you want to include in your random forest? DEFAULT = 500 (Must be > 10)", action = "store", type = "string", dest = "trees", default = 500)
group.add_option("-l",
                  help="LDA:  use this flag to exclude lda axes in your Random Forest", action = "store_false", dest = "lda", default =True)
group.add_option("-s",
                  help="Use this flag to skip simulation of SFS (If you've already simulated your SFS previously and want to reconstruct your forest with different parameters or use a different observed dataset", action = "store_true", dest = "skip", default = False),
group.add_option("-f",
                  help="Use this flag to specify a path to fastsimcoal2. DEFAULT = fsc25", action = "store", type = "string", dest = "fsc", default = 'fsc25')

parser.add_option_group(group)

(options, args) = parser.parse_args()





"""Parse the options entered by the user."""
nmods = int(options.nmods)
nreps = int(options.nreps)
projname = options.projname
observed = options.observed
trees = int(options.trees)
lda = str(options.lda)
skip = str(options.skip)

"""Simulate SFS in fastsimcoal2."""
def fsc():
    if skip == 'False':
        for num in range(1,nmods+1):
            model = projname
            model += '_'
            model += str(num)
            est = model+'.est'
            tpl = model+'.tpl'
            fsc = str(options.fsc)
            log = 'fsc_log' + str(num) + '.txt'
            os.system("%s -t %s -e %s -E %d -n 1 -m -u -c 1 -x > %s" % (fsc,tpl,est,nreps,log))
            os.system("cd %s && mv *_MSFS.obs ../" % model)
fsc()

"""Process fastsimcoal2 output to prepare reference table for abcrf package."""
def prepprior():
    if skip == 'False':
        for num in range(1,nmods+1):
            filename = projname
            filename += '_'
            filename += str(num)
            filename += '_MSFS.obs'
            f = open(filename)
            outfile = projname
            outfile += '_'
            outfile += str(num)
            outfile += '_Prior.txt'
            out = open(outfile, 'w')
            model = str(num)
            count = 1
            for line in f:
                if count % 3 == 0:
                    out.write(model)
                    out.write('\t')
                    out.write(line)
                    count += 1
                else:
                    count += 1
            f.close()
            out.close()

prepprior()

"""Combine priors for different models and save to file called 'Full_Prior.txt'."""
def catprior():
    if skip == 'False':
        os.system("cat %s_?_Prior.txt > Full_Prior.txt" % projname)

catprior()

"""Construct a Random Forest from your reference table with a user specified number of trees with or without lda axes included, and choose model for your observed data. This will also estimate the posterior probability of the selected model."""
def RandomForests():
	os.system("Rscript RandomForest_SFS.R -o %s -T %d -l %s > Rout.txt" % (observed,trees,lda))
RandomForests()
