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

In this branch (`3rd-solution`), the third solution is updated to use our dataset. In this process, we introduced some
potential breaking changes. This solution training procedure is suited for two tasks: landmark prediction and whale
identification. We changed it satisfy to our needs for the identification task only. To do so, we have made the
following changes:
- we created more [configuration files](./solutions/3rd-place/configs).
- we changed the training log strategy. We used a similar approach as the first and second solution, which consists in
writing the information directly to a text file, instead of using [TensorBoardX][11].
- we also included the _precision@k_ (_top@k_) metric to the log.
- we created a [bash script](./solutions/3rd-place/inference_tests.sh) to automatically run all inference steps for
the tests.
- we added landmarks and a bounding box for a image (`076e1f97f.jpg`) which did not have it available in the 5th split.

The other branches have the following changes:
- `main`: Original solutions;
- `{1st,2nd}-solution`: Updated solutions using our datasets;
- `gcn`: Updated `2nd-solution` branch code using Global Contrast Normalization (GCN);
- `lcn`: Same as above but using Local Contrast Normalization (LCN);
- `no-cn`: Same as above but using no Contrast Normalization;
- `swa`: Same as above but using [Stochastic Weight Averaging (SWA)][10];


## Acknowledgments

This project was supported by [São Paulo Research Foundation - FAPESP][6] under grant #2019/11386-3.
We also thank the [Institute of Computing/Unicamp][8] for the technical support given during the project execution,
which includes the configuration and maintenance of the machine used in our experiments, and acquired with FAPESP's
support under grant #2018/00031-7. Moreover, we also thank [SAE/Unicamp][7] for the support given.

Opinions, hypothesis and conclusions, or recommendations made in this material are responsibility of the authors,
and not necessarily reflect FAPESP's point of view.

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
[11]: https://tensorboardx.readthedocs.io/en/latest/tensorboard.html