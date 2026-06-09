import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

fig, axs = plt.subplots(3, 1, figsize=(10, 8))

def update(frame):

    df = pd.read_csv("metrics.csv")

    for ax in axs:
        ax.clear()

    axs[0].plot(df["memory"])
    axs[0].set_title("Uso de Memória RAM")

    axs[1].plot(df["cpu"])
    axs[1].set_title("Uso de CPU")

    axs[2].plot(df["network"])
    axs[2].set_title("Tráfego de Rede")

    plt.tight_layout()

ani = FuncAnimation(
    fig,
    update,
    interval=5000,
    cache_frame_data=False
)

plt.show()