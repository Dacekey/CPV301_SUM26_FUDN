import matplotlib.pyplot as plt


def showme(imgs, titles=None, cmap=None, estimate=5):
    core_num = len(imgs)

    if titles is None:
        titles = [""] * core_num

    plt.figure(figsize=(core_num * estimate, estimate))

    for i in range(core_num):
        plt.subplot(1, core_num, i + 1)
        plt.imshow(imgs[i], cmap=cmap)
        plt.title(titles[i])
        plt.axis("off")

    plt.show()
