"""Entry point for the pcap network traffic analyser."""

import argparse
import logging
import sys
import time
from pathlib import Path

from pcap_analyzer.parser import PcapParser
from pcap_analyzer.reporter import Reporter

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)


def _build_arg_parser() -> argparse.ArgumentParser:
    """Build and return the CLI argument parser."""
    parser = argparse.ArgumentParser(
        description="Analyse a pcap network capture file and report protocol and flow statistics."
    )
    parser.add_argument("pcap_file", type=Path, help="Path to the .pcap capture file")
    parser.add_argument(
        "-o", "--output",
        type=Path,
        default=Path("result.txt"),
        help="Output file path (default: result.txt)",
    )
    return parser


def main() -> None:
    """Parse CLI arguments, run pcap analysis, and write results."""
    args = _build_arg_parser().parse_args()
    pcap_path: Path = args.pcap_file

    if not pcap_path.exists():
        logger.error("File not found: %s", pcap_path)
        sys.exit(1)

    start = time.monotonic()

    # Part I — parse pcap, collect per-protocol statistics
    parser = PcapParser(pcap_path)
    stats = parser.parse()

    # Part II — group TCP and UDP packets into flows
    tcp_flows = PcapParser.group_by_flow(stats.tcp_packets)
    udp_flows = PcapParser.group_by_flow(stats.udp_packets)

    # Part III — write statistics and flow details to output file
    Reporter().write(args.output, stats, tcp_flows, udp_flows)

    elapsed_minutes = (time.monotonic() - start) / 60
    logger.info("Execution time: %.2f minutes.", elapsed_minutes)


if __name__ == "__main__":
    main()
