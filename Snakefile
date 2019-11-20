from snakemake.utils import min_version
min_version("5.3.0")
configfile: "config.yml"

rule all:
    """
    Collect the main outputs of the workflow.
    """
    input:
        expand("results/{substr}.csv", substr = config["dates"])


rule get_csv_by_url:
    """
    Collect samples CSVs for workflow
    """
    output:
        "results/{date}.csv"
    log:
        "results/logs/get_csvs/.{date}.log"
    params:
        url_path = lambda wildcards: config["surveys"][wildcards.date]
    shell:
        """
        wget {params.url_path} -O {output} -o {log}
        """

