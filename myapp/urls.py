from django.urls import path

from . import controller

urlpatterns = [
    path("taskList", controller.task_list),
    path("taskNew", controller.task_new),
    path("taskDetail", controller.task_detail),
    path("taskVisualization",controller.task_visualization)
]
