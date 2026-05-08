"""Pcap file parsing and network flow grouping."""

import logging
import socket

import dpkt
from dpkt.compat import compat_ord

from pcap_analyzer.models import FlowStats, Packet, ProtocolStats

logger = logging.getLogger(__name__)

_TRACKED_PROTOCOLS: list[str] = ["TCP", "UDP", "ICMP", "ARP"]


def _mac_addr(address: bytes) -> str:
    """Convert a raw MAC address to a colon-separated hex string.

    Args:
        address: Raw MAC address bytes.

    Returns:
        Human-readable MAC string, e.g. ``"01:02:03:04:05:06"``.
    """
    return ":".join(f"{compat_ord(b):02x}" for b in address)


def _inet_to_str(inet: bytes) -> str:
    """Convert a raw inet address to a printable dotted-decimal string.

    Tries IPv4 first and falls back to IPv6.

    Args:
        inet: Raw network-order address bytes.

    Returns:
        Printable IP address string.
    """
    try:
        return socket.inet_ntop(socket.AF_INET, inet)
    except ValueError:
        return socket.inet_ntop(socket.AF_INET6, inet)


class PcapParser:
    """Parses a pcap capture file and groups packets into network flows.

    Args:
        path: Path to the ``.pcap`` file to analyse.
    """

    def __init__(self, path: "Path") -> None:  # noqa: F821 — Path imported in main
        self._path = path
        logger.info("PcapParser initialised for '%s'", path)

    def parse(self) -> ProtocolStats:
        """Read the pcap file and return per-protocol statistics.

        Iterates every Ethernet frame, identifies its transport protocol,
        and builds detailed ``Packet`` records for TCP and UDP traffic.

        Returns:
            A ``ProtocolStats`` instance with counts, percentages, and
            the full lists of TCP and UDP ``Packet`` objects.

        Raises:
            FileNotFoundError: If the pcap file path does not exist.
            dpkt.dpkt.NeedData: If the file is truncated or malformed.
        """
        logger.info("Starting pcap analysis: '%s'", self._path)
        counts: list[int] = [0] * len(_TRACKED_PROTOCOLS)
        tcp_packets: list[Packet] = []
        udp_packets: list[Packet] = []

        with open(self._path, "rb") as f:
            pcap = dpkt.pcap.Reader(f)
            for timestamp, buf in pcap:
                eth = dpkt.ethernet.Ethernet(buf)
                ip = eth.data

                if not isinstance(eth.data, dpkt.ip.IP):
                    if isinstance(ip, dpkt.arp.ARP):
                        counts[_TRACKED_PROTOCOLS.index("ARP")] += 1

                elif ip.p == dpkt.ip.IP_PROTO_TCP:
                    counts[_TRACKED_PROTOCOLS.index("TCP")] += 1
                    tcp = ip.data
                    tcp_packets.append(Packet(
                        timestamp=timestamp,
                        length=len(buf),
                        src_ip=_inet_to_str(ip.src),
                        dst_ip=_inet_to_str(ip.dst),
                        src_port=tcp.sport,
                        dst_port=tcp.dport,
                        protocol=ip.get_proto(ip.p).__name__,
                    ))

                elif ip.p == dpkt.ip.IP_PROTO_UDP:
                    counts[_TRACKED_PROTOCOLS.index("UDP")] += 1
                    udp = ip.data
                    udp_packets.append(Packet(
                        timestamp=timestamp,
                        length=len(buf),
                        src_ip=_inet_to_str(ip.src),
                        dst_ip=_inet_to_str(ip.dst),
                        src_port=udp.sport,
                        dst_port=udp.dport,
                        protocol=ip.get_proto(ip.p).__name__,
                    ))

                elif isinstance(ip.data, dpkt.icmp.ICMP):
                    counts[_TRACKED_PROTOCOLS.index("ICMP")] += 1

        total = sum(counts)
        percentages = [f"{round(c / total * 100, 2)}%" for c in counts]

        logger.info(
            "Parsed %d total packets — TCP: %d  UDP: %d  ICMP: %d  ARP: %d",
            total, counts[0], counts[1], counts[2], counts[3],
        )
        return ProtocolStats(
            protocols=_TRACKED_PROTOCOLS,
            counts=counts,
            percentages=percentages,
            total_count=total,
            tcp_packets=tcp_packets,
            udp_packets=udp_packets,
        )

    @staticmethod
    def group_by_flow(packets: list[Packet]) -> list[FlowStats]:
        """Group packets by their 4-tuple flow and compute per-flow statistics.

        A flow is identified by
        ``(source IP, destination IP, source port, destination port)``.

        Args:
            packets: List of ``Packet`` objects all belonging to the same
                transport protocol.

        Returns:
            A list of ``FlowStats``, one entry per unique flow.
        """
        flow_index: dict[str, list[int]] = {}
        for i, pkt in enumerate(packets):
            flow_index.setdefault(pkt.flow_key, []).append(i)

        flows: list[FlowStats] = []
        for indices in flow_index.values():
            first = packets[indices[0]]
            total_length = sum(packets[i].length for i in indices)
            duration = (
                round(packets[indices[-1]].timestamp - packets[indices[0]].timestamp, 2)
                if len(indices) > 1
                else 0.0
            )
            flows.append(FlowStats(
                duration=duration,
                total_length=total_length,
                src_ip=first.src_ip,
                dst_ip=first.dst_ip,
                src_port=first.src_port,
                dst_port=first.dst_port,
                protocol=first.protocol,
                packet_count=len(indices),
            ))

        logger.info("Identified %d unique flows", len(flows))
        return flows
