# NZ Strong Motion

The **original** NZ strong motion database can be downloaded from
this [page](https://www.geonet.org.nz/data/supplementary/nzsmdb).

The ground motions are **processed** and **compiled** into separate files. Please download the archive first before
using any recordings. Users may need [7-Zip](https://www.7-zip.org/download.html) to unpack the archive.

|     type     |              link               |
|:------------:|:-------------------------------:|
| acceleration | [download](NZStrongMotion-A.7z) |
|   velocity   | [download](NZStrongMotion-V.7z) |
| displacement | [download](NZStrongMotion-D.7z) |

The archive contains all 756 displacement, velocity and acceleration histories along three directions. That totals 6804
records.

The script used to process the original data is available [here](ProcessNZSM.py).

## Syntax

```
amplitude NZStrongMotion (1) (2)
# (1) int, unique amplitude tag
# (2) string, record name
```

It must be noted that the amplitudes are normalized so that the maximum absolute magnitude is **unity**. Hence, to
achieve a target PGA/PGV/PGD, it shall be assigned to the magnitude of the applied load.

## Usage

For example, to load the accelerogram `20110221_235142_CSHS_N76W_A`, which is one of the 2011 Christchurch earthquake
recordings, user shall first extract the file `20110221_235142_CSHS_N76W_A` from `NZStrongMotion.7z` and place it where
the program can locate, for example, the current working folder.

To define such an amplitude, one can use

```
amplitude NZStrongMotion 1 20110221_235142_CSHS_N76W_A
```

## Explanation of File Format

The format of original file can be seen [here](https://www.geonet.org.nz/data/supplementary/strong_motion_file_formats).

The processed archive first extract accelerogram name from the file, then read how many acceleration values shall be
read and the interval between two records, then read all values and scale them by multiplying each by $$1000$$ and store
them into an integer array. The array has the following layout.

| index |         value ($$\times1000$$)         |
|:-----:|:--------------------------------------:|
|   0   | time interval of the record in seconds |
|   1   |     absolute maximum record value      |
|   2   |       value at first time point        |
|   3   |       value at second time point       |
|   4   |       value at third time point        |
|   5   |                  ...                   |