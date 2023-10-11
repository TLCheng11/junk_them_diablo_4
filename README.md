# Diablo 4 Inventory Junk Item Marker

## Disclaimer

**Note**: This is an unofficial application. This app utilizes macros to simulate certain mouse movements in the game, which may potentially lead to Blizzard overreacting, including but not limited to account bans. By using this app, you agree that you understand the risks involved and accept full responsibility for any actions taken by Blizzard.

## The Idea

The idea behind this application is to automate the process of marking junk items in your Diablo 4 inventory. It achieves this by simulating user mouse movements to toggle item tooltips, capturing screenshots of these tooltips, and processing the captured data using Tesseract OCR. The extracted data is then used to filter items based on user-defined criteria.

## How to Use

To use this application, follow these steps:

1. **Requirements:** Ensure that you have Python version 3.9 or higher installed on your system, as well as the Tesseract OCR Engine. You can download Tesseract following the instructions [here](https://github.com/tesseract-ocr/tesseract).

2. **Clone this Repository:** Clone this repository to your local machine.

3. **Configuration:** Open the `items_scanner.py` file and replace the default Tesseract path (on line 11) with the correct path to your Tesseract executable. The default path is set to 'C:\Program Files\Tesseract-OCR\tesseract.exe'.

4. **Execution:** Run the `run_app.bat` script to start the application. This will initiate the process of marking junk items in your Diablo 4 inventory.

Please be aware of the risks associated with using this application, as mentioned in the disclaimer section. Use it at your own discretion.

---
