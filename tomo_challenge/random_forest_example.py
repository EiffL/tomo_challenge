"""
This is an example tomographic bin generator
using a random forest.

Feel free to use any part of it in your own efforts.
"""
import time
import sys
import code

import numpy as np
from sklearn.ensemble import RandomForestClassifier

from . import metrics
from .data import load_magnitudes_and_colors, load_redshift

def build_random_forest(filename, bands, n_bin, **kwargs):
    # Load the training data
    training_data = load_magnitudes_and_colors(filename, bands)

    # Get the truth information
    z = load_redshift(filename)

    # Now put the training data into redshift bins.
    # Use zero so that the one object with minimum
    # z in the whole survey will be in the lowest bin
    training_bin = np.zeros(z.size)

    # Find the edges that split the redshifts into n_z bins of
    # equal number counts in each
    p = np.linspace(0, 100, n_bin + 1)
    z_edges = np.percentile(z, p)

    # Now find all the objects in each of these bins
    for i in range(n_bin):
        z_low = z_edges[i]
        z_high = z_edges[i + 1]
        training_bin[(z > z_low) & (z <= z_high)] = i

    # for speed, cut down to 5% of original size
    cut = np.random.uniform(0, 1, z.size) < 0.05
    training_bin = training_bin[cut]
    training_data = training_data[cut]

    # Can be replaced with any classifier
    classifier = RandomForestClassifier(**kwargs)

    t0 = time.perf_counter()
    # Lots of data, so this will take some time
    classifier.fit(training_data, training_bin)
    duration = time.perf_counter() - t0

    return classifier, z_edges


def apply_random_forest(classifier, filename, bands):
    data = load_magnitudes_and_colors(filename, bands)
    tomo_bin = classifier.predict(data)
    return tomo_bin

def main(bands, n_bin):
    # Assume data in standard locations relative to current directory
    training_file = f'{bands}/training.hdf5'
    validation_file = f'{bands}/validation.hdf5'
    output_file = f'{bands}_{n_bin}.png'
    classifier, z_edges = build_random_forest(training_file, bands, n_bin,
                                     max_depth=10,
                                     max_features=None,
                                     n_estimators=20,
    )

    tomo_bin = apply_random_forest(classifier, validation_file, bands)
    # Get a score
    z = load_redshift(validation_file)
    scores = metrics.compute_scores(tomo_bin, z)

    metrics.plot_distributions(z, tomo_bin, output_file, z_edges)


    # Return. Command line invovation also prints out
    return scores




if __name__ == '__main__':
    # Command line arguments
    try:
        bands = sys.argv[1]
        n_bin_max = int(sys.argv[2])
        assert bands in ['riz', 'griz']
    except:
        sys.stderr.write("Script takes two arguments, 'riz'/'griz' and n_bin_max\n")
        sys.exit(1)

    # Run main code
    for n_bin in range(1, n_bin_max+1):
        scores = main(bands, n_bin)
        print(f"Scores for {n_bin} bin(s) : ")
        for k,v in scores.items():
            print ("      %s : %4.1f"%(k,v))
            
