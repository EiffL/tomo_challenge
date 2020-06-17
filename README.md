# The Idealised Tomography Challenge

In this challenge you are asked to group galaxies into tomographic bins using only the quantities we generate using the metacalibration method.  These quantities are the only ones for which we can compute a shear bias correction associcated with the division.

We provide training and validation sets of data, and once everyone has added methods, we

This test is highly idealised: we have a huge complete training sample, simple noise models, no outliers, and no variation in depth or any other observing conditions.

Galaxy magnitudes are generated by adding noise to the CosmoDC2 data and applying a preliminary selection cut (SNR>10, metacal flag=0, metacal size > PSF size / 2).

All entrants will be on the author list for the upcoming TXPipe-CosmoDC2 paper, which these results will go into.  The winner will additionally receive glory.


## Installing requirements

In general you can install requirements with `pip install -r requirements.txt`

On NERSC it's easiest to use shifter (I've had problems with CCL there):

```
shifter --image=joezuntz/txpipe-tomo bash
```

This will put you in a shell with all requirements.


## Getting training data

Run `python -m tomo_challenge.data` in this directory to download the full set of challenge data, about 4.5GB.  You can also get the individual files from here if you prefer:  https://portal.nersc.gov/project/lsst/txpipe/tomo_challenge_data/


## Metric

The current metric is the S/N on the spectra generated with the method:
```
score^2 = sqrt(mu^T . C^{-1} . mu) - baseline
```
where mu is the theory spectrum and C the Gaussian covariance.

We plan to add second metric based on Fisher matrices shortly.


## Entering the contest.

You can enter the contest by pull request.  Add a python file with your method in it.


## Example Method

In `tomo_challenge/classifiers/random_forest.py` you can find an example of using a scikit-learn classified with a simple galaxy split to assign objects.  Run it by doing, e.g.:

```bash
$ python bin/challenge.py example/example.yaml
```

This will compute the metric and make a plot for the random forest method using between 1 and 5 bins.

You are welcome to adapt any part of that code in your methods.


The example random forest implementation gets the following scores using the spectrum S/N metric.  For griz:

```
# nbin  score
1  0.0
2  28.2
3  35.4
4  37.9
5  39.7
6  40.3
7  40.5
8  41.1
9  41.5
10  41.8
```

and for riz:

```
# nbin  score
1  0.1
2  21.6
3  26.4
4  28.5
5  29.7
6  30.1
7  30.1
8  29.4
9  29.1
10  30.1
```


## FAQ

#### How do I enter?

Create a pull request that adds a python file to the `tomo_challenge/classifiers` directory containing a class with `train` and `apply` methods, following the random forest example as a template.

#### Can I use a different programming language?

Only if it can be easily called from python.


#### What are the metrics?

- The total S/N (including covariance) of all the power spectra of weak lensing made using your bins
- The inverse area of the w0-wa Fisher matrix (due to [a technical problem](https://github.com/LSSTDESC/CCL/issues/779) the current metric is the sigma8-omega_c Fisher matrix)


#### Why is this needed?

The metacal method can correct galaxy shear biases associated with putting galaxies into bins (which arise because noise on magnitudes correlates with noise on shape), but only if the selection is done with quantities measured jointly with the shear.

This only affects shear catalogs - for lens bins we can do what we like.

#### What is the input data?

[CosmoDC2](https://arxiv.org/pdf/1907.06530.pdf) galaxies with mock noise added.

#### How many bins should I use, and what are the target distributions?

As many as you like - it's likely that more bins will add to your score as long as they're well-separated in redshift, so you probably want to push the number upwards.  You can experiment with what edges give you best metrics; historically most approaches have tried to divide into bins with roughly equal numbers, so that may be a good place to start.

#### What do I get out of this?

You can be an author on the paper we write if you submit a working method.  

#### Can non-DESC people enter?

Yes.  It's based on [public simulated data](https://portal.nersc.gov/project/lsst/cosmoDC2/).  If you're not in DESC you may have to fill in an [external collaborator form](https://docs.google.com/document/d/1kfDIi6REFupUQTAz_TfVbLTd6kcsBJ0x91-IYj73FK4/edit#).

#### How realistic is this?

This is the easiest possible challenge - the training set is large and drawn from the same population as the test data, and the data selection is relatively simple.

#### Do I have to use machine learning methods?

No - we call the methods `train` and `apply`, but that's just terminology, you can train however you like.

#### Can I use a simpler metric?

Yes, you can train however you like, including with your own metrics.  The final score will be on a suite of metrics including the two here.  We reserve the right to add more metrics to better understand things.

#### What does the winner get?

Recognition.
