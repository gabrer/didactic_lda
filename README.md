# Didactic implementation of LDA

This is a didactic implementation of LDA (Latent Dirichlet Allocation) which aims to provide an explicative and unoptimized code (as mush as possible).
It exploits the collapsed Gibbs sampling to infer the latent variables.


## Getting Started

I reccomend to execute this code in a Python 2.7 virtual environment, which can be set up using the provided "requirements.txt" file.



### Python environment


1. Create your environment "venv": 
```
virtualenv venv
```

2. Activate it:
```
source venv/bin/activate
```


3. Install the required libraries:
```
pip install -r requirements.txt
```

4. Run the didactic LDA:
```
python my_lda.py
```

and enjoy LDA!



## Built With

* [Latent Dirichlet Allocation](http://www.jmlr.org/papers/volume3/blei03a/blei03a.pdf) - The seminal paper about LDA (based on Varionatl Inference)
* [Gibbs sampling for LDA](http://psiexp.ss.uci.edu/research/papers/sciencetopics.pdf) - LDA based on Gibbs sampling


## Authors

* **Gabriele Pergola** - *PhD student*

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details
