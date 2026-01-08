def hit_animation(widget, on_finish=None):
    colors = ["#ffcccc", "#ff6666", "#cc0000"]

    def step(i=0):
        if i < len(colors):
            widget.config(bg=colors[i])
            widget.after(70, step, i + 1)
        else:
            if on_finish:
                on_finish()

    step()

def miss_animation(widget, on_finish=None):
    colors = ["#cceeff", "#66ccff", "#3399ff"]

    def step(i=0):
        if i < len(colors):
            widget.config(bg=colors[i])
            widget.after(70, step, i + 1)
        else:
            if on_finish:
                on_finish()

    step()

def invalid_click_animation(widget):
    colors = ["#ffaaaa", "blue"]
    def step(i=0):
        if i < len(colors):
            widget.config(bg=colors[i])
            widget.after(80, step, i + 1)
    step()
