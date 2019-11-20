from snakemake.utils import min_version
min_version("5.3.0")
configfile: "config.yml"

rule all:
    """
    Collect the main outputs of the workflow.
    """
    input:
        "results/counts.csv"

