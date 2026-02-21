def control_device(device, action):
    if device == "unknown":
        return "Device not recognized"

    return f"{device.capitalize()} has been turned {action}"