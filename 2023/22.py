import copy
import dataclasses
import inspect
import os

cwd = os.path.dirname(os.path.abspath(inspect.stack()[0][1]))

with open(os.path.join(cwd, "input"), "r") as f:
    bricks = [brick.split("~") for brick in f.read().splitlines()]


@dataclasses.dataclass
class Vector3:
    x: int
    y: int
    z: int

    def __sub__(self, other):
        assert isinstance(other, Vector3)
        return Vector3(self.x - other.x, self.y - other.y, self.z - other.z)

    def empty():
        return Vector3(0, 0, 0)

    def unit_z():
        return Vector3(0, 0, 1)


@dataclasses.dataclass
class Brick:
    min: Vector3
    max: Vector3

    def __sub__(self, other):
        assert isinstance(other, Vector3)

        self.min -= other
        self.max -= other

        return self

    def sub(self, other):
        assert isinstance(other, Vector3)

        return Brick(self.min - other, self.max - other)


def check_collision(c1, bricks):
    for c2 in bricks:
        if c2.max.z != c1.min.z:
            continue

        if (
            c2.min.x <= c1.max.x
            and c1.min.x <= c2.max.x
            and c2.min.y <= c1.max.y
            and c1.min.y <= c2.max.y
        ):
            return True

    return False


def apply_gravity(bricks):
    falls = 0

    for brick in bricks:
        z = brick.min.z
        tmp = brick.sub(Vector3.unit_z())

        while not check_collision(tmp, bricks) and tmp.min.z >= 1:
            brick -= Vector3.unit_z()
            tmp -= Vector3.unit_z()

        if brick.min.z != z:
            falls += 1

    return bricks, falls


def find_safe_disintegrates(bricks):
    res = len(bricks)

    for disintegrate in bricks:
        leftover = bricks.copy()
        leftover.remove(disintegrate)

        for brick in leftover:
            tmp = brick.sub(Vector3.unit_z())

            if tmp.min.z != disintegrate.max.z:
                continue

            if not check_collision(tmp, leftover) and tmp.min.z >= 1:
                res -= 1
                break

    return res


bricks = sorted(
    [
        Brick(
            Vector3(*map(int, min.split(","))),
            Vector3(*map(int, max.split(","))),
        )
        for min, max in bricks
    ],
    key=lambda brick: brick.max.z,
)

bricks, _ = apply_gravity(bricks)
bricks = sorted(bricks, key=lambda brick: brick.max.z)

# part 1

print(find_safe_disintegrates(bricks))

# part 2

def find_falls(bricks):
    res = 0

    for disintegrate in bricks:
        leftover = copy.deepcopy(bricks)
        leftover.remove(disintegrate)

        _, falls = apply_gravity(leftover)
        res += falls

    return res

print(find_falls(bricks))