# KLayout Macros
Collection of python and ruby macros to help with chip design in KLayout


## Features
* Coplanar Waveguide (CPW) Tools
    - **Path to CPW** rubymacros/make_cpw.rb
    - **CPW Resonator Frequency Calculation** pymacros/calc_freq.py
    - **Create Grounding Straps along CPW** pymacros/Make Ground Straps.py
* FastHenry Integration
    - Generates .inp from selected shapes(paths only for now), calls FastHenry, and displays resulting Zc.mat in a dialog box.
    - FastHenry3.0 needs to be available in your path.
    - **In progress** 
        * Boxes as well as paths
        * Ground Planes
        * Editable Material parameters
        * Finer control over parameters

* Fabrication Tools
    - **Write Job File for ASML Stepper** In progress.

## Installation

* Download [KLayout](http://www.klayout.de/build.html)
* Make sure you have Python 3.4 installed on your system, with full numpy and scipy packages. Using Anaconda to create a py34 environment is pretty easy, and you can install the full Anaconda suite (with Numpy and Scipy) automatically. 
    - If you're running Anaconda with Python 2.7  
    ```
    conda create --name py34 python=3.4 anaconda
    ```
    This will create an environment containing a Python 3.4 installataion and will also install all anaconda packages.

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

