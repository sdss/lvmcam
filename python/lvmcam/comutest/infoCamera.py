import FLIR_Utils as FU  # All the camera interface stuff


verbose = True
cam, dev = FU.Setup_Camera(verbose, False)    # Instantiate camera and dev
FU.Standard_Settings(cam, dev, verbose)       # Standard settings (full frame, etc.)
FU.FLIR_Status(cam, dev)                     # Print out camera info
volts, current, power, temperature = FU.FLIR_Power(cam, dev, False)
print(f"volts: {volts}")
print(f"current: {current}")
print(f"power: {power}")
print(f"temparature: {temperature}")
