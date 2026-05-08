"""Writes pcap analysis results to a structured text file."""

import json
import logging
from dataclasses import asdict
from pathlib import Path

from pcap_analyzer.models import FlowStats, ProtocolStats

logger = logging.getLogger(__name__)


class Reporter:
    """Serialises analysis results to a human-readable JSON-lines file.

    Each section (protocol statistics, TCP flows, UDP flows) is written
    in order, with one JSON object per line for the flow records.
    """

    def write(
        self,
        output_path: Path,
        stats: ProtocolStats,
        tcp_flows: list[FlowStats],
        udp_flows: list[FlowStats],
    ) -> None:
        """Write statistics and per-flow details to *output_path*.

        Args:
            output_path: Destination file path (created or overwritten).
            stats: Protocol-level statistics from the parser.
            tcp_flows: Grouped TCP flow records.
            udp_flows: Grouped UDP flow records.
        """
        logger.info("Writing results to '%s'", output_path)
        summary = {
            "protocol": stats.protocols,
            "count": stats.counts,
            "percentages": stats.percentages,
            "total_count": stats.total_count,
        }

        with open(output_path, "w", encoding="utf-8") as f:
            f.write("Statistics:\n")
            json.dump(summary, f)
            f.write("\n")

            f.write(f"Unique TCP flows: {len(tcp_flows)}\n")
            for flow in tcp_flows:
                json.dump(asdict(flow), f)
                f.write("\n")

            f.write(f"Unique UDP flows: {len(udp_flows)}\n")
            for flow in udp_flows:
                json.dump(asdict(flow), f)
                f.write("\n")

        logger.info("Results written successfully.")
