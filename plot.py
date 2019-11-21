#!/usr/bin/env python

import matplotlib as mpl
import matplotlib.pyplot as plt
plt.style.use('ggplot')
mpl.use('agg')
import pandas as pd
import seaborn as sns
import numpy as np
from argparse import ArgumentParser

def read_files(files):
    """Reads experience counts and concatenates into one dataframe"""
    df = pd.DataFrame()
    for i, f in enumerate(files):
        # Extract date
        d = f.split(".")[0]
        _df = pd.read_csv(f, sep=",", header=0)
        # Assign date
        _df = _df.assign(Date=pd.Series([d]*len(_df), index=_df.index))
        if i==0:
            df = _df.copy()
        else:
            df = pd.concat([df,_df], sort=True)
    return df.reset_index().drop("index",axis=1).fillna(0)

def count_experience(df, normalize=False):
    """Generates long format dataframe of counts"""
    df_l = pd.DataFrame()
    for software in df.columns:
        if software=="Date":
            continue
        # Groupby software and count
        _df = df.groupby(["Date",software]).count().iloc[:,0].reset_index()
        _df.columns = ["Date","Experience","Count"]
        _df = _df.assign(Software=pd.Series([software]*len(_df), index=_df.index))
        if normalize:
            _df = pd.merge(_df.groupby("Date").sum().rename(columns={'Count':'Tot'}),_df, left_index=True, right_on="Date")
            _df.Count = _df.Count.div(_df.Tot)*100
            _df.rename(columns={'Count': '%'}, inplace=True)
        df_l = pd.concat([df_l, _df], sort=True)
    df_l.loc[df_l.Experience==0,"Experience"] = np.nan
    return df_l


def plot_catplot(df, outdir, figname, y, palette="Blues"):
    """Plot barplots of user experience per software"""
    ax = sns.catplot(data=df, x="Date", col="Software", col_wrap=3, y=y, hue="Experience", height=2.8,
                     kind="bar",
                     hue_order=["Never heard of it", "Heard of it but haven't used it", "Tried it once or twice",
                                "Use it"],
                     col_order=["Conda", "Git", "Snakemake", "Jupyter", "RMarkdown", "Docker", "Singularity"],
                     palette=palette)
    ax.set_titles("{col_name}")
    plt.savefig("{}/{}".format(outdir, figname), bbox_to_inches="tight", dpi=300)
    plt.close()

def plot_barplot(df, outdir, figname, x):
    """Plot a barplot summarizing user experience over all software"""
    ax = sns.barplot(data=df, hue="Date", y="Experience", x=x, errwidth=.5,
                order=["Never heard of it", "Heard of it but haven't used it", "Tried it once or twice", "Use it"])
    plt.savefig("{}/{}".format(outdir, figname), bbox_inches="tight", dpi=300)
    plt.close()

def main(args):
    # Read all csv files
    df = read_files(args.files)
    # Count experience
    df_l = count_experience(df)
    # Count and normalize experience
    df_lp = count_experience(df, normalize=True)
    # Plot catplot of student experience
    plot_catplot(df_l, args.outdir, "exp_counts.png", y="Count")
    # Plot catplot of student experience in %
    plot_catplot(df_lp, args.outdir, "exp_percent.png", y="%", palette="Reds")
    # Plot barplot of experience
    plot_barplot(df_lp, args.outdir, "exp_barplot.png", x="%")

if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument("files", nargs="+",
                        help="CSV files with student experience to produce plots for")
    parser.add_argument("--outdir", type=str, default=".",
                        help="Output directory for plots (defaults to current directory)")
    args = parser.parse_args()
    main(args)
