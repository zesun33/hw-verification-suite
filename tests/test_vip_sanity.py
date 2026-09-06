"""test_vip_sanity.py — Unit Sanity Verification for Centralized VIP Library."""

from hw_verification.vip.common.poisson import PoissonSpikeGenerator
from hw_verification.vip.common.sva import TemporalAssertionChecker
from hw_verification.vip.aer.seq_item import AerPacketSeqItem
from hw_verification.vip.aer.scoreboard import AerRouterScoreboard


def test_poisson_generator_statistics():
    """Verify Poisson spike vector generator sparsity bounds."""
    gen = PoissonSpikeGenerator(num_channels=8, seed=1234)
    sweep = gen.generate_sweep(num_timesteps=100, min_rate=0.10, max_rate=0.90)
    assert len(sweep) == 100
    # First 10 should have low density, last 10 high density
    early_density = sum(bin(x).count("1") for x in sweep[:10]) / (10 * 8)
    late_density = sum(bin(x).count("1") for x in sweep[-10:]) / (10 * 8)
    assert early_density < 0.35
    assert late_density > 0.65


def test_aer_packet_codec():
    """Verify 16-bit encoding and decoding of AER packets."""
    pkt = AerPacketSeqItem(src_x=1, src_y=2, dst_x=3, dst_y=4, axon_id=7)
    enc = pkt.encode_16bit()
    dec = AerPacketSeqItem.decode_16bit(enc)
    assert dec.src_x == 1
    assert dec.src_y == 2
    assert dec.dst_x == 3
    assert dec.dst_y == 4
    assert dec.axon_id == 7


def test_dor_routing_prediction():
    """Verify Dimension-Order Routing (DOR: X then Y) path prediction."""
    # Current tile is at (1, 1)
    sb = AerRouterScoreboard("sb", None, curr_x=1, curr_y=1)

    # 1. Packet to (2, 1) must route East (port 3)
    p_east = AerPacketSeqItem(dst_x=2, dst_y=1)
    assert sb.predict_egress_port(p_east) == 3

    # 2. Packet to (0, 1) must route West (port 4)
    p_west = AerPacketSeqItem(dst_x=0, dst_y=1)
    assert sb.predict_egress_port(p_west) == 4

    # 3. Packet to (1, 2) must route South (port 2)
    p_south = AerPacketSeqItem(dst_x=1, dst_y=2)
    assert sb.predict_egress_port(p_south) == 2

    # 4. Packet to (1, 0) must route North (port 1)
    p_north = AerPacketSeqItem(dst_x=1, dst_y=0)
    assert sb.predict_egress_port(p_north) == 1

    # 5. Packet to (1, 1) must route to Local Tile (port 0)
    p_local = AerPacketSeqItem(dst_x=1, dst_y=1)
    assert sb.predict_egress_port(p_local) == 0


def test_temporal_sva_checker():
    """Verify non-overlapping temporal implication checker."""
    sva = TemporalAssertionChecker("test_in_refractory_no_spike")
    # Cycle 0: in_refractory=True, spike=False -> OK
    sva.check_implication(antecedent_t0=True, consequent_t1=True)
    # Cycle 1: in_refractory=True, spike=True -> Violation!
    sva.check_implication(antecedent_t0=True, consequent_t1=False, msg="Spike occurred while refractory")
    assert sva.violations == 1
