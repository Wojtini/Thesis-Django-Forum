from django.template import loader

from forum.models import CycleThread, Thread
from forum.views.base_view import BaseView


class GraphView(BaseView):
    prerender_template = "components/graph.html"

    def _get_prerender_view(self, *args, **kwargs):
        cycles = CycleThread.objects.all().order_by("id")
        return self.get_rendered_graph(cycles)

    def get_as_component_for_thread(self, thread: Thread):
        cycles = CycleThread.objects.filter(thread=thread).order_by("id")
        return self.get_rendered_graph(cycles)

    def get_rendered_graph(self, cycles):
        graph_colors = [
            'RGBA( 255, 0, 0,   1 )',
        ]
        curr_graph = 0
        x_values_id = list({cyclet.cycle_id for cyclet in cycles})
        x_values = list({cyclet.cycle for cyclet in cycles})
        x_values.sort(key=lambda x: x.id)
        x_values_id.sort()
        data = {}
        for cycle in cycles:
            if cycle.thread not in data:
                data.update({cycle.thread: {}})
            data[cycle.thread].update({cycle.cycle.id: cycle.popularity})

        better_data = {}
        for key, value in data.items():
            better_data[key] = {"y": [], "color": graph_colors[min(curr_graph, len(graph_colors)-1)]}
            better_data[key]["y"] = [
                value[x] if x in value else 0 for x in x_values_id
            ]
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

