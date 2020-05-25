from django.db import models


class Dashboard(models.Model):
    last_update = models.DateTimeField()


class Chart(models.Model):
    title = models.CharField(max_length=255)
    chart_type = models.CharField(max_length=255)
    data_json = models.TextField()
    dashboard = models.ForeignKey(Dashboard, on_delete=models.CASCADE)
