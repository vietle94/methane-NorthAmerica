#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Apr 17 15:56:25 2020

@author: tenkanen
"""

from glob import glob
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import numpy as np

fig_list_NO2 = sorted(glob('Figures/GIOVANNI-NO2*.png'))
fig_list_CH4 = sorted(glob('Figures/stropomi_3month_average_20*.png'))

figsize = (20,10)
for ind,fig_name in enumerate(fig_list_NO2):
    plt.figure(figsize=figsize)
    ax_ch4 = plt.subplot(2, 1, 1)
    ax_no2 = plt.subplot(2, 1, 2)
    
    img_ch4 = mpimg.imread(fig_list_CH4[ind])
    ax_ch4.imshow(img_ch4)
    ax_ch4.axis('off')

    img_no2 = mpimg.imread(fig_name)
    ax_no2.imshow(img_no2)
    ax_no2.axis('off')
        
    start = fig_name.split('_')[1]
    end = fig_name.split('_')[2]
    plt.savefig(f'Figures/XCH4_NO2_3month_average_{end}_{start}.png', dpi=150, bbox_inches='tight')
    plt.show()