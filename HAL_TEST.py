"""Quick test of the full HAL pipeline in simulated mode."""
import sys
sys.path.append('.')

from core.hal.dynamixel_bridge import DynamixelBridge
from core.hal.safety_governor import SafetyGovernor
from core.hal.servo_interpolator import ServoInterpolator

print()
bridge = DynamixelBridge()
print()
gov = SafetyGovernor(bridge)
print()
interp = ServoInterpolator()

print()
print("--- SIMULATION TEST ---")

# Set a target stance
target = [0.5]*7 + [-0.3]*7 + [0.1]*4 + [0.6]
interp.set_target(target)

# Get interpolated commands
left, right, stance, grip = interp.get_split_commands()

# Run through safety governor
sl, sr, ss, sg = gov.filter_command(left, right, stance, grip)

# Command servos
bridge.command_arms(sl, sr)
bridge.command_stance(ss)
bridge.command_grip(sg)

# Step simulation
for _ in range(10):
    bridge.step(0.02)

# Read proprioception
proprio = bridge.read_proprioception()
print(f"Proprioception ({len(proprio)} joints): {[round(p,3) for p in proprio]}")

# Reports
print()
report = bridge.get_status_report()
print(f"Total joints: {report['total_joints']}")
print(f"Simulated: {report['simulated']}")
print(f"E-Stopped: {report['e_stopped']}")

safety = gov.get_report()
st = safety['soft_touch']
print(f"Soft-Touch max force: {st['max_contact_force_N']}N")
print(f"Effective speed: {st['effective_speed_pct']}%")
print(f"Contact detected: {st['contact_detected']}")
print(f"Violations: {safety['violations']}")

# Show a few joints
print()
print("Joint states (first 5):")
shown = 0
for name, state in report['joints'].items():
    if shown >= 5:
        break
    print(f"  {name:20s}  cmd={state['commanded']:7.2f}  act={state['actual']:7.2f}  load={state['load']:.4f}")
    shown += 1

print()
print("[OK] Full HAL pipeline test PASSED")
