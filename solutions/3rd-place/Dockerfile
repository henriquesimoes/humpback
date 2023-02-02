FROM ufoym/deepo:pytorch-py38-cu113
RUN /usr/bin/python3 -m pip install --upgrade pip
RUN apt update
RUN apt install -y libgl1 libglib2.0-0 libsm6 libxrender1 libxext6
RUN apt install -y python3-venv --fix-missing
RUN python3 -m venv tutorial-env
RUN . tutorial-env/bin/activate
RUN pip3 install imgaug albumentations pretrainedmodels easydict
