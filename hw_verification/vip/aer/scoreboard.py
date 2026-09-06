"""scoreboard.py — Golden Scoreboard verifying Dimension-Order Routing (DOR)."""

from pyuvm import uvm_scoreboard, uvm_tlm_analysis_fifo
from hw_verification.vip.aer.seq_item import AerPacketSeqItem


class AerRouterScoreboard(uvm_scoreboard):
    """Verifies that packets route according to deterministic X-then-Y Dimension-Order Routing."""

    def __init__(self, name: str, parent, curr_x: int = 0, curr_y: int = 0):
        super().__init__(name, parent)
        self.curr_x = curr_x
        self.curr_y = curr_y
        self.total_routed = 0
        self.total_delivered_local = 0
        self.routing_errors = 0

    def predict_egress_port(self, item: AerPacketSeqItem) -> int:
        """Returns expected egress port: 0:Local, 1:North, 2:South, 3:East, 4:West."""
        if item.dst_x > self.curr_x:
            return 3  # East
        elif item.dst_x < self.curr_x:
            return 4  # West
        elif item.dst_y > self.curr_y:
            return 2  # South
        elif item.dst_y < self.curr_y:
            return 1  # North
        else:
            return 0  # Local tile

    def verify_route(self, item: AerPacketSeqItem, actual_port: int):
        expected_port = self.predict_egress_port(item)
        port_names = ["Local", "North", "South", "East", "West"]
        if actual_port != expected_port:
            self.logger.error(
                f"DOR ROUTING MISMATCH: Packet {item} exited via {port_names[actual_port]} "
                f"but expected {port_names[expected_port]} at tile ({self.curr_x}, {self.curr_y})!"
            )
            self.routing_errors += 1
        else:
            self.total_routed += 1
            if actual_port == 0:
                self.total_delivered_local += 1

    def check_phase(self):
        super().check_phase()
        assert self.routing_errors == 0, f"Scoreboard detected {self.routing_errors} DOR routing errors!"
