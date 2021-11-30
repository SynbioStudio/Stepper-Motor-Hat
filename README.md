# Product Description:
The [Raspberry Pi Stepper Motor Hat](https://synbiostudio.com/products/raspberry-pi-stepper-motor-hat-up-to-two-stepper-motors) is designed for hassle-free actuation of stepper motors using python code. It uses SPI as the communication protocol enabling up to two stepper motors on each SPI bus.

# Connecting the Stepper Motor Hat:
To connect the device, simply align the female inputs on the hat with the male outputs from the Raspberry Pi board or other hats which have been previously stacked on top of the board. Connect the board to a voltage source and clip in the stepper motor into the connector.

# Enabling SPI Devices:
On the desktop screen, click on the Raspberry Pi icon in the top left corner. Click on preferences and select Raspberry Pi Configuration. At the top of the screen, click on Interfaces. Make sure SPI is enabled by selecting the appropriate radio button. Click OK.

# Installing the Relevant Libraries:
The stepper motor board uses our custom library (TMC5130.py). Make sure to include this library in your code and copy it to the same folder as your python script.

# Adjusting the Chip Select:
Each hat can handle up to two stepper motors per SPI bus. You can address each motor individually using the chip select parameter.

