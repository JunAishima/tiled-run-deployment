import argparse

from prefect.deployments import run_deployment
from tiled.client import from_uri

arg_parser = argparse.ArgumentParser(
    description="Run a Prefect 2 workflow in response to a Kafka message."
)
arg_parser.add_argument("endstation")
arg_parser.add_argument("deployment_name")
args = arg_parser.parse_args()


def on_child_metadata_updated(update):
    print(
        f"Metadata updated, stop_doc: {update.metadata.get('stop')}\
          - run deployment {args.deployment_name}"
    )
    doc = update.metadata.get("stop")
    if doc:
        run_deployment(
            name=args.deployment_name,
            parameters={"stop_doc": doc},
            timeout=0,
        )
    else:
        print(update.metadata["name"])
        pass


def message_to_workflow():
    client = from_uri("https://tiled.nsls2.bnl.gov")
    pt = client[f"{args.endstation}/migration"]
    sub = pt.subscribe()
    sub.child_metadata_updated.add_callback(on_child_metadata_updated)
    print(f"Listening on \
            {args.endstation} for deployment {args.deployment_name}.")
    sub.start()  # block


if __name__ == "__main__":
    message_to_workflow()
