import pytest
from parchmint.component import Component
from parchmint.port import Port
from tests.conftest import comp1

from fluigi.pnr.sfc.primitivecell import ComponentSide
from fluigi.pnr.sfc.utils import get_closest_side, to_polar


@pytest.fixture
def cardinal_ports():
    # Create Ports
    port_north = Port("north", x=500, y=0)
    port_south = Port("south", x=500, y=1000)
    port_east = Port("east", x=1000, y=500)
    port_west = Port("west", x=0, y=500)

    return [port_north, port_south, port_east, port_west]


@pytest.fixture
def diagonal_ports():
    # TODO add more port on the diagnals and in the middle
    port_middle = Port("middle", x=500, y=500)

    port_northeast_corner = Port("northeast_corner", x=1000, y=0)
    port_southeast_corner = Port("southeast_corner", x=1000, y=1000)
    port_southwest_corner = Port("southwest_corner", x=0, y=1000)
    port_northwest_corner = Port("northwest_corner", x=0, y=0)

    return [port_middle, port_northeast_corner, port_southeast_corner, port_southwest_corner, port_northwest_corner]


def test_to_polar(component, cardinal_ports, diagonal_ports):
    # Extract the ports
    port_north, port_south, port_east, port_west = cardinal_ports
    (
        port_middle,
        port_northeast_corner,
        port_southeast_corner,
        port_southwest_corner,
        port_northwest_corner,
    ) = diagonal_ports

    # Test the function
    assert to_polar((0, 0, component.xspan, component.yspan), (port_north.x, port_north.y)) == (500.0, 90.0)
    assert to_polar((0, 0, component.xspan, component.yspan), (port_south.x, port_south.y)) == (500.0, -90.0)
    assert to_polar((0, 0, component.xspan, component.yspan), (port_east.x, port_east.y)) == (500.0, 0.0)
    assert to_polar((0, 0, component.xspan, component.yspan), (port_west.x, port_west.y)) == (500.0, 180.0)

    # TEST the diagnals
    # assert to_polar((0, 0, component.xspan, component.yspan), (port_middle.x, port_middle.y)) == (707.1067811865476, 45.0)
    assert to_polar((0, 0, component.xspan, component.yspan), (port_northeast_corner.x, port_northeast_corner.y)) == (
        707.1067811865476,
        45.0,
    )
    assert to_polar((0, 0, component.xspan, component.yspan), (port_southeast_corner.x, port_southeast_corner.y)) == (
        707.1067811865476,
        -45.0,
    )
    assert to_polar((0, 0, component.xspan, component.yspan), (port_southwest_corner.x, port_southwest_corner.y)) == (
        707.1067811865476,
        -135.0,
    )
    assert to_polar((0, 0, component.xspan, component.yspan), (port_northwest_corner.x, port_northwest_corner.y)) == (
        707.1067811865476,
        135.0,
    )


def test_get_closest_side(component, cardinal_ports, diagonal_ports, comp1: Component):
    # Extract the ports
    port_north, port_south, port_east, port_west = cardinal_ports
    (
        port_middle,
        port_northeast_corner,
        port_southeast_corner,
        port_southwest_corner,
        port_northwest_corner,
    ) = diagonal_ports

    # Test the function
    assert get_closest_side(component, port_north) == ComponentSide.NORTH
    assert get_closest_side(component, port_south) == ComponentSide.SOUTH
    assert get_closest_side(component, port_east) == ComponentSide.EAST
    assert get_closest_side(component, port_west) == ComponentSide.WEST
    assert get_closest_side(component, port_middle) is None

    assert get_closest_side(component, port_northeast_corner) == ComponentSide.NORTH
    assert get_closest_side(component, port_southeast_corner) == ComponentSide.EAST
    assert get_closest_side(component, port_southwest_corner) == ComponentSide.SOUTH
    assert get_closest_side(component, port_northwest_corner) == ComponentSide.WEST

    # Test the comp1 definition
    # The ports should be in the following sides:
    # 1 - NORTH
    # 2 - EAST
    # 3 - EAST
    # 4 - EAST
    # 5 - SOUTH
    # 6 - WEST
    # 7 - WEST

    assert get_closest_side(comp1, comp1.ports[0]) == ComponentSide.NORTH
    assert get_closest_side(comp1, comp1.ports[1]) == ComponentSide.EAST
    assert get_closest_side(comp1, comp1.ports[2]) == ComponentSide.EAST
    assert get_closest_side(comp1, comp1.ports[3]) == ComponentSide.EAST
    assert get_closest_side(comp1, comp1.ports[4]) == ComponentSide.SOUTH
    assert get_closest_side(comp1, comp1.ports[5]) == ComponentSide.WEST
    assert get_closest_side(comp1, comp1.ports[6]) == ComponentSide.WEST
