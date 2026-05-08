"""Data models for pcap network traffic analysis."""

from dataclasses import dataclass, field


@dataclass
class Packet:
    """Represents a single captured network packet.

    Attributes:
        timestamp: Unix timestamp of packet capture.
        length: Total byte length of the packet.
        src_ip: Source IP address string.
        dst_ip: Destination IP address string.
        src_port: Source transport-layer port.
        dst_port: Destination transport-layer port.
        protocol: Protocol name (e.g. ``"TCP"``, ``"UDP"``).
    """

    timestamp: float
    length: int
    src_ip: str
    dst_ip: str
    src_port: int
    dst_port: int
    protocol: str

    @property
    def flow_key(self) -> str:
        """Return a string key that uniquely identifies this packet's flow."""
        return f"{self.src_ip}{self.dst_ip}{self.src_port}{self.dst_port}"


@dataclass
class FlowStats:
    """Aggregated statistics for a single network flow.

    A flow is defined by the 4-tuple
    (source IP, destination IP, source port, destination port).

    Attributes:
        duration: Flow duration in seconds (last timestamp minus first).
        total_length: Sum of byte lengths of all packets in the flow.
        src_ip: Source IP address of the flow.
        dst_ip: Destination IP address of the flow.
        src_port: Source port of the flow.
        dst_port: Destination port of the flow.
        protocol: Transport protocol name.
        packet_count: Number of packets belonging to this flow.
    """

    duration: float
    total_length: int
    src_ip: str
    dst_ip: str
    src_port: int
    dst_port: int
    protocol: str
    packet_count: int


@dataclass
class ProtocolStats:
    """Per-protocol frequency statistics extracted from a pcap file.

    Attributes:
        protocols: Ordered list of tracked protocol names.
        counts: Absolute packet count for each protocol (same order).
        percentages: Relative frequency strings (e.g. ``"42.5%"``).
        total_count: Total number of packets matched to a tracked protocol.
        tcp_packets: All parsed TCP packets (populated by the parser).
        udp_packets: All parsed UDP packets (populated by the parser).
    """

    protocols: list[str]
    counts: list[int]
    percentages: list[str]
    total_count: int
    tcp_packets: list[Packet] = field(default_factory=list)
    udp_packets: list[Packet] = field(default_factory=list)
