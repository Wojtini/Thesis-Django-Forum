from django.template import loader

from forum.models import CycleThread
from forum.views.base_view import BaseView


class GraphView(BaseView):
    prerender_template = "components/graph.html"

    def _get_prerender_view(self, *args, **kwargs):
        graph_colors = [
            'RGBA( 0, 0, 255,   1 )',
            'RGBA( 127, 255, 0, 1 )',
            'RGBA( 220, 20, 60, 1 )',
            'RGBA( 0, 100, 0,   1 )',
            'RGBA( 255, 140, 0, 1 )',
            'RGBA( 0, 255, 255, 1 )',
        ]
        curr_graph = 0

        cycles = CycleThread.objects.all().order_by("id")
        data = {}
        x_values_id = list({cyclet.cycle_id for cyclet in cycles})
        x_values = list({cyclet.cycle for cyclet in cycles})
        x_values.sort(key=lambda x: x.id)
        x_values_id.sort()
        for cycle in cycles:
            if cycle.thread not in data:
                data.update({cycle.thread: {}})
            data[cycle.thread].update({cycle.cycle.id: cycle.popularity})

        better_data = {}
        for key, value in data.items():
            better_data[key] = {"y": [], "color": graph_colors[min(curr_graph, len(graph_colors)-1)]}
            for x in x_values_id:
                if x in value:
                    better_data[key]["y"].append(value[x])
                else:
                    better_data[key]["y"].append(0)
            curr_graph += 1
            better_data[key]["y"] = str(better_data[key]["y"])
        x_values = [
            x.date.strftime("%m/%d/%Y, %H:%M:%S")
            for x in x_values
        ]
        return loader.render_to_string(
            self.prerender_template,
            context={
                "data": better_data,
                "x_values": str(x_values)
            },
        )
