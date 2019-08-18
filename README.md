

# Requirements

Python 3.6 (or higher)  
CzEng 1.7


# Usage

## Web application

All relevant code for the web application can be found in the `website` directory.
To setup the web application in a new location, you will need to:
- put all the files in the `website` directory in the directory where you want to host the application
- generate the models that you want to use and place them in the `server/data` folder
- place the trimmed lexicon files in `server/data/lexicons` if they were generated
- create a virtual environment in the `server/venv` folder and install the gensim package (see below for more detail)
- configure the application by setting up the correct generators for each model in `server/codenames/generators_config.py` and adding servers to run the generators in `server/codenames/config.py`

To start the application, simply run:
```shell
> cd server
> python3 start_servers.py
```

To stop the application, run:
```shell
> cd server
> python3 stop_servers.py
```

### Create virtual environment and install gensim

Windows
```shell
> cd server
> python3 -m venv venv
> venv\Scripts\python.exe -m pip install gensim
```

Linux
```shell
> cd server
> python3 -m venv venv
> venv/bin/python.exe -m pip install gensim
```

## CzEng

CzEng deserves a special mention, because it is used extensively in the creation of the models.
In order to create any of the models, you will need to download [CzEng 1.6](https://ufal.mff.cuni.cz/czeng) and place the unzipped tar files in the `models/data/czeng` directory. (nested directories are no problem for the application)
The conversion to CzEng 1.7 is handled by the application itself in `czeng_faulty_sections.py` and does not need to be performed manually.

## Lexicons

The naming scheme of the lexicons is strict: `original_<language code>.txt`. For example, the English lexicon would be stored in `original_en.txt`.
The format of the lexicon is one entry per line, case insensitive. Casing is normalized when handling lexicons (all lowercase), so casing in lexicon files does not matter.
Some of the models will produce a trimmed lexicon if the lexicon contains words that the model does not know. If such a shortened lexicon is produced, that lexicon should be used in the web application instead of the full version of the lexicon to avoid errors, because the generated model is only compatible with the trimmed lexicon.

## Word embedding models

FastText word embeddings can be downloaded from: https://github.com/facebookresearch/fastText/blob/master/docs/pretrained-vectors.md

We apply several filters to the word embeddings file, only including words which are:
- alphabetic
- occur as a lemma in the CzEng corpus
- occur >=50 times in the CzEng corpus

Additionally, we assume that the embeddings file is ordered by word frequency, so we reduce the search space by taking the top-n word embeddings from the file that pass the above filters. Reducing the search space not only prevents the model from using niche words that a player might not know (in other words: useless hints), but also helps reduce server load when running the model.

For practical purposes `filter.py` also requires the lexicon that you want to use. A trimmed lexicon is produced in cases where there are words in the lexicon that do not occur in the word embeddings file. This trimmed lexicon can then be used in the actual application to avoid situations where the model cannot generate a hint for a word because it has never seen it before.

To apply the filtering to an existing word embeddings file, run:
```shell
> cd models
> python3 word_embeddings/filter.py <word embeddings file> <new word embeddings file> <language> <top n>
```

Example:
```shell
> cd models
> python3 word_embeddings/filter.py data/wiki.en/wiki.en.vec data/wiki.en/wiki-czeng-filtered-top-10000.en.vec en 10000
```

## Collocation models

...


# Future direction

## Features

The following is a list of features that could be worthwhile to implement in the future:

- Two player version (requires robust networking code and some structural changes to avoid race conditions)
- New models
- Support for multi-word expressions (e.g. scuba diver, ice cream, etc.)
- Achievements (to increase player engagement)
- Leaderboard based on a player's last 10-20 games (only worthwhile if we can increase the average winrate, i.e. if we have better models)

## Code quality

The following is a list of possible improvements to the code quality of the project:

- The official language code for Czech is 'cs' instead of 'cz'.
- Better mechanism for handling models for different languages
