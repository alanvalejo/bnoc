#!/usr/bin/env python
# -*- coding: utf-8 -*-

import igraph
import os
import numpy
import random
import inspect
import math

from colour import Color

import models.args as args
import models.helper as helper
import models.helperigraph as helperigraph
# import models.helpermgraph as helpermgraph
# from models.timing import Timing
# from models.similarity import Similarity

def build_layout(graph, options):
    coords = []
    w = 0.6 * min(numpy.asarray(options.bbox))
    r = 0.8 * w / 2
    n = len(options.vertices)

    teta = numpy.linspace(-math.pi / 2, 2 * math.pi - math.pi / 2, num=n + 1)
    p = [numpy.asarray([r * math.cos(t), r * math.sin(t)] ) for t in teta]

    for layer in range(n):
        p0 = p[layer]
        p1 = p[layer + 1]
        ni = options.vertices[layer]
        vec = p1 - p0
        s = 0.4 / (ni - 1)
        ci = [p0 + (0.3 + s * i) * vec for i in range(ni)]
        coords += ci

    layout = igraph.Layout(coords)

    return layout

def plot_network(graph, options):

    graph.vs['vertex_color'] = 'black'
    vertex_color = graph.vs['vertex_color']
    if options.membership is not None:
        colors = []

        if options.color is None:
            if options.eq_color:
                for i in range(0, max(options.comms) + 1):
                    colors.append('#' + '%06X' % random.randint(0, 0xFFFFFF))
                with open(options.output + '.color', 'w+') as f:
                    f.write('\n'.join(colors))
            else:
                for i in range(0, sum(options.comms) + 1):
                    colors.append('#' + '%06X' % random.randint(0, 0xFFFFFF))
                with open(options.output + '.color', 'w+') as f:
                    f.write('\n'.join(colors))
        else:
            with open(options.color, 'r') as f:
                for index, line in enumerate(f):
                    colors.append(line.strip())

        for layer in range(graph['layers']):
            vertices = graph.vs.select(type=layer)['index']

            for vertex in vertices:
                member = next(iter(graph.vs[vertex]['membership']))
                if options.eq_color:
                    vertex_color[vertex] = colors[member]
                else:
                    vertex_color[vertex] = colors[member + sum(options.comms[:layer])]

        graph.vs['vertex_color'] = vertex_color

    if options.black:
        graph.vs['vertex_color'] = 'black'

    old_min, old_max = min(graph.es['weight']), max(graph.es['weight'])
    bondary_edges, edge_opacity, edge_width = ([] for i in range(3))
    for edge in graph.es():
        w = helper.remap(edge['weight'], old_min, old_max, options.weight_min, options.weight_max)
        if w is None:
            w = 0.5
        edge_width.append(w)
        opacity = helper.remap(edge['weight'], old_min, old_max, options.opacity_min, options.opacity_max)
        if opacity is None:
            opacity = 0.2
        if graph.vs[edge.tuple[0]]['vertex_color'] != graph.vs[edge.tuple[1]]['vertex_color']:
            bondary_edges.append(edge)
            edge_opacity.append("rgba(1,1,1," + str(opacity) + ")")
        else:
            edge_opacity.append("rgba(1,1,1," + str(opacity) + ")")

    graph.es['width'] = edge_width
    graph.es['opacity'] = edge_opacity
    graph.vs['vertex_size'] = options.vertex_size

    if options.degree is True:
        weight = graph.strength(weights='weight')
        old_min, old_max = min(weight), max(weight)
        for index, w in enumerate(weight):
            weight[index] = helper.remap(w, old_min, old_max, options.vertex_min, options.vertex_max)
        graph.vs['vertex_size'] = weight

    if options.weight is not None:
        weight = options.weight.copy()
        old_min, old_max = min(weight), max(weight)
        for index, w in enumerate(weight):
            weight[index] = helper.remap(w, old_min, old_max, options.vertex_min, options.vertex_max)
            if math.isnan(weight[index]):
                print('Warning: Vertex size with NaN value.')
                weight[index] = 1
        graph.vs['vertex_size'] = weight

    graph.vs['vertex_shape'] = graph.vcount() * ['circle']
    graph.vs['vertex_frame_color'] = str(options.vertex_frame_color)
    graph.vs['vertex_frame_width'] = options.vertex_frame_width
    types = ['rectangle', 'circle', 'triangle-up', 'triangle-down']
    while len(types) < 10:
        types += types
    if options.layout_name in ['kk', 'fr', 'heterogeneous']:
        for layer in range(graph['layers']):
            vertices = graph.vs.select(type=layer)['index']
            for vertex in vertices:
                graph.vs[vertex]['vertex_shape'] = types[layer]

    if options.overlapping is not None and options.overlapping_paint:
        graph.vs[options.overlapping]['vertex_color'] = str(options.overlapping_color)
        graph.vs[options.overlapping]['vertex_frame_color'] = str(options.vertex_frame_color)
        graph.vs[options.overlapping]['vertex_shape'] = str(options.overlapping_shape)

    if options.coloring_degree:
        unique_degrees = list(numpy.unique(graph.strength()))
        blue = Color("#000000")
        red = Color("#c10000")
        colors = list(blue.range_to(red, len(unique_degrees)))
        color_list = [str(colors[unique_degrees.index(degree)]) for degree in graph.strength()]
        graph.vs['vertex_color'] = color_list

    if options.coloring_weight:
        unique_weights = list(numpy.unique(options.weight))
        blue = Color("#000000")
        red = Color("#c10000")
        colors = list(blue.range_to(red, len(unique_weights)))
        color_list = [str(colors[unique_weights.index(weight)]) for weight in options.weight]
        graph.vs['vertex_color'] = color_list

    if options.delete_weight_le:
        for weight in options.delete_weight_le:
            graph.es.select(weight_le=weight).delete()

    # remove isolated vertices
    if options.delete_degree:
        for degree in options.delete_degree:
            graph.vs.select(_degree=degree).delete()

    visual_style = {}
    visual_style['edge_label'] = None
    visual_style['edge_color'] = graph.es['opacity']
    visual_style['edge_width'] = graph.es['width']
    if options.curved:
        visual_style["edge_curved"] = 0.4

    visual_style['vertex_shape'] = graph.vs['vertex_shape']
    visual_style['vertex_size'] = graph.vs['vertex_size']
    visual_style['vertex_color'] = graph.vs['vertex_color']
    visual_style['vertex_label_dist'] = [3] * graph['vertices'][0] + [-3] * graph['vertices'][1]
    visual_style['vertex_frame_color'] = graph.vs['vertex_frame_color']
    visual_style['vertex_frame_width'] = graph.vs['vertex_frame_width']

    if options.layout is None:
        gcopy = graph.copy()
        if options.layout_name == 'fr':
            gcopy.delete_edges(bondary_edges)
            visual_style['layout'] = gcopy.layout(options.layout_name, weights='width')
        elif options.layout_name == 'bipartite':
            visual_style['layout'] = gcopy.layout(options.layout_name, hgap=500, vgap=500)
        elif options.layout_name == 'kk':
            gcopy.delete_edges(bondary_edges)
            visual_style['layout'] = gcopy.layout(options.layout_name)
        elif options.layout_name == 'heterogeneous':
            gcopy.delete_edges(bondary_edges)
            visual_style['layout'] = build_layout(graph, options)
            edge_curved = []
            for edge in graph.es():
                u, v = edge.tuple
                type_u, type_v = graph.vs['type'][u], graph.vs['type'][v]
                edge_curved.append(0.2 if type_u != type_v else -2.0)
            visual_style['edge_curved'] = edge_curved
        with open(options.output + '.layout', 'w+') as f:
            for xy in visual_style['layout']:
                f.write(str(xy[0]) + ',' + str(xy[1]) + '\n')
    else:
        array = []
        with open(options.layout, 'r') as f:
            for line in f:
                item = map(float, line.strip().split(','))
                array.append([item[0], item[1]])
        visual_style['layout'] = array

    visual_style['bbox'] = options.bbox
    visual_style['margin'] = options.margin
    visual_style['edge_order_by'] = ('weight', 'asc')

    if options.save_pdf:
        igraph.plot(graph, options.output + '.pdf', **visual_style)
        if options.img_roteted:
            helper.rotate_pdf(options.output)
        if options.img_trim:
            command = 'pdfcrop ' + options.output + '.pdf ' + options.output + '.pdf'
            os.system(command)

    if options.save_png:
        igraph.plot(graph, options.output + '.png', **visual_style)
        if options.img_trim:
            command = 'convert ' + options.output + '.png -trim ' + options.output + '.png'
            os.system(command)
        if options.img_roteted:
            helper.rotate_png(options.output)
    if options.show:
        igraph.plot(graph, **visual_style)

if __name__ == '__main__':

    # Setup parse options command line
    current_path = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
    parser = args.setup_parser(current_path + '/args/pynetviewer.json')
    options = parser.parse_args()
    args.update_json(options)
    args.check_output(options)

    # Check required fields
    if options.input is None:
        parser.error('required -f [input] arg.')
    if options.vertices is None:
        parser.error('required -v [number of vertices for each layer] arg.')

    # Create graph
    graph = helperigraph.load(options.input, options.vertices, type_filename=options.type_file)

    # Create membership and overlaping lists
    options.comms = [0] * graph['layers']
    options.overlapping = []
    if options.membership:
        with open(options.membership, 'r') as f:
            for vertex, comms in enumerate(f):
                members = set(map(int, comms.split()))
                if len(members) > 1:
                    options.overlapping.append(vertex)
                graph.vs[vertex]['membership'] = members
        options.membership = numpy.array(graph.vs['membership'])
        for layer in range(graph['layers']):
            vertices = graph.vs.select(type=layer)['index']
            options.comms[layer] = max(list(set().union(*options.membership[vertices]))) + 1

    if options.community_detection:
        if options.community_detection == "fastgreedy":

            cl = graph.community_fastgreedy(weights='weight')
            membership = cl.as_clustering(options.k).membership
            for vertex, members in enumerate(membership):
                graph.vs[vertex]['membership'] = set([members])
            options.membership = numpy.array(membership)
            options.comms = [options.k, options.k]
        else:
            parser.error('There are no ' + str(options.community_detection) + ' algorithm.')

    if options.weight:
        options.weight = numpy.loadtxt(options.weight)

    # Plot
    plot_network(graph, options)
