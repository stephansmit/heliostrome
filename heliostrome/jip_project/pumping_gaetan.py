import pvpumpingsystem.waterproperties as wp
import pvpumpingsystem.pipenetwork as pn
import numpy as np
import fluids as fl
import os
import pvpumpingsystem.pvgeneration as pvgen
import pvpumpingsystem.pump as pp
import pvpumpingsystem.mppt as mppt
import pvpumpingsystem.pvpumpsystem as pvps
import heliostrome

# def water_source():
#     print("Select the water source available:")
#     print("1. Lake")
#     print("2. River")
#     print("3. Borehole/Well")
#     print("4. Large Dam/Large Open Well")

#     choice = input("Select an option: (1,2,3,4)")

#     if choice == "1":
#         print("You selected Option 1")
#         print("Most suitable pump is a surface pump")
#         # Add your code for Option 1 here
#     elif choice == "2":
#         print("You selected Option 2")
#         print("Most suitable pump is a surface pump")
#         # Add your code for Option 2 here
#     elif choice == "3":
#         print("You selected Option 3")
#         print("Most suitable pump is a submersible pump")
#         # Add your code for Option 3 here
#     elif choice == "4":
#         print("You selected Option 4")
#         print("Most suitable pump is a floating pump")
#         break
#     else:
#         print("Invalid choice. Please choose a valid option.")


def total_static_head(static_suction_head, static_delivery_head):
    """
    Head/Pressure required to bring fluid from a height to another certain height"""

    static_suction_head = static_suction_head  # Height from the water source to the pump (if the water source is higher than the pump, head is +ve)
    static_delivery_head = static_delivery_head  # Height from the pump to where the water needs to be delivered to (if the delivery location is higher than the pump, head is +ve)
    tsh = static_delivery_head - static_suction_head

    return tsh


def total_frictional_head(
    l: float, d: float, t: float, Q: float, r: float, material: str
):
    """
    Head/pressure required to overcome the friction of the pipes in which the fluid must flow through
    length  - Total length of pipes in the system ignoring bends
    diameter - Diameter of the pipes in mm
    temperature - Temperature of the water
    Q  - Flow rate of the water soruce in litres per minute
    r  - roughness of the material of the pipes
    material  - Material of the pipes"""

    d = d / 1000

    pipes = pn.PipeNetwork(h_stat=tsh, l_tot=l, diam=d, roughness=r, material=material)
    q = Q / 60000  # Convert litres per minute to m3 per second
    A = 0.25 * np.pi * d**2  # Area of the pie
    v = q / A  # Calculate the velocity of the water in the pipe
    viscosity_dyn = wp.water_prop("nuf", t + 273.15)  # [Pa.s¸]
    Re = v * pipes.diam / viscosity_dyn
    darcycoeff = fl.friction.friction_factor(Re, eD=pipes.roughness / pipes.diam)

    tfh = (darcycoeff * l * v**2) / (2 * d * 9.81)
    return tfh


def total_velociy_head(Q: float, d: float):
    """
    Head/pressure required to overcome the kinetic energy of a fluid in the pip
    """
    q = Q / 60000  # Convert litres per minute to m3 per second
    A = 0.25 * np.pi * d**2  # Area of the pie
    v = q / A  # Calculate the velocity of the water in the pipe
    tvh = (v**2) / (2 * 9.81)

    return tvh


def total_dynamic_head(tsh, tfh, tvh):
    tdh = tsh + tfh + tvh

    return tdh


def req_flow_rate(mm_max: float):
    hours_of_irrigation = 12
    mm_max_per_minute = mm_max / (
        hours_of_irrigation * 60
    )  # maximum mm of water delivered per minute
    flow_rate = mm_max_per_minute / 1000  # maximum l of water delivered per minute

    return flow_rate


def req_power(tsh, Q):
    power = tsh * Q * 16

    return power


# Bangladesh Case Example

# Calculating Required Total Dynamic Head & Flow Rate

# locations = [Gazipur - Brinjal, Jamalpur, Magura,Barisal]
static_suction_head = [0, 0, 0, 0]  # Given in Paper
static_delivery_head = [33.5, 24, 24, 8]  # Given in Paper
d = 38  # Given in Paper
t = 25.5  # Assumed for average water temperature in Bangladesh
r = 0.0015  # Value for roughness of PVC pipe (material in paper)
mm_max = 25  # Taken from simulation
Q = req_flow_rate(mm_max)
l = [93]  # Calculated from Brinjal in Gazipur layout
pump_eff = 0.6  # Assumption from averages

# Calculating the Required Total Dynamic Head with the goal to select the optimum pump
tsh = total_static_head(static_suction_head[0], static_delivery_head[0])
tfh = total_frictional_head(l[0], d, t, Q, r, "plastic")
tvh = total_velociy_head(Q, d)
print(f"Total Dynamic Head = {round(total_dynamic_head(tsh,tfh,tvh),2)}")
print(f"Power Required = {round(req_power(33.5,Q),2)}W")


##################################################

# Running the simulation with the given pump in case study


# main_folder = os.path.dirname(heliostrome.__file__)  # .replace("\\","/")

# #Need to adjust weather data for bangladesh

# pvpumping_input = os.path.join(main_folder, "data/weather/TUN_Tunis.607150_IWEC.epw")
# pvgen1 = pvgen.PVGeneration(
#     # Weather data path
#     weather_data_and_metadata=pvpumping_input,
#     pv_module_name="Canadian Solar CS5C 80M",  # Name of pv module to model
#     modules_per_string=4,
#     strings_in_parallel=1,
#     orientation_strategy="south_at_latitude_tilt",  # or 'flat' or None
# )

# mppt1 = mppt.MPPT(efficiency=0.96, idname="PCA-120-BLS-M2")

# #Pump Used - Lorentz PS 1200, 2.2 HP

# pump_file = os.path.join(main_folder, "data/pump/SCB_10_150_120_BL.txt")
# pump_sunpump = pp.Pump(path=pump_file)

# pipes1 = pn.PipeNetwork(
#     h_stat=tsh,  # static head [m]
#     l_tot=l[0],  # length of pipes [m]
#     diam=d/1000,  # diameter [m]
#     material="plastic",
# )

# pvps1 = pvps.PVPumpSystem(
#     pvgen1,
#     pump_sunpump,
#     coupling="direct",  # to adapt: 'mppt' or 'direct',
#     mppt=mppt1,
#     pipes=pipes1,
# )
# pvps1.run_model()

# pvps1.calc_efficiency()

# print(pvps1)
# print("\ntotal water pumped in the year = ", pvps1.flow.Qlpm.sum() * 60)
# print(
#     "\ndetails on second day of pumping = \n", pvps1.flow[24:200]
# )  # pvgen1.plot_model()
