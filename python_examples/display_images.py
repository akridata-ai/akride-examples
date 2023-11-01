import matplotlib.pyplot as plt


def display_images(images: list,
                   n_rows: int,
                   n_cols: int,
                   figure_w: int,
                   figure_h: int,
                   output_file_name: str = None):
    """Display a grid of n_rows x n_cols of images"""
    assert len(images) <= n_rows * n_cols
    fig = plt.figure(figsize=(figure_w, figure_h))
    for i, img in enumerate(images):
        fig.add_subplot(n_rows, n_cols, i + 1)
        plt.axis('off')
        plt.tight_layout()
        plt.imshow(img)

    if output_file_name is None:
        plt.show()
    else:
        plt.savefig(f"./{output_file_name}")
