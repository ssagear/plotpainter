from re import sub
import numpy as np
import matplotlib
matplotlib.use("TkAgg")
from matplotlib import pyplot as plt
import pdb
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from plotpainter import extracted_figure_class as efc
import PySimpleGUI as sg

import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)

def run_GUI(fig):
    """
    When you run the plotpainter GUI with a given matplotlib.figure.Figure, it brings
    up your plot in a GUI that you can use to change the plot colors.

    Args:

         fig (matplotlib.figure.Figure): the matplotlib Figure that the user will change colors
                                    of artists on

    Returns:

         None
    """
    
    # Create ExtractedFigure object using the given matplotlib.figure.Figure object
    extractedfig = efc.ExtractedFigure(fig=fig)

    # Collect the subplots in the Figure and their associated matplotlib Artists that have been
    # plotted in the Figure. These will be used in the drop-down menus in the GUI, allowing the user
    # to select a given subplot and given Artist to change the color of.
    subplots = []
    subplots_ints = []
    artists = np.empty(np.array(extractedfig.plotted_artists_labels).shape, dtype=np.dtype('U100'))

    for i in range(len(extractedfig.extracted_artist_list)):
        subplots.append('Subplot ' + str(i))
        subplots_ints.append(i)
        for j in range(len(extractedfig.extracted_artist_list[i])):
            if extractedfig.plotted_artists_labels[i][j][0] == '_':
                artists[i][j] = 'Subplot ' + str(i) +\
                                '; Artist ' + str(j) +\
                                '; Type ' + str(extractedfig.plotted_artists_types[i][j][0]) +\
                                '; Original Color ' + str(extractedfig.plotted_artists_colors[i][j])
            else:
                artists[i][j] =  'Subplot ' + str(i) + '; ' + extractedfig.plotted_artists_labels[i][j] +\
                                 '; Type ' + str(extractedfig.plotted_artists_types[i][j][0]) +\
                                 '; Original Color ' + str(extractedfig.plotted_artists_colors[i][j])

    subplots = np.array(subplots)
    artists= np.array(artists)

    # Create the layout of the window that will hold the GUI
    
    line_type = ['solid', 'dotted', 'dashed', 'dashdot']

    layout = [
    [sg.T('Graph')],
    [sg.B('Plot'), sg.B('Exit')],
    [sg.T('Controls:')],
    [sg.Canvas(key='controls_cv')],
    [sg.T('Figure:')],
    [sg.Column(
        layout=[[sg.Canvas(key='fig_cv', size=(400 * 2, 400))]],
        background_color='#DAE0E6',
        pad=(0, 0)
    )],
    [sg.In(key='color', enable_events=True, visible=False), sg.ColorChooserButton(button_text='Choose Color', target='color')],
    [sg.Listbox(values=list(artists.flatten()), select_mode='extended', key='artst', size=(30, 6))],
    [sg.T('Choose line:  '), sg.Slider(orientation ='horizontal', key='lineSlider', range=(0,3))]
    ]

    # Start window and draw Figure with the Toolbar (from interactive iPython)

    window = sg.Window('Graph with controls', layout, finalize=True)
    draw_figure_w_toolbar(window['fig_cv'].TKCanvas, extractedfig.extracted_figure, window['controls_cv'].TKCanvas)
    pdb.set_trace()
    while read:

        try:
            event, values = window.read()
            indices = np.where(artists == values['artst'])
            splot = int(indices[0])
            art = int(indices[1])
            hex_code = values['color']

            line_index_float = values['lineSlider']
            line_index = int(line_index_float)

            

        except TypeError:
            continue

        # Commenting exit/break out because the program crashes if you click exit :(

        if event == sg.WIN_CLOSED: 
            break
        
        elif event in ('lineSlider', 'color', 'Plot'):
            try:
                DPI = extractedfig.extracted_figure.get_dpi()
                extractedfig.extracted_figure.set_size_inches(404 * 2 / float(DPI), 404 / float(DPI))
                extractedfig.extracted_artist_list[splot][art].set_color(hex_code)
                draw_figure_w_toolbar(window['fig_cv'].TKCanvas, extractedfig.extracted_figure, window['controls_cv'].TKCanvas)
            except ValueError:
                draw_figure_w_toolbar(window['fig_cv'].TKCanvas, extractedfig.extracted_figure, window['controls_cv'].TKCanvas)

        
    window.close()



class Toolbar(NavigationToolbar2Tk):
   """
   Toolbar for the PySimpleGUI window.
   
   Args: 
        None
   """
   def __init__(self, *args, **kwargs):
       super(Toolbar, self).__init__(*args, **kwargs)

def draw_figure_w_toolbar(canvas, fig, canvas_toolbar):
    """
    Draw the matplotlib.figure.Figure in the GUI along with the Toolbar

    Args:
         canvas (PySimpleGUI.Windowwindow['fig_cv'].TKCanvas): canvas of the PySimpleGUI.Window
         fig (matplotlib.figure.Figure): the figure to be plotted and then have artist colors adjusted
         canvas_toolbar: (PySimpleGUI.Windowwindow['controls_cv'].TKCanvas): toolbar of the PySimpleGUI.Window

    Returns:
         None
    """
    if canvas.children:
        for child in canvas.winfo_children():
            child.destroy()
    if canvas_toolbar.children:
        for child in canvas_toolbar.winfo_children():
            child.destroy()
    figure_canvas_agg = FigureCanvasTkAgg(fig, master=canvas)
    figure_canvas_agg.draw()
    toolbar = Toolbar(figure_canvas_agg, canvas_toolbar)
    toolbar.update()
    figure_canvas_agg.get_tk_widget().pack(side='right', fill='both', expand=1)
