**Importante note: The source code will be available from 26th June, 2017**

## BNOC: A benchmarking tool to generate bipartite network models with overlapping communities

**About**

BNOC is a tool for benchmarking weighted bipartite network with overlapping community structures. BNOC can create network  with balanced or unbalanced overlapping communities, heterogeneous community sizes, different intra- and inter-community edge densities, and with varying average degrees and clustering coefficients. The set of parameters, described in  the table below, controls the bipartite network features.

**Usage**

	python bnoc.py [options]

| Option             | Domain                    | Default  | Description                                                   |
| ------------------ | ------------------------- | -------- | ------------------------------------------------------------- |
| -dir --directory   | string [DIR]              | '.'      | directory of output file                                      |
| -out --output      | string [FILE]             | 'out'    | filename                                                      |
| -cnf --conf        | string [FILE]             | None     | None                                                          |
| -v, --vertices     | [1, V] Integer interval   | [10, 10] | number of vertices for each layer (array of two values)       |
| -c, --communities  | [1, V] Integer interval   | 2        | number of communities                                         |
| -p1, --probability | (0, V] Real interval      | None     | probability of vertices in each community for layer 1         |
| -p2, --probability | (0, V] Real interval      | None     | probability of vertices in each community for layer 2         |
| -x, --x            | [0, V_1] Integer interval | 0        | number of vertices from V1 that participate of overlapin      |
| -y, --y            | [0, V_2] Integer interval | 0        | number of vertices from V2 that participate of overlapin      |
| -z, --z            | [0, c] Integer interval   | 1        | number of vertices of overlapping communities                 |
| -d, --dispersion   | (0, 1] Real interval      | 0.1      | dispersion of gamma mixing distribution                       |
| -m, --mu           | Real                      | 0.9      | dispersion or range of wieght values                          |
| -n, --noise        | (0, 1] Real interval      | 0.0      | noise                                                         |
| -b, --balanced     | boolean                   | False    | boolean balancing flag that suppresses -p parameter           |
| -u, --unweighted   | boolean                   | False    | unweighted networks                                           |
| -no, --normalize   | boolean                   | False    | scale input vectors individually to unit norm (vector length) |
| -hd, --hard        | boolean                   | False    | hard noise                                                    |
| --save_ncol        | boolean                   | False    | save ncol format                                              |
| --save_gmal        | boolean                   | False    | save gml format                                               |
| --save_arff        | boolean                   | False    | save arff format                                              |
| --show_timing      | boolean                   | False    | show timing                                                   |
| --save_timing_json | boolean                   | False    | save timing in json                                           |
| --save_timing_csv  | boolean                   | False    | save timing in csv                                            |
| --unique_key       | boolean                   | False    | output date and time as unique_key                            |

**Examples**

	$ python bnoc.py -v 100 50 -dir output -out network -m 0.9 -c 3 -d 0.6 -n 0.2
	$ python plot-bipartite-graph.py -in output/network.ncol -dir output -out network -m output/network -v 100 50 --save_pdf --bbox 1000 300

![](output/network.png)

	$ python plot-bipartite-matrix.py -in output/network.ncol -dir output -out matrix -v 100 50 --save_png --bbox 500 200

![](output/matrix.png)

You can use a config file (.json) to specify the parameters, for instance:

	$ python bnoc.py -cnf input/network.json
	$ python plot-bipartite-graph.py -cnf input/plot-bipartite-graph.json
	$ python plot-bipartite-matrix.py -cnf input/plot-bipartite-matrix.json

**Anaconda**
conda create --name py372 python=3.7.2
conda activate py372
conda install -c conda-forge python-igraph
conda install -c anaconda pyyaml
conda install -c anaconda scipy
conda install -c anaconda networkx
conda install PIL
conda install -c conda-forge weave
conda install -c conda-forge pypdf2

**References**

> [1] Valejo, A.; Goes, F.; Oliveira, M. C. F.; Alneu, A. A.: An open-source benchmarking tool for overlapping community detection in bipartite network. (2018)

~~~~~{.bib}
@article{Alan2016,
    author={Alan Valejo and Fabiana Goes and Maria Cristina Ferreira de Oliveira and Alneu de Andrade Lopes},
    title={An open-source benchmarking tool for overlapping community detection in bipartite network.},
    year={2018}
}
~~~~~
