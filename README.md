# Humpback Whale Identification by Its Tail

This repository houses the files and codes used by [Henrique Simões][1] and [João Meidanis][2] in the research project
entitled "_Humpback Whale Identification by Its Tails_".

## Abstract

Humpback whales (_Megaptera novaeangliae_) were predominantly explored by the fishing industry between the 1860s and the
late 1900s. After the humpback whale fishing was banned, and the species declared endangered, the population started to
recover. However, the data of this recovery were still limited. In order to track the population dynamics, researchers
use the whale’s fluke shape and markings to identify the individuals. But this process had to be done manually.
To address this issue, the Kaggle platform hosted a competition from Nov. 2018 to Feb. 2019 where an automatic model should
identify the whales by their tails. In our research project, we aimed at analyzing and reproducing the competition top
solutions’ results, as well as at testing improvements that could be incorporated to the best solution.

## Repository Structure

### Directories

The files are distributed across several folders which are described next.

- [data-analysis](./data-analysis): Processed information about the data used by competitors to build their algorithms.
- [solutions](./solutions): Solutions developed by the analysed candidates;
- [util](./util): Executables created by us to handle some tasks;
- [test](./test): Corrected data (and intermediate files);

### Branches

This repository contains several branches, which correspond to different changes in the source code.

In this branch (`gcn`), the second solution code using our dataset is updated to use Global Contrast
Normalization (GCN). For a description of this strategy, see Goodfellow _et al._'s [Deep Learning book][11],
section 12.2.1.1. To do so, we added a [contrast module](./solutions/2nd-place/process/contrast.py) which allows the
application of the global and local normalization, as well as the author's original transformation, to a batch of
images.

The other branches have the following changes:
- `main`: Original solutions;
- `{1st,2nd,3rd}-solution`: Updated solutions using our datasets;
- `lcn`: Updated `2nd-solution` branch code using Local Contrast Normalization (LCN);
- `no-cn`: Same as above but using no Contrast Normalization;
- `swa`: Same as above but using [Stochastic Weight Averaging (SWA)][10];

## Acknowledgments

This project was supported by [São Paulo Research Foundation - FAPESP][6] under grant #2019/11386-3.
We also thank the [Institute of Computing/Unicamp][8] for the technical support given during the project execution,
which includes the configuration and maintenance of the machine used in our experiments, and acquired with FAPESP's
support under grant #2018/00031-7. Moreover, we also thank [SAE/Unicamp][7] for the support given.

Opinions, hypothesis and conclusions, or recommendations made in this material are responsibility of the authors,
and do not necessarily reflect FAPESP's point of view.

## License

The source codes except those in the [solutions folder](./solutions) are licenced under the
[BSD 3-Clause License](./LICENSE), and the data resources of this project except those in the
[solutions folder](./solutions) are licensed under the [CC0 1.0 Universal (CC0 1.0) Public Domain Dedication][3].

[1]: http://lattes.cnpq.br/2364440352119569
[2]: http://lattes.cnpq.br/1313385414995585

[3]: https://creativecommons.org/publicdomain/zero/1.0/

[5]: https://www.kaggle.com/c/humpback-whale-identification
[6]: https://fapesp.br/en/
[7]: https://www.sae.unicamp.br
[8]: https://ic.unicamp.br/en/

[10]: https://arxiv.org/abs/1803.05407
[11]: https://www.deeplearningbook.org
