"""seq_item.py — Address Event Representation (AER) Packet Sequence Item."""

from pyuvm import uvm_sequence_item


class AerPacketSeqItem(uvm_sequence_item):
    """Transaction representing a discrete spiking event routed across the 2D NoC mesh."""

    def __init__(
        self,
        name: str = "AerPacketSeqItem",
        src_x: int = 0,
        src_y: int = 0,
        dst_x: int = 0,
        dst_y: int = 0,
        axon_id: int = 0,
        port_ingress: int = 0  # 0: Local, 1: N, 2: S, 3: E, 4: W
    ):
        super().__init__(name)
        self.src_x = src_x
        self.src_y = src_y
        self.dst_x = dst_x
        self.dst_y = dst_y
        self.axon_id = axon_id
        self.port_ingress = port_ingress
        self.timestamp = 0

    def encode_16bit(self) -> int:
        """Encodes {valid[15], dst_x[14:12], dst_y[11:9], axon_id[8:6], src_x[5:3], src_y[2:0]}."""
        return (
            (1 << 15) |
            ((self.dst_x & 0x7) << 12) |
            ((self.dst_y & 0x7) << 9) |
            ((self.axon_id & 0x7) << 6) |
            ((self.src_x & 0x7) << 3) |
            (self.src_y & 0x7)
        )

    @staticmethod
    def decode_16bit(val: int) -> "AerPacketSeqItem":
        item = AerPacketSeqItem("decoded_aer")
        item.dst_x = (val >> 12) & 0x7
        item.dst_y = (val >> 9) & 0x7
        item.axon_id = (val >> 6) & 0x7
        item.src_x = (val >> 3) & 0x7
        item.src_y = val & 0x7
        return item

    def __str__(self):
        return f"AER[{self.src_x},{self.src_y} -> {self.dst_x},{self.dst_y} | Axon={self.axon_id}]"
