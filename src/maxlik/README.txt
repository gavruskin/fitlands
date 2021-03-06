I've added some Rscript files to the fitlands repository which I am
offering as an alternative for computing the probability of rank
orders based on comparison results.  It is a maximum likelihood
approach, where I assume the elements in the set x_0,x_1,...x_n have
independent Gaussian distributed fitness values with means
0,mu_1,mu_2,...,mu_n and standard deviation 1.  Note that we can
assume the mean of one of the elements is 0 and the standard deviation
1 since we are only interested in rank order, hence scale and position
don't matter.  I assume that we have an empirical data set showing the
results of various fitness comparison tests: The ijth entry is the
number of results which showed element i with greater fitness than
element j.  Using the optimization function 'nlm' in R, I find the
values of mu_1,mu_2,...m_n which maximize the log likelihood of
obtaining the empirical results.  

Looking at the files in the repo, feed the file 'data' as standard
input into 'maxlik.R'.  maxlik.R should have as commandline arguments
a reasonable guess of the values of mu_1,mu_2,...,mu_n to use as the
starting point for the optimization procedure.  (Getting at least the
order right will help to prevent R from complaining about infinite
values being taken during the optimization.) 

The first line of output of maxlik.R will be the likelihood maximizing
0,mu_1,mu_2,...,mu_n.  The following lines will consist of the results
of sampling from the distribution thus derived, showing the rank
orders which occurred as well as the proportion of samples which had
that rank order.  

I've also included maxlikTest.R which can be thought of as the
"inverse" of maxlik.R.  It takes as standard input a file containing
the parameters mu_0,mu_1,mu_2,...,mu_n and delivers as output a matrix
consisting of the results of comparison tests.  You can feed this back
into maxlik.R and see how well the maximum likelihood mus compare to
those you fed into maxlikTest.R.
