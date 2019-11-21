from snakemake.utils import min_version
min_version("5.3.0")
configfile: "config.yml"

rule all:
    """
    Collect the main outputs of the workflow.
    """
    input:
        #expand("temp/{substr}.csv", substr = config["dates"])
        expand("results/{substr}_clean.csv", substr = config["dates"]),
        dir = directory("results/final")

rule get_csv_by_url:
    """
    Collect samples CSVs for workflow
    """
    output:
        "temp/{date}.csv"
    log:
        "results/logs/get_csvs/.{date}.log"
    shadow: "minimal"
    params:
        url_path = lambda wildcards: config["surveys"][wildcards.date]
    shell:
        """
        wget {params.url_path} -O {output} -o {log}
        """

rule clean_csvs:
    """
    Clean sample CSVs with clean_csv.py for visualisation
    """
    input:
        "temp/{date}.csv"
    output:
        "results/{date}_clean.csv"
    shell:
        """
        python clean_csv.py {input} {output}
        """

rule make_plot:
    """
    For plotting in markdown document
    """
    input:
        expand("results/{date}_clean.csv", date = config["dates"])
    output:
        directory("results/final")
    shell:
        """
        python plot.py {input} --outdir {output}
        """