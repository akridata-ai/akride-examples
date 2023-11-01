import matplotlib.pyplot as plt


def display_images(images: list,
                   n_rows: int,
                   n_cols: int,
                   figure_w: int,
                   figure_h: int,
                   save_file: str = None):
    """Display a grid of n_rows x n_cols of images. Show the images or save if path provided"""
    assert len(images) <= n_rows * n_cols
    fig = plt.figure(figsize=(figure_w, figure_h))
    for i, img in enumerate(images):
        fig.add_subplot(n_rows, n_cols, i + 1)
        plt.axis('off')
        plt.tight_layout()
        plt.imshow(img)

    if save_file is None:
        plt.show()
    else:
        plt.savefig(save_file)
