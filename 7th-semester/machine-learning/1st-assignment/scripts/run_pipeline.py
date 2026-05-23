"""CLI entry point for the bankruptcy classification pipeline."""

from __future__ import annotations

import click


@click.command()
@click.option(
    "--config",
    default="configs/config.yaml",
    help="Path to YAML config.",
    type=click.Path(exists=True),
)
def main(config: str) -> None:
    """Run the corporate bankruptcy classification pipeline."""
    from bankruptcy_clf.pipeline.experiment import ExperimentRunner

    runner = ExperimentRunner(config_path=config)
    results_df = runner.run()
    click.echo(f"\nResults ({len(results_df)} records):")
    click.echo(
        results_df.groupby("Classifier Name")["F1 Score"]
        .mean()
        .sort_values(ascending=False)
        .to_string()
    )


if __name__ == "__main__":
    main()
