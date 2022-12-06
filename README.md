# PypiReCom 

## Overview

**Want to build a new capability in Python?**
   
   * Probably you would visit repositories like Pypi and see what's available
   ![Today's Flow](https://drive.google.com/uc?export=view&id=1rvj_N2Phs5tqc7KQz0U8qToqMSTfrl2N)   

   
**Welcome to PypiReCom**
   
   Let's make this all easy.


## Table of Content
   * [Problem Statement](#problem-statement)
   * [Use Case](#use-case)
   * [How we got the Idea?](#how-we-got-this-idea)
   * [Architecture](#architecture)
   * [What have we done till now?](#what-have-we-done-till-now)
      * [Data Extraction](#data-extraction)
      * [Data Selection & Graph](#selecting-the-data-and-making-a-dependecy-graph)
   * [Result](#result)

## Problem Statement
This project is to solve a problem that is which package to choose
while doing any kind of development or ML or GML or data  analysis or
anything. The focus is to provide the users with package details of the
best package available in the market that they can use to make 
their work easy.

## Use case
This can be used by developers to search for the package they need.

This can be used to suggest packages to user working on some project.

This can be used in providing the Depedency of any Pip package.

## How we got this Idea?
If we look at the current searching that is availble on the pypi 
website, we can see that the results are not perfect to our need.

![Pypi Website Screenshot](https://drive.google.com/uc?export=view&id=1ixmx_J--8odR8abG2gN3hnhhiJL9WEQH)

So we can see if we are searching for api development we get a lot of results.
We have so many filters like framework, topic, development status, license that a new user will get confuse and it will be very hard for them to select the perfect package for their need.

This is how we came to the idea of making life easy for developers.

***This is where our project helps.***

## Architecture

![Architecture](https://drive.google.com/uc?export=view&id=18H9Z11LaYCS0M-dG7iO3mTEVE-XxS0Rm)
## What have we done till now?

### Data Extraction
We have collected the metadata of the packages from Pypi Public API available.

```http
  GET https://pypi.python.org/pypi/${Package_Name}/json
```

| Parameter | Type     | Description                       |
| :-------- | :------- | :-------------------------------- |
| `Package_Name`      | `string` | **Required**. Name of Package to Fetch |

This is how the Meta-Data is:
```yalm
{
    "info": {
        "author": "PyTorch Team",
        "author_email": "packages@pytorch.org",
        "bugtrack_url": null,
        "classifiers": [
            "Development Status :: 5 - Production/Stable",
            "Intended Audience :: Developers",
            "Intended Audience :: Education",
            "Intended Audience :: Science/Research",
            "License :: OSI Approved :: BSD License",
            "Programming Language :: C++",
            "Programming Language :: Python :: 3",
            "Programming Language :: Python :: 3.10",
            "Programming Language :: Python :: 3.7",
            "Programming Language :: Python :: 3.8",
            "Programming Language :: Python :: 3.9",
            "Topic :: Scientific/Engineering",
            "Topic :: Scientific/Engineering :: Artificial Intelligence",
            "Topic :: Scientific/Engineering :: Mathematics",
            "Topic :: Software Development",
            "Topic :: Software Development :: Libraries",
            "Topic :: Software Development :: Libraries :: Python Modules"
        ],
        "description": "![PyTorch Logo](https://github.com/pytorch/pytorch/blob/master/docs/source/_static/img/pytorch-logo-dark.png)\n\n--------------------------------------------------------------------------------\n\nPyTorch is a Python package that provides two high-level features:\n- Tensor computation (like NumPy) with strong GPU acceleration\n- Deep neural networks built on a tape-based autograd system\n\nYou can reuse your favorite Python packages such as NumPy, SciPy, and Cython to extend PyTorch when needed.\n\nOur trunk health (Continuous Integration signals) can be found at [hud.pytorch.org](https://hud.pytorch.org/ci/pytorch/pytorch/master).\n\n<!-- toc -->\n\n- [More About PyTorch](#more-about-pytorch)\n  - [A GPU-Ready Tensor Library](#a-gpu-ready-tensor-library)\n  - [Dynamic Neural Networks: Tape-Based Autograd](#dynamic-neural-networks-tape-based-autograd)\n  - [Python First](#python-first)\n  - [Imperative Experiences](#imperative-experiences)\n  - [Fast and Lean](#fast-and-lean)\n  - [Extensions Without Pain](#extensions-without-pain)\n- [Installation](#installation)\n  - [Binaries](#binaries)\n    - [NVIDIA Jetson Platforms](#nvidia-jetson-platforms)\n  - [From Source](#from-source)\n    - [Prerequisites](#prerequisites)\n    - [Install Dependencies](#install-dependencies)\n    - [Get the PyTorch Source](#get-the-pytorch-source)\n    - [Install PyTorch](#install-pytorch)\n      - [Adjust Build Options (Optional)](#adjust-build-options-optional)\n  - [Docker Image](#docker-image)\n    - [Using pre-built images](#using-pre-built-images)\n    - [Building the image yourself](#building-the-image-yourself)\n  - [Building the Documentation](#building-the-documentation)\n  - [Previous Versions](#previous-versions)\n- [Getting Started](#getting-started)\n- [Resources](#resources)\n- [Communication](#communication)\n- [Releases and Contributing](#releases-and-contributing)\n- [The Team](#the-team)\n- [License](#license)\n\n<!-- tocstop -->\n\n## More About PyTorch\n\nAt a granular level, PyTorch is a library that consists of the following components:\n\n| Component | Description |\n| ---- | --- |\n| [**torch**](https://pytorch.org/docs/stable/torch.html) | A Tensor library like NumPy, with strong GPU support |\n| [**torch.autograd**](https://pytorch.org/docs/stable/autograd.html) | A tape-based automatic differentiation library that supports all differentiable Tensor operations in torch |\n| [**torch.jit**](https://pytorch.org/docs/stable/jit.html) | A compilation stack (TorchScript) to create serializable and optimizable models from PyTorch code  |\n| [**torch.nn**](https://pytorch.org/docs/stable/nn.html) | A neural networks library deeply integrated with autograd designed for maximum flexibility |\n| [**torch.multiprocessing**](https://pytorch.org/docs/stable/multiprocessing.html) | Python multiprocessing, but with magical memory sharing of torch Tensors across processes. Useful for data loading and Hogwild training |\n| [**torch.utils**](https://pytorch.org/docs/stable/data.html) | DataLoader and other utility functions for convenience |\n\nUsually, PyTorch is used either as:\n\n- A replacement for NumPy to use the power of GPUs.\n- A deep learning research platform that provides maximum flexibility and speed.\n\nElaborating Further:\n\n### A GPU-Ready Tensor Library\n\nIf you use NumPy, then you have used Tensors (a.k.a. ndarray).\n\n![Tensor illustration](./docs/source/_static/img/tensor_illustration.png)\n\nPyTorch provides Tensors that can live either on the CPU or the GPU and accelerates the\ncomputation by a huge amount.\n\nWe provide a wide variety of tensor routines to accelerate and fit your scientific computation needs\nsuch as slicing, indexing, mathematical operations, linear algebra, reductions.\nAnd they are fast!\n\n### Dynamic Neural Networks: Tape-Based Autograd\n\nPyTorch has a unique way of building neural networks: using and replaying a tape recorder.\n\nMost frameworks such as TensorFlow, Theano, Caffe, and CNTK have a static view of the world.\nOne has to build a neural network and reuse the same structure again and again.\nChanging the way the network behaves means that one has to start from scratch.\n\nWith PyTorch, we use a technique called reverse-mode auto-differentiation, which allows you to\nchange the way your network behaves arbitrarily with zero lag or overhead. Our inspiration comes\nfrom several research papers on this topic, as well as current and past work such as\n[torch-autograd](https://github.com/twitter/torch-autograd),\n[autograd](https://github.com/HIPS/autograd),\n[Chainer](https://chainer.org), etc.\n\nWhile this technique is not unique to PyTorch, it's one of the fastest implementations of it to date.\nYou get the best of speed and flexibility for your crazy research.\n\n![Dynamic graph](https://github.com/pytorch/pytorch/blob/master/docs/source/_static/img/dynamic_graph.gif)\n\n### Python First\n\nPyTorch is not a Python binding into a monolithic C++ framework.\nIt is built to be deeply integrated into Python.\nYou can use it naturally like you would use [NumPy](https://www.numpy.org/) / [SciPy](https://www.scipy.org/) / [scikit-learn](https://scikit-learn.org) etc.\nYou can write your new neural network layers in Python itself, using your favorite libraries\nand use packages such as [Cython](https://cython.org/) and [Numba](http://numba.pydata.org/).\nOur goal is to not reinvent the wheel where appropriate.\n\n### Imperative Experiences\n\nPyTorch is designed to be intuitive, linear in thought, and easy to use.\nWhen you execute a line of code, it gets executed. There isn't an asynchronous view of the world.\nWhen you drop into a debugger or receive error messages and stack traces, understanding them is straightforward.\nThe stack trace points to exactly where your code was defined.\nWe hope you never spend hours debugging your code because of bad stack traces or asynchronous and opaque execution engines.\n\n### Fast and Lean\n\nPyTorch has minimal framework overhead. We integrate acceleration libraries\nsuch as [Intel MKL](https://software.intel.com/mkl) and NVIDIA ([cuDNN](https://developer.nvidia.com/cudnn), [NCCL](https://developer.nvidia.com/nccl)) to maximize speed.\nAt the core, its CPU and GPU Tensor and neural network backends\nare mature and have been tested for years.\n\nHence, PyTorch is quite fast – whether you run small or large neural networks.\n\nThe memory usage in PyTorch is extremely efficient compared to Torch or some of the alternatives.\nWe've written custom memory allocators for the GPU to make sure that\nyour deep learning models are maximally memory efficient.\nThis enables you to train bigger deep learning models than before.\n\n### Extensions Without Pain\n\nWriting new neural network modules, or interfacing with PyTorch's Tensor API was designed to be straightforward\nand with minimal abstractions.\n\nYou can write new neural network layers in Python using the torch API\n[or your favorite NumPy-based libraries such as SciPy](https://pytorch.org/tutorials/advanced/numpy_extensions_tutorial.html).\n\nIf you want to write your layers in C/C++, we provide a convenient extension API that is efficient and with minimal boilerplate.\nNo wrapper code needs to be written. You can see [a tutorial here](https://pytorch.org/tutorials/advanced/cpp_extension.html) and [an example here](https://github.com/pytorch/extension-cpp).\n\n\n## Installation\n\n### Binaries\nCommands to install binaries via Conda or pip wheels are on our website: [https://pytorch.org/get-started/locally/](https://pytorch.org/get-started/locally/)\n\n\n#### NVIDIA Jetson Platforms\n\nPython wheels for NVIDIA's Jetson Nano, Jetson TX1/TX2, Jetson Xavier NX/AGX, and Jetson AGX Orin are provided [here](https://forums.developer.nvidia.com/t/pytorch-for-jetson-version-1-10-now-available/72048) and the L4T container is published [here](https://catalog.ngc.nvidia.com/orgs/nvidia/containers/l4t-pytorch)\n\nThey require JetPack 4.2 and above, and [@dusty-nv](https://github.com/dusty-nv) and [@ptrblck](https://github.com/ptrblck) are maintaining them.\n\n\n### From Source\n\n#### Prerequisites\nIf you are installing from source, you will need:\n- Python 3.7 or later (for Linux, Python 3.7.6+ or 3.8.1+ is needed)\n- A C++14 compatible compiler, such as clang\n\nWe highly recommend installing an [Anaconda](https://www.anaconda.com/distribution/#download-section) environment. You will get a high-quality BLAS library (MKL) and you get controlled dependency versions regardless of your Linux distro.\n\nIf you want to compile with CUDA support, install the following (note that CUDA is not supported on macOS)\n- [NVIDIA CUDA](https://developer.nvidia.com/cuda-downloads) 10.2 or above\n- [NVIDIA cuDNN](https://developer.nvidia.com/cudnn) v7 or above\n- [Compiler](https://gist.github.com/ax3l/9489132) compatible with CUDA\n\nNote: You could refer to the [cuDNN Support Matrix](https://docs.nvidia.com/deeplearning/cudnn/pdf/cuDNN-Support-Matrix.pdf) for cuDNN versions with the various supported CUDA, CUDA driver and NVIDIA hardware\n\nIf you want to disable CUDA support, export the environment variable `USE_CUDA=0`.\nOther potentially useful environment variables may be found in `setup.py`.\n\nIf you are building for NVIDIA's Jetson platforms (Jetson Nano, TX1, TX2, AGX Xavier), Instructions to install PyTorch for Jetson Nano are [available here](https://devtalk.nvidia.com/default/topic/1049071/jetson-nano/pytorch-for-jetson-nano/)\n\nIf you want to compile with ROCm support, install\n- [AMD ROCm](https://rocmdocs.amd.com/en/latest/Installation_Guide/Installation-Guide.html) 4.0 and above installation\n- ROCm is currently supported only for Linux systems.\n\nIf you want to disable ROCm support, export the environment variable `USE_ROCM=0`.\nOther potentially useful environment variables may be found in `setup.py`.\n\n#### Install Dependencies\n\n**Common**\n\n```bash\nconda install astunparse numpy ninja pyyaml setuptools cmake cffi typing_extensions future six requests dataclasses\n```\n\n**On Linux**\n\n```bash\nconda install mkl mkl-include\n# CUDA only: Add LAPACK support for the GPU if needed\nconda install -c pytorch magma-cuda110  # or the magma-cuda* that matches your CUDA version from https://anaconda.org/pytorch/repo\n```\n\n**On MacOS**\n\n```bash\n# Add this package on intel x86 processor machines only\nconda install mkl mkl-include\n# Add these packages if torch.distributed is needed\nconda install pkg-config libuv\n```\n\n**On Windows**\n\n```bash\nconda install mkl mkl-include\n# Add these packages if torch.distributed is needed.\n# Distributed package support on Windows is a prototype feature and is subject to changes.\nconda install -c conda-forge libuv=1.39\n```\n\n#### Get the PyTorch Source\n```bash\ngit clone --recursive https://github.com/pytorch/pytorch\ncd pytorch\n# if you are updating an existing checkout\ngit submodule sync\ngit submodule update --init --recursive --jobs 0\n```\n\n#### Install PyTorch\n**On Linux**\n\nIf you're compiling for AMD ROCm then first run this command:\n```bash\n# Only run this if you're compiling for ROCm\npython tools/amd_build/build_amd.py\n```\n\nInstall PyTorch\n```bash\nexport CMAKE_PREFIX_PATH=${CONDA_PREFIX:-\"$(dirname $(which conda))/../\"}\npython setup.py install\n```\n\nNote that if you are using [Anaconda](https://www.anaconda.com/distribution/#download-section), you may experience an error caused by the linker:\n\n```plaintext\nbuild/temp.linux-x86_64-3.7/torch/csrc/stub.o: file not recognized: file format not recognized\ncollect2: error: ld returned 1 exit status\nerror: command 'g++' failed with exit status 1\n```\n\nThis is caused by `ld` from the Conda environment shadowing the system `ld`. You should use a newer version of Python that fixes this issue. The recommended Python version is 3.7.6+ and 3.8.1+.\n\n**On macOS**\n\n```bash\nexport CMAKE_PREFIX_PATH=${CONDA_PREFIX:-\"$(dirname $(which conda))/../\"}\nMACOSX_DEPLOYMENT_TARGET=10.9 CC=clang CXX=clang++ python setup.py install\n```\n\n**On Windows**\n\nChoose Correct Visual Studio Version.\n\nSometimes there are regressions in new versions of Visual Studio, so\nit's best to use the same Visual Studio Version [16.8.5](https://github.com/pytorch/pytorch/blob/master/.circleci/scripts/vs_install.ps1) as Pytorch CI's.\n\nPyTorch CI uses Visual C++ BuildTools, which come with Visual Studio Enterprise,\nProfessional, or Community Editions. You can also install the build tools from\nhttps://visualstudio.microsoft.com/visual-cpp-build-tools/. The build tools *do not*\ncome with Visual Studio Code by default.\n\nIf you want to build legacy python code, please refer to [Building on legacy code and CUDA](https://github.com/pytorch/pytorch/blob/master/CONTRIBUTING.md#building-on-legacy-code-and-cuda)\n\n**CPU-only builds**\n\nIn this mode PyTorch computations will run on your CPU, not your GPU\n\n```cmd\nconda activate\npython setup.py install\n```\n\nNote on OpenMP: The desired OpenMP implementation is Intel OpenMP (iomp). In order to link against iomp, you'll need to manually download the library and set up the building environment by tweaking `CMAKE_INCLUDE_PATH` and `LIB`. The instruction [here](https://github.com/pytorch/pytorch/blob/master/docs/source/notes/windows.rst#building-from-source) is an example for setting up both MKL and Intel OpenMP. Without these configurations for CMake, Microsoft Visual C OpenMP runtime (vcomp) will be used.\n\n**CUDA based build**\n\nIn this mode PyTorch computations will leverage your GPU via CUDA for faster number crunching\n\n[NVTX](https://docs.nvidia.com/gameworks/content/gameworkslibrary/nvtx/nvidia_tools_extension_library_nvtx.htm) is needed to build Pytorch with CUDA.\nNVTX is a part of CUDA distributive, where it is called \"Nsight Compute\". To install it onto an already installed CUDA run CUDA installation once again and check the corresponding checkbox.\nMake sure that CUDA with Nsight Compute is installed after Visual Studio.\n\nCurrently, VS 2017 / 2019, and Ninja are supported as the generator of CMake. If `ninja.exe` is detected in `PATH`, then Ninja will be used as the default generator, otherwise, it will use VS 2017 / 2019.\n<br/> If Ninja is selected as the generator, the latest MSVC will get selected as the underlying toolchain.\n\nAdditional libraries such as\n[Magma](https://developer.nvidia.com/magma), [oneDNN, a.k.a MKLDNN or DNNL](https://github.com/oneapi-src/oneDNN), and [Sccache](https://github.com/mozilla/sccache) are often needed. Please refer to the [installation-helper](https://github.com/pytorch/pytorch/tree/master/.jenkins/pytorch/win-test-helpers/installation-helpers) to install them.\n\nYou can refer to the [build_pytorch.bat](https://github.com/pytorch/pytorch/blob/master/.jenkins/pytorch/win-test-helpers/build_pytorch.bat) script for some other environment variables configurations\n\n\n```cmd\ncmd\n\n:: Set the environment variables after you have downloaded and unzipped the mkl package,\n:: else CMake would throw an error as `Could NOT find OpenMP`.\nset CMAKE_INCLUDE_PATH={Your directory}\\mkl\\include\nset LIB={Your directory}\\mkl\\lib;%LIB%\n\n:: Read the content in the previous section carefully before you proceed.\n:: [Optional] If you want to override the underlying toolset used by Ninja and Visual Studio with CUDA, please run the following script block.\n:: \"Visual Studio 2019 Developer Command Prompt\" will be run automatically.\n:: Make sure you have CMake >= 3.12 before you do this when you use the Visual Studio generator.\nset CMAKE_GENERATOR_TOOLSET_VERSION=14.27\nset DISTUTILS_USE_SDK=1\nfor /f \"usebackq tokens=*\" %i in (`\"%ProgramFiles(x86)%\\Microsoft Visual Studio\\Installer\\vswhere.exe\" -version [15^,17^) -products * -latest -property installationPath`) do call \"%i\\VC\\Auxiliary\\Build\\vcvarsall.bat\" x64 -vcvars_ver=%CMAKE_GENERATOR_TOOLSET_VERSION%\n\n:: [Optional] If you want to override the CUDA host compiler\nset CUDAHOSTCXX=C:\\Program Files (x86)\\Microsoft Visual Studio\\2019\\Community\\VC\\Tools\\MSVC\\14.27.29110\\bin\\HostX64\\x64\\cl.exe\n\npython setup.py install\n\n```\n\n##### Adjust Build Options (Optional)\n\nYou can adjust the configuration of cmake variables optionally (without building first), by doing\nthe following. For example, adjusting the pre-detected directories for CuDNN or BLAS can be done\nwith such a step.\n\nOn Linux\n```bash\nexport CMAKE_PREFIX_PATH=${CONDA_PREFIX:-\"$(dirname $(which conda))/../\"}\npython setup.py build --cmake-only\nccmake build  # or cmake-gui build\n```\n\nOn macOS\n```bash\nexport CMAKE_PREFIX_PATH=${CONDA_PREFIX:-\"$(dirname $(which conda))/../\"}\nMACOSX_DEPLOYMENT_TARGET=10.9 CC=clang CXX=clang++ python setup.py build --cmake-only\nccmake build  # or cmake-gui build\n```\n\n### Docker Image\n\n#### Using pre-built images\n\nYou can also pull a pre-built docker image from Docker Hub and run with docker v19.03+\n\n```bash\ndocker run --gpus all --rm -ti --ipc=host pytorch/pytorch:latest\n```\n\nPlease note that PyTorch uses shared memory to share data between processes, so if torch multiprocessing is used (e.g.\nfor multithreaded data loaders) the default shared memory segment size that container runs with is not enough, and you\nshould increase shared memory size either with `--ipc=host` or `--shm-size` command line options to `nvidia-docker run`.\n\n#### Building the image yourself\n\n**NOTE:** Must be built with a docker version > 18.06\n\nThe `Dockerfile` is supplied to build images with CUDA 11.1 support and cuDNN v8.\nYou can pass `PYTHON_VERSION=x.y` make variable to specify which Python version is to be used by Miniconda, or leave it\nunset to use the default.\n```bash\nmake -f docker.Makefile\n# images are tagged as docker.io/${your_docker_username}/pytorch\n```\n\n### Building the Documentation\n\nTo build documentation in various formats, you will need [Sphinx](http://www.sphinx-doc.org) and the\nreadthedocs theme.\n\n```bash\ncd docs/\npip install -r requirements.txt\n```\nYou can then build the documentation by running `make <format>` from the\n`docs/` folder. Run `make` to get a list of all available output formats.\n\nIf you get a katex error run `npm install katex`.  If it persists, try\n`npm install -g katex`\n\n> Note: if you installed `nodejs` with a different package manager (e.g.,\n`conda`) then `npm` will probably install a version of `katex` that is not\ncompatible with your version of `nodejs` and doc builds will fail.\nA combination of versions that is known to work is `node@6.13.1` and\n`katex@0.13.18`. To install the latter with `npm` you can run\n```npm install -g katex@0.13.18```\n\n### Previous Versions\n\nInstallation instructions and binaries for previous PyTorch versions may be found\non [our website](https://pytorch.org/previous-versions).\n\n\n## Getting Started\n\nThree-pointers to get you started:\n- [Tutorials: get you started with understanding and using PyTorch](https://pytorch.org/tutorials/)\n- [Examples: easy to understand PyTorch code across all domains](https://github.com/pytorch/examples)\n- [The API Reference](https://pytorch.org/docs/)\n- [Glossary](https://github.com/pytorch/pytorch/blob/master/GLOSSARY.md)\n\n## Resources\n\n* [PyTorch.org](https://pytorch.org/)\n* [PyTorch Tutorials](https://pytorch.org/tutorials/)\n* [PyTorch Examples](https://github.com/pytorch/examples)\n* [PyTorch Models](https://pytorch.org/hub/)\n* [Intro to Deep Learning with PyTorch from Udacity](https://www.udacity.com/course/deep-learning-pytorch--ud188)\n* [Intro to Machine Learning with PyTorch from Udacity](https://www.udacity.com/course/intro-to-machine-learning-nanodegree--nd229)\n* [Deep Neural Networks with PyTorch from Coursera](https://www.coursera.org/learn/deep-neural-networks-with-pytorch)\n* [PyTorch Twitter](https://twitter.com/PyTorch)\n* [PyTorch Blog](https://pytorch.org/blog/)\n* [PyTorch YouTube](https://www.youtube.com/channel/UCWXI5YeOsh03QvJ59PMaXFw)\n\n## Communication\n* Forums: Discuss implementations, research, etc. https://discuss.pytorch.org\n* GitHub Issues: Bug reports, feature requests, install issues, RFCs, thoughts, etc.\n* Slack: The [PyTorch Slack](https://pytorch.slack.com/) hosts a primary audience of moderate to experienced PyTorch users and developers for general chat, online discussions, collaboration, etc. If you are a beginner looking for help, the primary medium is [PyTorch Forums](https://discuss.pytorch.org). If you need a slack invite, please fill this form: https://goo.gl/forms/PP1AGvNHpSaJP8to1\n* Newsletter: No-noise, a one-way email newsletter with important announcements about PyTorch. You can sign-up here: https://eepurl.com/cbG0rv\n* Facebook Page: Important announcements about PyTorch. https://www.facebook.com/pytorch\n* For brand guidelines, please visit our website at [pytorch.org](https://pytorch.org/)\n\n## Releases and Contributing\n\nPyTorch has a 90-day release cycle (major releases). Please let us know if you encounter a bug by [filing an issue](https://github.com/pytorch/pytorch/issues).\n\nWe appreciate all contributions. If you are planning to contribute back bug-fixes, please do so without any further discussion.\n\nIf you plan to contribute new features, utility functions, or extensions to the core, please first open an issue and discuss the feature with us.\nSending a PR without discussion might end up resulting in a rejected PR because we might be taking the core in a different direction than you might be aware of.\n\nTo learn more about making a contribution to Pytorch, please see our [Contribution page](CONTRIBUTING.md).\n\n## The Team\n\nPyTorch is a community-driven project with several skillful engineers and researchers contributing to it.\n\nPyTorch is currently maintained by [Adam Paszke](https://apaszke.github.io/), [Sam Gross](https://github.com/colesbury), [Soumith Chintala](http://soumith.ch) and [Gregory Chanan](https://github.com/gchanan) with major contributions coming from hundreds of talented individuals in various forms and means.\nA non-exhaustive but growing list needs to mention: Trevor Killeen, Sasank Chilamkurthy, Sergey Zagoruyko, Adam Lerer, Francisco Massa, Alykhan Tejani, Luca Antiga, Alban Desmaison, Andreas Koepf, James Bradbury, Zeming Lin, Yuandong Tian, Guillaume Lample, Marat Dukhan, Natalia Gimelshein, Christian Sarofeen, Martin Raison, Edward Yang, Zachary Devito.\n\nNote: This project is unrelated to [hughperkins/pytorch](https://github.com/hughperkins/pytorch) with the same name. Hugh is a valuable contributor to the Torch community and has helped with many things Torch and PyTorch.\n\n## License\n\nPyTorch has a BSD-style license, as found in the [LICENSE](LICENSE) file.\n\n\n",
        "description_content_type": "text/markdown",
        "docs_url": null,
        "download_url": "https://github.com/pytorch/pytorch/tags",
        "downloads": {
            "last_day": -1,
            "last_month": -1,
            "last_week": -1
        },
        "home_page": "https://pytorch.org/",
        "keywords": "pytorch,machine learning",
        "license": "BSD-3",
        "maintainer": "",
        "maintainer_email": "",
        "name": "torch",
        "package_url": "https://pypi.org/project/torch/",
        "platform": null,
        "project_url": "https://pypi.org/project/torch/",
        "project_urls": {
            "Download": "https://github.com/pytorch/pytorch/tags",
            "Homepage": "https://pytorch.org/"
        },
        "release_url": "https://pypi.org/project/torch/1.13.0/",
        "requires_dist": [
            "typing-extensions",
            "nvidia-cuda-runtime-cu11 (==11.7.99)",
            "nvidia-cudnn-cu11 (==8.5.0.96)",
            "nvidia-cublas-cu11 (==11.10.3.66)",
            "nvidia-cuda-nvrtc-cu11 (==11.7.99)",
            "opt-einsum (>=3.3) ; extra == 'opt-einsum'"
        ],
        "requires_python": ">=3.7.0",
        "summary": "Tensors and Dynamic neural networks in Python with strong GPU acceleration",
        "version": "1.13.0",
        "yanked": false,
        "yanked_reason": null
    },
    "last_serial": 15567777,
    "vulnerabilities": []
}
```
We have more data on releases. This only package gives a result of 
7000 lines of json.

### Selecting the data and making a Dependecy Graph

We have used TigerGraph to make our Graph.

Attributes used:
Name of Package, Dependencies and License

This is the 1st Schema we got:
![First Schema](https://drive.google.com/uc?export=view&id=1sAGJtExoyNofdxC-k8PmPSEec11yZX1R)

The data we got was not very good we included some more factors like Language used and Development Status
![2nd Schema](https://drive.google.com/uc?export=view&id=1jKBIAyKzDdKWB775RkKvXPCMaNXYB8Qp)

This was good, the graph we got after loading some data:
![Graph](https://drive.google.com/uc?export=view&id=1lOPOKEZmAMGajljnNIC5n2CSb5O8A7WH)

We did not have anything to Search so we added Search Meta
## Result
![Final Schema](https://drive.google.com/uc?export=view&id=1SojGsbzC30sGFHFgSpQPy4a1KLlXvb_0)

Now our Graph looks like:
![Final Graph](https://drive.google.com/uc?export=view&id=1HS-q6_R6zpERgk3zTtLiVchJ3F3KXihZ)

### After getting this our next step was to query and check the results
![GSQL Query](https://drive.google.com/uc?export=view&id=1V8rLN3ybwPD41l3CfdRjKE5CWuiPPQAP)

#### We got the data of the Packages that have the search query as Search_Meta



## Future Work
Our next step is to generate a confidence score that helps us in rating the packages.

Once that is working. Our project has to get the input from the users that what are the 
project they want to work on so that, we can do an NLP and get
the related Search Meta that we think is usefull and give them the output of 
the possible packages.
