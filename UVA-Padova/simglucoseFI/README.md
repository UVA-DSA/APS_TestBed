# simglucose-FI

This repositary contains a python version of UVA/PADOVA Type 1 Diabetes Simulator and a fault injection engine.

(1) Install virtual environment for simglucose
    virtualenv --python=/usr/bin/python3 ./venv

(2) Activate Virtual environment
    source ./venv/bin/activate

(3) Install dependent library for simglucose
    pip install -e .

(4) install rallab
    pip install git+https://github.com/Theano/Theano.git@adfe319ce6b781083d8dc3200fb4481b00853791#egg=Theano
    pip install joblib==0.10.3
    pip install pyprind
    pip install git+https://github.com/neocxi/Lasagne.git@484866cf8b38d878e92d521be445968531646bb8#egg=Lasagne
    pip install Pillow
    pip install cached_property

(5) Test your code 
    cd tests
    python3 run_Faultinjection_monitor.py 


This simulator was built on a previous work by integrating an adverse event simultor and upgrading controllers. Please refer to this [link](https://github.com/jxx123/simglucose) if you are interested to the originial simulator.

