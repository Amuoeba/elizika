import matplotlib.pyplot as plt
import numpy as np
import matplotlib.pyplot as plt

plt.switch_backend('agg')
#
# objects = ('Python', 'C++', 'Java', 'Perl', 'Scala', 'Lisp')
# y_pos = np.arange(len(objects))
# performance = [10, 8, 6, 4, 2, 1]
#
# plt.bar(y_pos, performance, align='center', alpha=0.5)
# plt.xticks(y_pos, objects)
# plt.ylabel('Usage')
# plt.title('Programming language usage')
#
# plt.show()


def bar_freq_plot(x_ax, y_ax, name="default"):
    fig, ax = plt.subplots()
    ax.bar(x_ax, y_ax)
    fig.savefig('./Plots/'+name, transparent=False, dpi=80, bbox_inches="tight")
    plt.clf()
    plt.close("all")
    return None
