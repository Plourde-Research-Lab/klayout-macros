# KLayout Macros
Collection of python and ruby macros to help with chip design in KLayout


## Features
* Coplanar Waveguide (CPW) Tools
    - **Path to CPW** rubymacros/make_cpw.rb
    - **CPW Resonator Frequency Calculation** pymacros/calc_freq.py
    - **Create Grounding Straps along CPW** pymacros/Make Ground Straps.py

* Fabrication Tools
    - **Write Job File for ASML Stepper** In progress.

## Installation

* Download the [KLayout Python Integration Preview.](http://www.klayout.de/python_preview.html)
* Make sure you have Python 3.4 installed on your system, with full numpy and scipy packages. Using Anaconda to create a py34 environment is pretty easy, and you can install the full Anaconda suite (with Numpy and Scipy) automatically. 
    - If you're running Anaconda with Python 2.7  
    ```
    conda create py34 anaconda
    ```

* Clone this repository
    ```
    git clone https://github.com/calebjordan/klayout-macros
    ```

* In KLayout Macros Development Window (F5), right click in the list of python folders, and click 'Add Location'. Add the 'pymacros' folder. 
* Do the same for the rubymacros in the ruby tab. 
* In 'pymacros/Python Startup.py', change the path names to correspond to your py34 environment. For instance, 

    ```
    sys.path.append("c:/Anaconda/envs/py34/lib")
    sys.path.append("c:/Anaconda/envs/py34/lib/site-packages")
    ```
* Restart KLayout. Most functions should appear in 'Tools' menu. 

