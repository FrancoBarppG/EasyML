def generate_plot2d(x_data, y_data, plot_type, plot_name, plot_title, mode1):

    if mode1 == 'markers':
        data = {'x': x_data, 'y': y_data, 'type': plot_type, 'name': plot_name, 'marker': {'size': 15, 'line': {'width': 0.5, 'color': 'white'}, 'opacity': 0.7}, 'mode': mode}
    else:
        data = {'x': x_data, 'y': y_data, 'type': plot_type, 'name': plot_name}

        
    return{'data': [
        data
    ],
    'layout': {
        'title': plot_title
    }
    }

def generate_plot2d_2(x_data, y_data, plot_type, plot_name, plot_title, x_data2, y_data2, plot_type2, plot_name2, mode1, mode2):

    if mode1 == 'markers':
        data1 = {'x': x_data, 'y': y_data, 'type': plot_type, 'name': plot_name, 'marker': {'size': 15, 'line': {'width': 0.5, 'color': 'white'}, 'opacity': 0.7}, 'mode': mode1}
    else:
        data1 = {'x': x_data, 'y': y_data, 'type': plot_type, 'name': plot_name, 'mode': 'lines'}
        
    if mode2 == 'markers':
        data2 = {'x': x_data2, 'y': y_data2, 'type': plot_type2, 'name': plot_name2, 'marker': {'size': 15, 'line': {'width': 0.5, 'color': 'white'}, 'opacity': 0.7}, 'mode': mode2}
    else:
        data2 = {'x': x_data2, 'y': y_data2, 'type': plot_type2, 'name': plot_name2}

    return{'data': [
        data1,
        data2
    ],
    'layout': {
        'title': plot_title,
    }
    }



def generate_plot3d(x_data, y_data, z_data, plot_type, plot_text, marker_data,  plot_name, plot_title):

    return{'data': [
        {'x': x_data, 'y': y_data, 'z': z_data, 'type': plot_type, 'text': plot_text, 'marker': marker_data, 'name': plot_name},
    ],
    'layout': {
        'title': plot_title
    }
    }

def generate_plot3d_2(x_data, y_data, z_data, plot_type, plot_text, marker_data,  plot_name, plot_title, x_data2, y_data2, z_data2, plot_type2, plot_text2, marker_data2,  plot_name2, plot_title2):

    return{'data': [
        {'x': x_data, 'y': y_data, 'z': z_data, 'type': plot_type, 'text': plot_text, 'marker': marker_data, 'name': plot_name},
        {'x': x_data2, 'y': y_data2, 'z': z_data2, 'type': plot_type2, 'text': plot_text2, 'marker': marker_data2, 'name': plot_name2}
    ],
    'layout': {
        'title': plot_title
    }
    }
