# -*- coding: utf-8 -*-

import pytest
from chanjo.bam import BamFile


def test_bam():
  bam = BamFile('tests/fixtures/alignment.bam')

  # These are the 39 read depths matching base pairs in 'align.bam'
  reference = [2., 4., 5., 5., 5., 5., 6., 7., 7., 7., 7., 7., 7., 7., 7., 7.,
               7., 7., 7., 7., 7., 7., 7., 8., 8., 7., 7., 7., 7., 7., 7., 7.,
               6., 4., 4., 3., 3., 2., 2.]

  # Read BAM from position [1,10]
  depths = bam('chr1', 1, 10)

  # Make assertions: we expect the read depths from 1st to 10th position
  # to be included.
  answer = reference[0:10]
  # Compare the list version of the returned ``numpy.array`` to 'answer'
  assert list(depths) == answer

  # Test also an interval that extends beyond the available reads
  depths = bam('chr1', 35, 45)
  assert list(depths) == reference[34:] + [0, 0, 0, 0, 0, 0]

  # Test interval completely outside the available reads
  depths = bam('chr1', 50, 59)
  assert list(depths) == [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

  # Test reading a single base
  depths = bam('chr1', 7, 7)
  assert list(depths) == [6.]

  # This is not the current implementation but should perhaps be?
  # How else can you tell this case from returning only zeros.
  # Test submitting a false chromosome Id
  with pytest.raises(ValueError):
    _ = bam('crh1', 10, 20)

  # Test submitting 0-based positions (the 0th doesn't exist)
  with pytest.raises(ValueError):
    _ = bam('chr1', 0, 9)
