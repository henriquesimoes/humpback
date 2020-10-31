import torch
import torch.nn.functional as F


def global_contrast_norm(x, scale=1, lmbda=0, eps=1e-8):
    """
    Applies the Global Contrast Normalization (GCN) to a image batch.

    # Parameters

    x : `torch.Tensor`, required
        Image batch with shape=(batch_size, channels, width, height)
    scale : `float`, optional (default = 1)
        Result scaling factor
    lmbda : `float`, optional (default = 0)
        Standard deviation bias term.
    eps : `float`, optional (default = 1e-8)
        Constant for division numeric stability

    # Returns

    y : `torch.Tensor`
        Normalized batch with the same shape as `x`
    """
    x = x - torch.mean(x, dim=(1, 2, 3), keepdim=True)

    contrast = torch.sqrt(lmbda + torch.mean(x ** 2, dim=(1, 2, 3), keepdim=True))

    x = scale * x / contrast.clamp(min=eps)

    return x


def local_contrast_norm(x, kernel_size=9, scale=1, lmbda=0, eps=1e-8):
    """
    Applies the Local Contrast Normalization (LCN) to a image batch.

    It uses the arithmetic average over all channels to combine the
    neighboring pixels.

    # Parameters

    x : `torch.Tensor`, required
        Image batch with shape=(batch_size, channels, width, height)
    kernel_size : `int`, odd, optional (default = 9)
        Kernel size to be used collect nearby pixel statistics
    scale : `float`, optional (default = 1)
        Result scaling factor
    lmbda : `float`, optional (default = 0)
        Standard deviation bias term.
    eps : `float`, optional (default = 1e-8)
        Constant for division numeric stability

    # Returns

    y : `torch.Tensor`
        Normalized batch with the same shape as `x`
    """
    batch_size, channels, w, h = x.shape

    # pad convolution to guarantee all pixels will be covered, and
    # the convolution output's shape is equal to the input's
    padding = (kernel_size - 1) // 2

    kernel = torch.ones((1, channels, kernel_size, kernel_size), dtype=torch.float32) / (
                channels * kernel_size * kernel_size)

    mean = F.conv2d(x, weight=kernel, padding=padding)
    x = x - mean

    var = F.conv2d(x ** 2, weight=kernel, padding=padding)
    std = (lmbda + var).sqrt().clamp(min=eps)

    x = scale * x / std

    return x


def imagenet_norm(x):
    """
    Normalizes the input image batch using the ImageNet image statistics
    (i.e. mean and standard deviation).

    # Parameters

    x : `torch.Tensor`, required
      Image batch with shape=(batch_size, channels, width, height)

    # Returns

    y : `torch.Tensor`
        Normalized batch with the same shape as `x`
    """
    mean = [0.485, 0.456, 0.406]  # rgb
    std = [0.229, 0.224, 0.225]

    x = torch.cat([
        (x[:, [0]] - mean[0]) / std[0],
        (x[:, [1]] - mean[1]) / std[1],
        (x[:, [2]] - mean[2]) / std[2],
    ], 1)

    return x


if __name__ == "__main__":
    import time
    import argparse
    import numpy as np
    from PIL import Image

    ap = argparse.ArgumentParser()
    ap.add_argument('-i', dest="image", required=True, help="test image")
    config = ap.parse_args()

    image = Image.open(config.image).convert('RGB').resize((512, 256))

    image = np.asarray(image).transpose((2, 0, 1))

    image = torch.FloatTensor(image / 255)

    images = torch.stack([image.clone() for _ in range(5)])

    t = time.time()
    imgs = [image,
            imagenet_norm(images)[0] + .5,
            global_contrast_norm(images, scale=1, lmbda=1)[0] + .5,
            local_contrast_norm(images, scale=1, lmbda=1)[0] + .5]
    print('It took', time.time() - t, 'seconds to run...')

    for img in imgs:
        image = (img * 255).clamp(min=0, max=255).numpy().transpose((1, 2, 0))

        Image.fromarray(image.astype(np.uint8)).show()
