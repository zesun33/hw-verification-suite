"""hw_verification.vip.aer — Address-Event Representation (AER) VIP package."""

from hw_verification.vip.aer.seq_item import AerPacketSeqItem
from hw_verification.vip.aer.scoreboard import AerRouterScoreboard
from hw_verification.vip.aer.coverage import sample_aer_coverage, get_aer_coverage_summary

__all__ = [
    "AerPacketSeqItem",
    "AerRouterScoreboard",
    "sample_aer_coverage",
    "get_aer_coverage_summary",
]
