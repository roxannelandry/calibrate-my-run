# CalibrateMyRun

CalibrateMyRun is a Python application designed to calibrate TCX files when the total recorded distance and time is inaccurate. Whether you're using Garmin, Strava, or other fitness platforms, this tool ensures your activity data reflects the correct distance.  

---

## Features  
- 🛠️ **Calibrate TCX files**: Automatically adjust files to correct total distance and time discrepancies.  
- 🌍 **Supports Garmin & Strava formats**: Works seamlessly with popular fitness tracking platforms.  
- 📏 **Precision Adjustments**: Ensure your activity data is accurate for better analysis and comparisons.  

---

## Installation  

1. Clone this repository:  
   ```bash
   git clone https://github.com/roxannelandry/CalibrateMyRun.git
   cd CalibrateMyRun
   ```
2. Install the required dependencies:
```bash
pip install -r requirements.txt
```

## Usage

### Run the script:
```bash
python calibrate_threadmill_run.py <your_file.gpx> <distance-in-km> <time-in-min>
```

## How It Works

- Input Parsing: Reads TCX files to extract distance, waypoints, and other relevant metadata.
- Calibration: Adjusts distances by resampling, smoothing, or interpolating waypoints.
- Output Generation: Creates a new TCX file with the corrected total distance.

## Requirements
Python 3.8+

## Contributing
Contributions are welcome!

- Fork the repository.
- Create a feature branch: git checkout -b feature-name
- Commit your changes: git commit -m "Add some feature"
- Push to the branch: git push origin feature-name
- Open a pull request.

## License
This project is licensed under the MIT License.

## Support
If you encounter any issues or have suggestions, feel free to open an issue.

Happy tracking! 🚴‍♂️ 🏃‍♀️ 🏞️
