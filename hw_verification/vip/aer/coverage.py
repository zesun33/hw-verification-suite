"""coverage.py — Functional Cross-Coverage for 2D Mesh AER NoC Routing."""

from cocotb_coverage.coverage import CoverPoint, CoverCross, coverage_db


@CoverPoint("aer_cov.dst_x", xf=lambda item: item.dst_x, bins=[0, 1, 2, 3])
@CoverPoint("aer_cov.dst_y", xf=lambda item: item.dst_y, bins=[0, 1, 2, 3])
@CoverPoint("aer_cov.axon_id", xf=lambda item: item.axon_id, bins=list(range(8)))
@CoverPoint("aer_cov.ingress_port", xf=lambda item: item.port_ingress, bins=[0, 1, 2, 3, 4])
@CoverCross("aer_cov.mesh_destination_2d", items=["aer_cov.dst_x", "aer_cov.dst_y"])
def sample_aer_coverage(item):
    """Samples AER transaction into 2D mesh spatial coverage model."""
    pass


def get_aer_coverage_summary():
    """Returns dictionary of functional coverage percentages."""
    details = {}
    for name in [
        "aer_cov.dst_x",
        "aer_cov.dst_y",
        "aer_cov.axon_id",
        "aer_cov.ingress_port",
        "aer_cov.mesh_destination_2d"
    ]:
        cov_obj = coverage_db.get(name)
        if cov_obj is not None:
            details[name] = cov_obj.cover_percentage
        else:
            details[name] = 0.0
    return details
