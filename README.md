```
Warning
-------
The original implementation (i.e. paper version [1]) is deprecated.
This software is a new version, more robust and fast.
There may be divergences between this version and the original algorithm.
If you looking for the original version used in the paper don't hesitate to contact the authors.
```

### BNOC: A benchmarking tool to generate bipartite, k-partite and heterogeneous network models with overlapping communities

**About**

BNOC is a tool for synthesizing bipartite, k-partite and heterogeneous network models with varied features representative of properties from real networks. Multiple input parameters can be manipulated to create networks of varying sizes and with distinct community patterns in terms of number, size, balance, edge distribution intra- and inter-communities, degree of overlapping and cohesion, and degree of noise in the connection patterns.

> To help you visualize networks you can use the [PyNetViewer](https://github.com/alanvalejo/pynetviewer) software.

**Usage**

	$ python bnoc.py [options]

| Option             | Domain                       | Default                  | Description                                                   |
| ------------------ | ---------------------------- | ------------------------ | ------------------------------------------------------------- |
| -dir --directory   | str [DIR]                    | '.'                      | directory of output file                                      |
| -out --output      | str [FILE]                   | 'out'                    | filename                                                      |
| -cnf --conf        | str [FILE]                   | None                     | Input parameters in .json format                              |
| -v, --vertices     | int array                    | [10, 10, 10]             | number of vertices for each layer                             |
| -d, --dispersion   | float array                  | [0.3, 0.3, 0.3]          | dispersion of gamma mixing distribution for each layer        |
| -m, --mu           | float array                  | [0.3, 0.3, 0.3]          | dispersion or range of wieght values for each layer           |
| -c, --communities  | int array                    | [2, 2, 2]                | number of communities                                         |
| -x, --x            | int array                    | [1, 1, 1]                | number of vertices from V1 that participate of overlaping      |
| -z, --z            | int array                    | [2, 2, 2]                | number of vertices of overlapping communities                 |
| -p, --p            | int array of array           | [[0.5, 0.5], [0.5, 0.5]] | probability of vertices in each community for each layer      |
| -e, --scheme       | int array of array           | [[0, 1], [1,2]]          | connections type                                              |
| -n, --noise        | float array                  | [0.1, 0.1]               | noise for each connections type                               |
| -b, --balanced     | boolean                      | False                    | boolean balancing flag that suppresses -p parameter           |
| -u, --unweighted   | boolean                      | False                    | unweighted networks                                           |
| -no, --normalize   | boolean                      | False                    | scale input vectors individually to unit norm (vector length) |
| -hd, --hard        | boolean                      | False                    | hard noise                                                    |
| --save_npy         | boolean                      | False                    | save numpy object                                             |
| --save_ncol        | boolean                      | False                    | save ncol format                                              |
| --save_gml         | boolean                      | False                    | save gml format                                               |
| --save_arff        | boolean                      | False                    | save arff format                                              |
| --save_cover       | boolean                      | False                    | save communities in cover form                                |
| --save_membership  | boolean                      | False                    | save communities in a membership format                       |
| --save_type        | boolean                      | False                    | save vertex type                                              |
| --save_overlap     | boolean                      | False                    | save save overlap vertices                                    |
| --show_timing      | boolean                      | False                    | show timing                                                   |
| --save_timing_json | boolean                      | False                    | save timing in json                                           |
| --save_timing_csv  | boolean                      | False                    | save timing in csv                                            |
| --unique_key       | boolean                      | False                    | output date and time as unique_key                            |
| -o --output_objects| boolean                      | False                    | return python objects dictionary and don't write files        |

Parameters `-d`, `-m`, `-c`, `-x`, `-y` and `-z` are arrays of size L, where L is the number of layers.
Parameter `p` is an array of array the probability of vertices in each community for each layer. Parameter `e` define the scheme of the networks, i.e., the connections type.

**Examples**

You can use a config file (.json) to specify the parameters, for instance:

A bipartite network with communities, overlapping and a small level of noise:

	$ python bnoc.py -cnf input/bipartite-1.json

Then, it is possible to plot the network using the PyNetViewer using a bipartite layout. Line widths reflect the
 corresponding edge weights; red squares depict overlapping vertices; and colored circles indicate non-overlapping vertices and their assigned community.
	
    $ python pynetviewer.py -cnf input/bipartite-1_layout_1.json

![](img/bipartite-1-layout-1.png)

The same network with standard layout. Only overlapping vertices are highlighted.

    $ python pynetviewer.py -cnf input/plot_bipartite-1_layout_2.json
	
![](img/bipartite-1-layout-2.png)

A bipartite network with hard level of noise, unbalanced community sizes and no overlapping.

    $ python bnoc.py -cnf input/bipartite-2.json
    $ python pynetviewer.py -cnf input/plot_bipartite-2.json
    
![](img/bipartite-2.png) 
    
A bipartite network with small level of noise, balanced community sizes, no overlapping and many communities.    
    
	$ python bnoc.py -cnf input/bipartite-3.json
	$ python pynetviewer.py -cnf input/plot_bipartite-3.json
	
![](img/bipartite-3.png)	
	
A k-partite network with k=4 and overlapping.

	$ python bnoc.py -cnf input/kpartite.json
	$ python pynetviewer.py -cnf input/plot_kpartite.json
	
![](img/kpartite.png) 	
	
A heterogeneous network with k=3 layers and no overlapping.
	
	$ python bnoc.py -cnf input/heterogeneous.json
	$ python pynetviewer.py -cnf input/plot_heterogeneous.json

![](img/heterogeneous.png)

**Scalability**

BNOC can generate large-scale bipartite networks with tens or even hundreds of thousands of vertices and hundreds of millions of edges in a timely manner. See the article for details about complexity and scalability.

Important, save the output files in text format is slow. It is recommended save the result with numpy `.npy` object, see [numpy.save](https://docs.scipy.org/doc/numpy-1.15.1/reference/generated/numpy.save.html) for details.

For instance, a bipartite network with twenty thousand vertices (use `--show_timing` to print timing values):

    $ python bnoc.py -cnf input/input_bipartite_time_ncol.json

    $        Snippet       Time [m]       Time [s]
    $ Pre-processing            0.0         0.0213
    $     Build BNOC            0.0         2.6187
    $           Save            1.0         34.596

Note, the bottleneck of the Bnoc execution time is to save the output in a text format. To suppress this limitation you can process the network directly in the memory or save a `.npy` object using `--output_npy` or `-onpy` parameter.

    $ python bnoc.py -cnf input/input_bipartite_time_npy.json

    $        Snippet       Time [m]       Time [s]
    $ Pre-processing            0.0         0.0223
    $     Build BNOC            0.0         2.4116
    $           Save            1.0         0.2627

**Install**

> Pip
    
    $ pip install -r requirements.txt

> Or Anaconda env

    $ conda env create -f environment.yml
    $ conda activate bnoc

> Or Anaconda create

    $ conda create --name bnoc python=3.7.2
    $ conda activate bnoc
    $ conda install -c anaconda pyyaml
    $ conda install -c conda-forge pypdf2
    $ conda install -c anaconda scipy

**Testing**

To check that routines are (probably) working properly:

    $ make test

Writing files is tested by exercising the script mode described in the *Usage* section above.
Created objects should probably be better tested, as directions of Bnoc usage.
File I/O can be tested by e.g. appropriatelly replacing the `bnoc.open` function.

**Known Bugs**

- Please contact the author for problems and bug report.

**Contact**

- Alan Valejo
- alanvalejo@gmail.com.br
- www.alanvalejo.com.br
- Postdoctoral research fellow at the University of São Paulo (USP), Brazil

**License and credits**

- Giving credit to the author by citing the papers [1]
- The GNU General Public License v3.0
- This program comes with ABSOLUTELY NO WARRANTY. THE ENTIRE RISK AS TO THE QUALITY AND PERFORMANCE OF THE PROGRAM IS
 WITH YOU.
- Owner or contributors are not liable for any direct, indirect, incidental,
special, exemplary, or consequential damages, (such as loss of data or profits, and others) arising in any way out of
 the use of this software, even if advised of the possibility of such damage.
- This program is free software and distributed in the hope that it will be useful: you can redistribute it and/or
 modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either
  version 3 of the License, or (at your option) any later version. See the GNU General Public License for more
   details. You should have received a copy of the GNU General Public License along with this program. If not, see
    http://www.gnu.org/licenses/.

**To-do list**

- Explicitly seed a global variable or parameter to achieve reproducibility
- Improve usage section

**References**

> [1] Valejo, Alan and Goes, F. and Romanetto, L. M. and Oliveira, Maria C. F. and Lopes, A. A., A benchmarking tool for the generation of bipartite network models with overlapping communities, in Knowledge and information systems, accepted paper, 2019

~~~~~{.bib}
@article{valejo2019benchmarking,
    author = {Valejo, Alan and Goes, F. and Romanetto, L. M. and Oliveira, Maria C. F. and Lopes, A. A.},
    title = {A benchmarking tool for the generation of bipartite network models with overlapping communities},
    journal = {Knowledge and information systems, accepted paper},
    year = {2019}
}
~~~~~

<div class="footer"> &copy; Copyright (C) 2016 Alan Valejo &lt;alanvalejo@gmail.com&gt; All rights reserved.</div>
