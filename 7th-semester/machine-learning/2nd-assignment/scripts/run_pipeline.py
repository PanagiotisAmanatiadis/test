"""CLI entry point for the Fashion-MNIST clustering pipeline."""

from __future__ import annotations

import click


@click.command()
@click.option(
    "--config",
    default="configs/config.yaml",
    help="Path to the YAML configuration file.",
    type=click.Path(exists=True),
)
def main(config: str) -> None:
    """Run the Fashion-MNIST dimensionality reduction & clustering pipeline."""
    from fashion_clustering.pipeline.experiment import ExperimentRunner

    runner = ExperimentRunner(config_path=config)
    results_df = runner.run()
    click.echo(f"\nResults ({len(results_df)} experiments):")
    click.echo(results_df.to_string(index=False))


if __name__ == "__main__":
    main()
