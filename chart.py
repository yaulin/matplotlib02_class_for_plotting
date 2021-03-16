# load necessary libraries


# Standard library
from io import BytesIO

# 3rd party
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from  matplotlib import colors, patches
from matplotlib.font_manager import FontProperties
from matplotlib.figure import Figure
from matplotlib.backends.backend_agg import FigureCanvasAgg
from matplotlib.ticker import FormatStrFormatter, FuncFormatter
import matplotlib.dates as mdates
from matplotlib.patches import Polygon

from matplotlib.ticker import (MultipleLocator, FormatStrFormatter,
                               AutoMinorLocator)


from matplotlib.path import Path
from matplotlib.patches import PathPatch

from matplotlib.lines import Line2D


import datetime

import numpy as np
import pandas as pd


# class for plotting

class Chart(object):
    #-----------------------------------------------------------------------------   
    #constructor
        
    def __init__(self,dict):
        
        self.dict=dict
        
        self.nseries=len(dict['series'])
        self.dpi=100
        
        # Setup figure size (wxh) in inches (dpi is for PNG generation)
        self.plt=plt
              
        self.fig=plt.figure(figsize=(self.dict['chart_size']['width']/self.dpi,
                                self.dict['chart_size']['height']/self.dpi),
                       dpi=self.dpi)
        
        self.canvas = FigureCanvasAgg(self.fig)
        
        
        
        
        # add axes, last parameter is not 1 to have proper display of subtitle
        
        if self.dict['x_axis']['text']!=None:
            
            self.ax=self.fig.add_axes([0.1,0.3,0.8,0.5])
        
        else:
            
            self.ax=self.fig.add_axes([0.1,0.175,0.8,0.65]) 
            
                      
        
                   
        
        # check if there are traces associated with secondary axis
        self.ax2b=False
        
        for s in self.dict['series']:
            if 'line_plot' in s:
                if s['line_plot']['y-axis']=='secondary':
                    self.ax2b=True
                
            if 'area_plot' in s:
                if s['area_plot']['y-axis']=='secondary':
                    self.ax2b=True
                        
        if self.ax2b: self.ax2 = self.ax.twinx()
        

        # Create an Agg canvas for rendering
        self.canvas = FigureCanvasAgg(self.fig)

        
    #-----------------------------------------------------------------------------   
    
    #format title    
    def format_title(self):
        title=self.dict['title']
            
        if self.dict['title']!=None:
            
            if title['anchor']=='center':
                x0 = 0.5
            if title['anchor']=='right':
                x0 = 1
            if title['anchor']=='left':
                x0 = 0
            
          
      #      self.fig.suptitle(
       #         title['text'],
      #          color=title['color'],
       #        size=title['size'],
       #        family=title['font'],
        #       x=x0,y=1.2
        #       )
            
            
            plt.figtext(x0,0.9,title['text'], fontsize=title['size'],family=title['font'],color=title['color'], ha='center')
            
            
         
            
    #-----------------------------------------------------------------------------   
            
    # format subtitle    
    def format_subtitle(self):
        if self.dict['subtitle']!=None:
            subtitle=self.dict['subtitle']
            
            if subtitle['anchor']=='center':
                x0= 0.5
            if subtitle['anchor']=='right':
                x0 = 1
            if subtitle['anchor']=='left':
                x0 = 0
                
          #  self.ax.set_title(
           #     subtitle['text'],
          #      loc=subtitle['anchor'],
           #     color=subtitle['color'],
           #     size=subtitle['size'],
           #     family=subtitle['font'],
           #     x=x0
           #     )
            
            plt.figtext(x0,0.85,subtitle['text'], fontsize=subtitle['size'],family=subtitle['font'],color=subtitle['color'], ha='center')
            
            
       
    #-----------------------------------------------------------------------------   
              
    # format borders
    def format_borders(self):
        
        if self.dict['borders']['left']!=None:
            self.ax.spines['left'].set_color(self.dict['borders']['left']['color'])
            self.ax.spines['left'].set_linewidth(self.dict['borders']['left']['size'])
            if self.ax2b:
                self.ax2.spines['left'].set_color(self.dict['borders']['left']['color'])
                self.ax2.spines['left'].set_linewidth(self.dict['borders']['left']['size'])
        else:
            self.ax.spines['left'].set_visible(False)
            if self.ax2b:
                self.ax2.spines['left'].set_visible(False)
                
        if self.dict['borders']['right']!=None:
            self.ax.spines['right'].set_color(self.dict['borders']['right']['color'])
            self.ax.spines['right'].set_linewidth(self.dict['borders']['right']['size'])
            if self.ax2b:
                self.ax2.spines['right'].set_color(self.dict['borders']['right']['color'])
                self.ax2.spines['right'].set_linewidth(self.dict['borders']['right']['size'])
        else:
            self.ax.spines['right'].set_visible(False)
            if self.ax2b:
                self.ax2.spines['right'].set_visible(False) 
            
        if self.dict['borders']['top']!=None:
            self.ax.spines['top'].set_color(self.dict['borders']['top']['color'])
            self.ax.spines['top'].set_linewidth(self.dict['borders']['top']['size'])
            if self.ax2b:
                self.ax2.spines['top'].set_color(self.dict['borders']['top']['color'])
                self.ax2.spines['top'].set_linewidth(self.dict['borders']['top']['size'])
        else:
            self.ax.spines['top'].set_visible(False)
            if self.ax2b:
                self.ax2.spines['top'].set_visible(False) 
            
        if self.dict['borders']['bottom']!=None:
            self.ax.spines['bottom'].set_color(self.dict['borders']['bottom']['color'])
            self.ax.spines['bottom'].set_linewidth(self.dict['borders']['bottom']['size'])
            if self.ax2b:
                self.ax2.spines['bottom'].set_color(self.dict['borders']['bottom']['color'])
                self.ax2.spines['bottom'].set_linewidth(self.dict['borders']['bottom']['size'])
        else:
            self.ax.spines['bottom'].set_visible(False)
            if self.ax2b:
                self.ax2.spines['bottom'].set_visible(False)
  
    #-----------------------------------------------------------------------------   
              
    # format x axis
    def format_x_axis(self):
        if self.dict['x_axis']['text']!=None:
            self.ax.set_xlabel(
                self.dict['x_axis']['text'],
                family=self.dict['x_axis']['font'],
                fontsize=self.dict['x_axis']['size'],
                color=self.dict['x_axis']['color'],
                va=self.dict['x_axis']['anchor'],
                labelpad=20
                )
            
            if self.dict['x_axis']['anchor']=='bottom':
                self.ax.xaxis.set_label_coords(0,-0.35)
            if self.dict['x_axis']['anchor']=='top':
                self.ax.xaxis.set_label_coords(1,-0.35)
            if self.dict['x_axis']['anchor']=='center':
                self.ax.xaxis.set_label_coords(0.5,-0.35)
                
                
                
        self.ax.tick_params(axis='x', rotation=self.dict['x_axis']['rotate'])
        
        if self.dict['x_axis']['major_ticks']!=None:
            self.ax.tick_params(axis='x', which='major', color=self.dict['x_axis']['major_ticks']['color'])
        else:
            self.ax.tick_params(axis='x', which='major', bottom = False, top = False)
            
        if self.dict['x_axis']['minor_ticks']!=None:
            self.ax.xaxis.set_minor_locator(AutoMinorLocator())
            self.ax.tick_params(axis='x', which='minor', color=self.dict['x_axis']['minor_ticks']['color'])
        else:
            self.ax.tick_params(axis='x', which='minor', bottom = False, top = False)
     #-----------------------------------------------------------------------------   
              
     # format y axis
    
    def format_y_axis(self):
        if self.dict['y_axis']['text']!=None:
            self.ax.set_ylabel(
                self.dict['y_axis']['text'],
                family=self.dict['y_axis']['font'],
                fontsize=self.dict['y_axis']['size'],
                color=self.dict['y_axis']['color'],
                va=self.dict['y_axis']['anchor'],
                labelpad=20,
                zorder=101
                )
            
            if self.dict['y_axis']['anchor']=='bottom':
                self.ax.yaxis.set_label_coords(-0.1,0)
            if self.dict['y_axis']['anchor']=='top':
                self.ax.yaxis.set_label_coords(-0.1,1)
            if self.dict['y_axis']['anchor']=='center':
                self.ax.yaxis.set_label_coords(-0.1,0.5)
            
        
        self.ax.tick_params(axis='y', rotation=self.dict['y_axis']['rotate'])
        
        if self.dict['y_axis']['major_ticks']!=None:
            self.ax.tick_params(axis='y', which='major', color=self.dict['y_axis']['major_ticks']['color'])
        else:
            self.ax.tick_params(axis='y', which='major', left = False, right = False)
            
        if self.dict['y_axis']['minor_ticks']!=None:
            self.ax.yaxis.set_minor_locator(AutoMinorLocator())
            self.ax.tick_params(axis='y', which='minor', color=self.dict['y_axis']['minor_ticks']['color'])
        else:
            self.ax.tick_params(axis='y', which='minor', left = False, right = False)

      

     #-----------------------------------------------------------------------------   
              
     # format y2 axis    
    
    
    def format_y2_axis(self):
        if self.ax2b:  
            if self.dict['y2_axis']['text']!=None:
                self.ax2.set_ylabel(
                    self.dict['y2_axis']['text'],
                    family=self.dict['y2_axis']['font'],
                    fontsize=self.dict['y2_axis']['size'],
                    color=self.dict['y2_axis']['color'],
                    va=self.dict['y2_axis']['anchor'],
                    labelpad=20
                    )
            if self.dict['y2_axis']['anchor']=='bottom':
                self.ax2.yaxis.set_label_coords(1.1,0)
            if self.dict['y2_axis']['anchor']=='top':
                self.ax2.yaxis.set_label_coords(1.1,1)
            if self.dict['y2_axis']['anchor']=='center':
                self.ax2.yaxis.set_label_coords(1.1,0.5)
                
            self.ax2.tick_params(axis='y', rotation=self.dict['y2_axis']['rotate'])
        
            if self.dict['y2_axis']['major_ticks']!=None:
                self.ax2.tick_params(axis='y', which='major', color=self.dict['y2_axis']['major_ticks']['color'])
            else:
                self.ax2.tick_params(axis='y', which='major', left = False,right = False)
            
            if self.dict['y2_axis']['minor_ticks']!=None:
                self.ax2.yaxis.set_minor_locator(AutoMinorLocator())
                self.ax2.tick_params(axis='y', which='minor', color=self.dict['y2_axis']['minor_ticks']['color'])
            else:
                self.ax2.tick_params(axis='y', which='minor', left = False, right = False)

   
    #-----------------------------------------------------------------------------   
              
    # add gridlines   
           
    def add_gridlines(self):
        if self.dict['x_axis']['grid_lines']!=None:
            if self.dict['x_axis']['grid_lines']['on_top']:
                z=5
            else:
                z=0
                
            self.ax.grid(
                axis='x',
                color=self.dict['x_axis']['grid_lines']['color'],
                linewidth=self.dict['x_axis']['grid_lines']['size'],
                linestyle=self.dict['x_axis']['grid_lines']['style'],
                )
                     
            
            lines = self.ax.xaxis.get_gridlines().copy()
            #ax.grid(False)
            for l in lines:
                self.ax.add_line(l)
                l.set_zorder(z)
        
        if self.dict['y_axis']['grid_lines']!=None:
            if self.dict['y_axis']['grid_lines']['on_top']:
                z=5
            else:
                z=0
                
            self.ax.grid(
                axis='y',
                color=self.dict['y_axis']['grid_lines']['color'],
                linewidth=self.dict['y_axis']['grid_lines']['size'],
                linestyle=self.dict['y_axis']['grid_lines']['style'],
                )
                     
            
            lines = self.ax.yaxis.get_gridlines().copy()
            #ax.grid(False)
            for l in lines:
                self.ax.add_line(l)
                l.set_zorder(z)
                
    
    
        if self.dict['y2_axis']['grid_lines']!=None:
            if self.dict['y2_axis']['grid_lines']['on_top']:
                z=5
            else:
                z=0
                
                
                
            if self.ax2b:
                
                self.ax2.grid(
                    axis='y',
                    color=self.dict['y2_axis']['grid_lines']['color'],
                    linewidth=self.dict['y2_axis']['grid_lines']['size'],
                    linestyle=self.dict['y2_axis']['grid_lines']['style'],
                    )
                     
            
                lines = self.ax2.yaxis.get_gridlines().copy()
            
                for l in lines:
                    self.ax2.add_line(l)
                    l.set_zorder(z)
            
    
    
    
    
    #----------------------------------------------------------------------------
    # add legend
    
    def add_legend(self):
     
        
        
        custom_lines=[]
        custom_names=[]
        
        
        for s in self.dict['series']:
            
            if 'line_plot' in s :
                
                custom_lines.append(Line2D([0], [0], color=s['line_plot']['color'],
                                           lw=s['line_plot']['size']))
                custom_names.append(s['line_plot']['series_name'])
                
            if 'area_plot' in s:
                if s['area_plot']['line_style']!=None:
                    col1=s['area_plot']['line_style']['color']
                    s1=s['area_plot']['line_style']['size']
                else:
                    col1=s['area_plot']['stop_color']
                    s1=6
                custom_lines.append(Line2D([0], [0], color=col1,lw=s1))
                custom_names.append(s['area_plot']['series_name'])
                
                
                
        
        
        
        
        #custom_lines = [Line2D([0], [0], color='red', lw=4),
        #        Line2D([0], [0], color='green', lw=4),
         #       Line2D([0], [0], color='blue', lw=4)]
        
        if self.dict['legend']!=None:
            
            x=0.5
            y=0.5
            
            
            if self.dict['legend']['anchor']=='lower left':
                x=-0.1
                y=-0.6
            if self.dict['legend']['anchor']=='lower center':
                x=0.5
                y=-0.6
            if self.dict['legend']['anchor']=='lower right':
                x=1.1
                y=-0.6
            
            

            leg=self.plt.legend(custom_lines,custom_names,
                            loc=self.dict['legend']['anchor'],
                            prop={'family':self.dict['legend']['font'],
                            'size':self.dict['legend']['size']},
                                bbox_to_anchor=(x,y),
                                frameon=False,
                                ncol=5
                                 )
            
            
            
            leg.set_zorder(200)
        
        
            
            
          
        
         #   self.ax.legend()
         # leg.set_zorder(101)
            
            #print(leg.get_texts())
            
       # for text in leg.get_texts():
        #        text.set_color(self.dict['legend']['color'])
                
    #----------------------------------------------------------------------------
    # format date
                
    def format_date(self):           
        locator = mdates.AutoDateLocator(minticks=3, maxticks=7)
        #formatter = mdates.ConciseDateFormatter(locator)
        self.ax.xaxis.set_major_locator(locator)
        #self.ax.xaxis.set_major_formatter(formatter)
        self.ax.xaxis.set_major_formatter(mdates.DateFormatter('%H-%M'))
        
        if self.ax2b:
            self.ax2.xaxis.set_major_locator(locator)
            #self.ax2.xaxis.set_major_formatter(formatter)
            self.ax2.xaxis.set_major_formatter(mdates.DateFormatter('%H-%M'))
                  
                
                           
   #-----------------------------------------------------------------------------
   # plot all                     
                        
    def plot_all(self):
         
           
        for s in self.dict['series']:
            
            #----------------------------------------
            # plot line plot
            
            if 'line_plot' in s:
                x=[x1[0] for x1 in s['line_plot']['data']]
                y=[x1[1] for x1 in s['line_plot']['data']]
                
                x=mdates.date2num(x)
                self.ax.xaxis_date()
                self.ax.set_xlim(min(x),max(x))
                if self.ax2b:
                    self.ax2.xaxis_date()
                    self.ax2.set_xlim(min(x),max(x))
                
                if s['line_plot']['y-axis']=='primary':
                    self.ax.plot(
                        x,y,
                        color='blue',
                        #color=s['line_plot']['color'],
                        linewidth=s['line_plot']['size'],
                        zorder=3,
                        label=s['line_plot']['series_name']
                        )
                    
                    
                    
                if s['line_plot']['y-axis']=='secondary' and self.ax2b:
                    self.ax2.plot(
                        x,y,
                        color=s['line_plot']['color'],
                        linewidth=s['line_plot']['size'],
                        zorder=3,
                        label=s['line_plot']['series_name']
                        )
            #----------------------------------------
            # plot area plot
            
            if 'area_plot' in s:
                x=[x1[0] for x1 in s['area_plot']['data']]
                y=[x1[1] for x1 in s['area_plot']['data']]
                
                x=mdates.date2num(x)
                x=np.array(x)
                y=np.array(y)
                
                
                #primary axis
                 
                if s['area_plot']['y-axis']=='primary':
                    
                    self.ax.xaxis_date()
                    self.ax.set_xlim(min(x),max(x))
                
                    if self.ax2b:
                        self.ax2.xaxis_date()
                        self.ax2.set_xlim(min(x),max(x))
                    
                    
                    fill_color1=s['area_plot']['start_color']
                    fill_color2=s['area_plot']['stop_color']
                    
                    

                    rgb0 = colors.colorConverter.to_rgb(fill_color1)
                    rgb1 = colors.colorConverter.to_rgb(fill_color2)
    
                    cmap = colors.LinearSegmentedColormap.from_list('tmp', (rgb0, rgb1))


                 
            
                    
                    path = Path(np.array([x,y]).transpose())
                    patch = PathPatch(path,fc='none',ec='none')
                    self.ax.add_patch(patch)

                    im = self.ax.imshow(x.reshape(y.size,1),  cmap=cmap,interpolation="bicubic",
                                       origin='lower',extent=[min(x),
                                       max(x),
                                       0,max(y)],aspect="auto", clip_path=patch, clip_on=True,
                                       zorder=3)



                    

                  


                                        
                        

                    
                    if s['area_plot']['line_style']!=None:
                        self.ax.plot(x,y,
                                color=s['area_plot']['line_style']['color'],
                                linewidth=s['area_plot']['line_style']['size'],
                                zorder=3,
                                label=s['area_plot']['series_name']
                                )
                        
                        
                # secondary axis    
                        
                if s['area_plot']['y-axis']=='secondary' and self.ax2b:
                    
                    self.ax.xaxis_date()
                    self.ax.set_xlim(min(x),max(x))
                
                    self.ax2.xaxis_date()
                    self.ax2.set_xlim(min(x),max(x))
                    
                    
                    fill_color1=s['area_plot']['start_color']
                    fill_color2=s['area_plot']['stop_color']
                    
                    

                    rgb0 = colors.colorConverter.to_rgb(fill_color1)
                    rgb1 = colors.colorConverter.to_rgb(fill_color2)
    
                    cmap = colors.LinearSegmentedColormap.from_list('tmp', (rgb0, rgb1))


                 
            
                    
                    path = Path(np.array([x,y]).transpose())
                    patch = PathPatch(path, fc='none',ec='none')
                    self.ax2.add_patch(patch)

                    im = self.ax2.imshow(x.reshape(y.size,1),  cmap=cmap,interpolation="bicubic",
                    origin='lower',extent=[min(x),
                                       max(x),
                                       0,max(y)],aspect="auto", clip_path=patch, clip_on=True,
                                        zorder=3)



                    

                   

                                        
                        

                    
                    if s['area_plot']['line_style']!=None:
                           self.ax2.plot(
                            x,y,
                            color=s['area_plot']['line_style']['color'],
                            linewidth=s['area_plot']['line_style']['size'],
                            zorder=3,
                            label=s['area_plot']['series_name']
                            )
            
            
    #-----------------------------------------------------------------------------   
              
     # autoscale
    
    def autoscale(self):
        
            
           
        
             
                       
                
                
        # determine x range
        
        xall=[]     
                
        for s in self.dict['series']:
            if 'line_plot' in s :
                x=[x1[0] for x1 in s['line_plot']['data']]
                
            if 'area_plot' in s:
                x=[x1[0] for x1 in s['area_plot']['data']]
                
            for i in range(len(x)):
                xall.append(x[i])
            
        xmin=min(xall)
        xmax=max(xall)
                
                
        # determine y range
               
                
        yall=np.array([])      
                
        for s in self.dict['series']:
            if ('line_plot' in s) and (s['line_plot']['y-axis']=='primary')  :
                y=[x1[1] for x1 in s['line_plot']['data']]
                
            if ('area_plot' in s) and (s['area_plot']['y-axis']=='primary'):
                y=[x1[1] for x1 in s['area_plot']['data']]
                
            yall=np.append(yall,y)
            
        ymin=min(yall)
        ymax=max(yall)
        
        
        # determine y2 range
        
        
        y2all=np.array([])      
                
        for s in self.dict['series']:
            if ('line_plot' in s) and (s['line_plot']['y-axis']=='secondary')  :
                y=[x1[1] for x1 in s['line_plot']['data']]
                
            if ('area_plot' in s) and (s['area_plot']['y-axis']=='secondary'):
                y=[x1[1] for x1 in s['area_plot']['data']]
                
            y2all=np.append(y2all,y)
            
        y2min=min(y2all)
        y2max=max(y2all)
        
                 
          
        
        self.ax.set_xlim(xmin,xmax)
        self.ax.set_ylim(ymin,ymax)
        if self.ax2b:
            self.ax2.set_ylim(y2min,y2max)
        
    
    #-----------------------------------------------------------------------------   
              
     
        
        
              
            
        
                    
        
        
        
        
                
                
                



    #-----------------------------------------------------------------------------   
              
     # render    
              
        
        
        
           
    def render(self):
        self.format_title()
        self.format_subtitle()
        self.format_borders()
        self.format_x_axis()
        self.format_y_axis()
        self.format_y2_axis()
        

        
                      
        self.plot_all()
       
                
        self.format_date()
        
        self.add_legend()
       
        self.add_gridlines()
        self.autoscale()
        
       # self.ax.set_ylabel('YLabel')
       # self.ax.yaxis.set_label_coords(-0.1,0)
             
        
        
        
        b = BytesIO()
        self.fig.savefig(b, format='png')
        return b.getvalue()
        
        
        
    
        
        
 


