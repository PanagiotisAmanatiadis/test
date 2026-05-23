"""CLI entry point for the diabetes regression pipeline."""

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
    """Run the diabetes progression regression pipeline."""
    from diabetes_reg.pipeline.experiment import ExperimentRunner

    runner = ExperimentRunner(config_path=config)
    results_df = runner.run()
    click.echo(f"\nResults ({len(results_df)} records).")


if __name__ == "__main__":
    main()
