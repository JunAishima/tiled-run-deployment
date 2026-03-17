tiled-run-deployment
====================

Replace the Kafka-based system used to run deployments as found in https://github.com/nsls2/nslsii-kafka. Uses Tiled websockets instead.
* Requires use of SQL for the endstation/beamline as this provides the websocket capability
* Requires that the Tiled catalog have the name with the format `<endstation>/migration`

Example usage:

```bash
pixi run python consumer.py cms end-of-run-workflow/tst-end-of-run-workflow-docker False
```
