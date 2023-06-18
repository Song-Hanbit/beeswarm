
# import packages
import numpy as np
from bokeh.plotting import figure, show
from bokeh.models import Whisker
from bokeh.palettes import Category20_4 as c
if __name__ == '__main__': from beeswarm import swarm
else: from beeswarm.beeswarm import swarm

# setting arbitrary data
dog = (25, 20)
cat = (75, 80)
p_dog = np.where(np.random.normal(dog[1], 10, 100) > 0, 
                 np.random.normal(dog[1], 10, 100), 0)
p_cat = np.where(np.random.normal(cat[1], 10, 100) < 100, 
                 np.random.normal(cat[1], 10, 100), 100)

# bokeh plot
radius = 0.5
s_dog = swarm(dog[0], p_dog, radius)
s_cat = swarm(cat[0], p_cat, radius)
p = figure(width=500, height=500, x_range=(0, 100), y_range=(0, 100), toolbar_location=None)
p.vbar(x=dog[0], top=p_dog.mean(), width=40, fill_color=c[1], line_color=c[0])
p.vbar(x=cat[0], top=p_cat.mean(), width=40, fill_color=c[3], line_color=c[2])
p.add_layout(Whisker(base=dog[0], lower=p_dog.mean() - p_dog.std(),
                     upper=p_dog.mean() + p_dog.std(), level='annotation', 
                     line_color='black'))
p.add_layout(Whisker(base=cat[0], lower=p_cat.mean() - p_cat.std(),
                     upper=p_cat.mean() + p_cat.std(), level='annotation', 
                     line_color='black'))
p.scatter(s_dog[:, 0], s_dog[:, 1], marker='circle', radius=radius, line_color=None,
          fill_color=c[0])
p.scatter(s_cat[:, 0], s_cat[:, 1], marker='circle', radius=radius, line_color=None,
          fill_color=c[2])
p.xaxis.ticker = [dog[0], cat[0]]
p.xaxis.major_label_overrides = {dog[0]:'🐶', cat[0]:'🐱'}
p.yaxis.axis_label = 'P(🐱)'
p.xgrid.grid_line_color = None
p.ygrid.grid_line_color = None
p.outline_line_color = 'black'
p.toolbar.logo = None
show(p)

