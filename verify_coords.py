from utils import world_to_pixel

# Test case from PRD: AmbroseValley, scale=900, origin=(-370, -473)
# World position: x=-301.45, z=-355.55
# Expected: pixel_x = 78, pixel_y = 890

x, z = -301.45, -355.55
px, py = world_to_pixel(x, z, "AmbroseValley")

print(f"World: ({x}, {z})")
print(f"Calculated Pixel: ({px:.2f}, {py:.2f})")
print(f"Expected Pixel: (78, 890)")

assert round(px) == 78, f"Expected 78, got {px}"
assert round(py) == 890, f"Expected 890, got {py}"

print("Coordinate mapping verification PASSED!")
