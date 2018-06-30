# YAIA Email Summarizer - The ML script

### The data

#### The BC3 Email Corpus

The corpus consists of 40 email threads (3222 sentences) from the W3C corpus. 
Each thread has been annotated by three different annotators. 
The annotation consists of the following:

- Extractive Summaries
- Abstractive Summaries with linked sentences
- Sentences labeled with:
   - Speech Acts: Propose, Request, Commit, Meeting
   - Meta Sentences
   - Subjectivity
 

**Download the corpus**

https://www.cs.ubc.ca/cs-research/lci/research-groups/natural-language-processing/bc3/download.html

_Credits: Ulrich J., Murray G., Carenini G., A Publicly Available Annotated
corpus for Supervised Email Summarization AAAI08 EMAIL Workshop, Chicago, USA, 2008._

### Set the environment

- Once downloaded the data, extract the BC3 corpus inside ml/Resources/bc3/
directory.

#### The Jupyter Notebook

To be able to run the data_processing file, you need to install Jupyter Notebook
or Jupyter Lab

- http://jupyter.org/install
- https://github.com/jupyterlab/jupyterlab

#### The data processing and ML

Once the Jupyter server is running, open the the browser and go to 
http://localhost:8888/notebooks/ml/data_processing.ipynb






