#!/usr/bin/env python
"""
Download from W&B the raw dataset and apply some basic data cleaning, exporting the result to a new artifact
"""
import argparse
import logging
import wandb
import pandas as pd


logging.basicConfig(level=logging.INFO, format="%(asctime)-15s %(message)s")
logger = logging.getLogger()

def go(args):

    run = wandb.init(job_type="basic_cleaning")
    run.config.update(args)

    # Download input artifact. This will also log that this script is using this
    # particular version of the artifact
    # artifact_local_path = run.use_artifact(args.input_artifact).file()

    ######################
    # YOUR CODE HERE     #
    ######################
    logger.info("Starting Basic Cleaning Component")
    artifact_local_path = run.use_artifact(args.input_artifact).file()
    logger.info("Artifact downloaded")

    # Reading the artifact_local_path
    df = pd.read_csv(artifact_local_path)

    # Dropping the outliers
    min_price = args.min_price
    max_price = args.max_price
    idx = df['price'].between(min_price, max_price)
    df = df[idx].copy()
    logger.info("Outliers fixed")
    
    # Convert last_review to datetime
    df['last_review'] = pd.to_datetime(df['last_review'])
    
    idx = df['longitude'].between(-74.25, -73.50) & df['latitude'].between(40.5, 41.2)
    df = df[idx].copy()

    filename = args.output_artifact
    df.to_csv(filename, index=False)

    artifact = wandb.Artifact(
        name=args.output_artifact,
        type=args.output_type,
        description=args.output_description,
    )
    artifact.add_file(filename)

    logger.info("Logging artifact")
    run.log_artifact(artifact)


if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="A very basic data cleaning")


    parser.add_argument(
        "--input_artifact", 
        type=str,## INSERT TYPE HERE: str, float or int,
        help="Artfact input name, e.g: sample.csv:latest",## INSERT DESCRIPTION HERE,
        required=True
    )

    parser.add_argument(
        "--output_artifact", 
        type=str,## INSERT TYPE HERE: str, float or int,
        help="Artfact output name, e.g: clean_sample.csv",## INSERT DESCRIPTION HERE,
        required=True
    )

    parser.add_argument(
        "--output_type", 
        type=str,## INSERT TYPE HERE: str, float or int,
        help="component output type",## INSERT DESCRIPTION HERE,
        required=True
    )

    parser.add_argument(
        "--output_description", 
        type=str,## INSERT TYPE HERE: str, float or int,
        help="component output description",## INSERT DESCRIPTION HERE,
        required=True
    )

    parser.add_argument(
        "--min_price", 
        type=int,## INSERT TYPE HERE: str, float or int,
        help="minimum price value",## INSERT DESCRIPTION HERE,
        required=True
    )

    parser.add_argument(
        "--max_price", 
        type=int,## INSERT TYPE HERE: str, float or int,
        help="maximum price value",## INSERT DESCRIPTION HERE,
        required=True
    )


    args = parser.parse_args()

    go(args)
