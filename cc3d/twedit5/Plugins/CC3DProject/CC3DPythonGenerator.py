import os.path


def generate_configure_simulation_header():
    configureSimLines = '''
def configure_simulation():

    from cc3d.core.XMLUtils import ElementCC3D
    
'''

    return configureSimLines


def generate_configure_sim_fcn_body(root_element, output_file_name):
    # note the XML root element generated using C++ xml-to-python converter is called RootElementNameElmnt
    # here it will be CompuCell3DElmnt

    configure_sim_file_name = str(output_file_name)

    # _rootElement.saveXMLInPython(configure_sim_file_name)

    python_xml_file = open(configure_sim_file_name, 'w')

    python_xml_file.write('%s' % root_element.getXMLAsPython())

    python_xml_file.close()

    configure_sim_lines = generate_configure_simulation_header()

    configure_sim_file = open(configure_sim_file_name, "r")

    configure_sim_body = configure_sim_file.read()

    configure_sim_file.close()

    configure_sim_lines += configure_sim_body

    configure_sim_lines += '''

    CompuCellSetup.setSimulationXMLDescription(CompuCell3DElmnt)    

    '''

    configure_sim_lines += '\n'

    os.remove(configure_sim_file_name)

    return configure_sim_lines


class CC3DPythonGenerator:

    def __init__(self, xml_generator):

        self.xmlGenerator = xml_generator
        self.simulationDir = self.xmlGenerator.simulationDir
        self.simulationName = self.xmlGenerator.simulationName
        self.xmlFileName = self.xmlGenerator.fileName
        self.mainPythonFileName = os.path.join(str(self.simulationDir), str(self.simulationName) + ".py")
        self.steppablesPythonFileName = os.path.join(str(self.simulationDir),

                                                     str(self.simulationName) + "Steppables.py")

        self.configureSimLines = ''
        self.plotTypeTable = []
        self.pythonPlotsLines = ''
        self.pythonPlotsNames = []
        self.steppableCodeLines = ''
        self.steppableRegistrationLines = ''
        self.generatedSteppableNames = []
        self.generatedVisPlotSteppableNames = []
        self.cellTypeTable = [["Medium", False]]
        self.afMolecules = []
        self.afFormula = 'min(Molecule1,Molecule2)'
        self.cmcCadherins = []
        self.pythonOnlyFlag = False
        self.steppableFrequency = 1

    def set_python_only_flag(self, _flag):

        self.pythonOnlyFlag = _flag

    def generate_configure_sim_fcn(self):

        # note the XML root element generated using C++ xml-to-python converter is called RootElementNameElmnt
        # here it will be CompuCell3DElmnt

        configure_sim_file_name = str(self.xmlFileName + ".py")

        self.configureSimLines = generate_configure_sim_fcn_body(self.xmlGenerator.cc3d.CC3DXMLElement,
                                                                 configure_sim_file_name)

        self.configureSimLines += '\n'

    def generate_main_python_script(self):

        file = open(self.mainPythonFileName, "w")

        print("self.pythonPlotsLines=", self.pythonPlotsLines)

        header = ''

        if self.pythonOnlyFlag:
            self.generate_configure_sim_fcn()

        # note the XML root element generated using C++ xml-to-python converter is called RootElementNameElmnt
        # here it will be CompuCell3DElmnt

        if self.configureSimLines != '':
            header += self.configureSimLines

            header += '''
        
    CompuCellSetup.setSimulationXMLDescription(CompuCell3DElmnt)

            '''

        header += '''
from cc3d import CompuCellSetup
        '''

        if self.configureSimLines != '':
            header += '''

configure_simulation()            

            '''

        main_loop_line = '''
CompuCellSetup.run()
'''

        script = header
        script += self.steppableRegistrationLines
        script += main_loop_line
        file.write(script)

        file.close()

    # using only demo steppable
    def generate_steppable_registration_lines(self):

        steppable_module = self.simulationName + "Steppables"
        steppable_class = self.simulationName + "Steppable"
        steppable_frequency = self.steppableFrequency

        if not len(self.generatedSteppableNames) and not len(self.generatedVisPlotSteppableNames):

            self.steppableRegistrationLines += '''

from {steppable_module} import {steppable_class}

CompuCellSetup.register_steppable(steppable={steppable_class}(frequency={steppable_frequency}))

'''.format(steppable_module=steppable_module, steppable_class=steppable_class, steppable_frequency=steppable_frequency)

        else:
            # generating registration lines for user stppables
            for steppable_class in self.generatedSteppableNames:
                self.steppableRegistrationLines += '''


from {steppable_module} import {steppable_class}

CompuCellSetup.register_steppable(steppable={steppable_class}(frequency={steppable_frequency}))

'''.format(steppable_module=steppable_module, steppable_class=steppable_class, steppable_frequency=steppable_frequency)

    def generate_vis_plot_steppables(self):

        if not len(self.pythonPlotsNames):
            return

        self.steppableCodeLines += '''

            

from PlayerPython import *

from math import *            

'''

        for plotNameTuple in self.pythonPlotsNames:

            steppableName = plotNameTuple[0] + 'Steppable'

            if steppableName not in self.generatedVisPlotSteppableNames:
                self.generatedVisPlotSteppableNames.append(steppableName)

            plotType = plotNameTuple[1]

            if plotType == 'ScalarField':

                self.steppableCodeLines += '''



class %s(SteppableBasePy):

''' % (steppableName)

                self.steppableCodeLines += '''

    def __init__(self,_simulator,_frequency=%s):

        SteppableBasePy.__init__(self,_simulator,_frequency)

        self.visField=None

        

    def step(self,mcs):

        clearScalarField(self.dim,self.visField)

        for x in xrange(self.dim.x):

            for y in xrange(self.dim.y):

                for z in xrange(self.dim.z):

                    pt=CompuCell.Point3D(x,y,z)

                    if (not mcs % 20):

                        value=x*y

                        fillScalarValue(self.visField,x,y,z,value) # value assigned to individual pixel

                    else:

                        value=sin(x*y)

                        fillScalarValue(self.visField,x,y,z,value) # value assigned to individual pixel                    

''' % (self.steppableFrequency)



            elif plotType == 'CellLevelScalarField':

                self.steppableCodeLines += '''

                    

class %s(SteppableBasePy):

    def __init__(self,_simulator,_frequency=%s):

        SteppableBasePy.__init__(self,_simulator,_frequency)

        self.visField=None



    def step(self,mcs):

        clearScalarValueCellLevel(self.visField)

        from random import random

        for cell in self.cellList:

            fillScalarValueCellLevel(self.visField,cell,cell.id*random())   # value assigned to every cell , all cell pixels are painted based on this value             

''' % (steppableName, self.steppableFrequency)



            elif plotType == 'VectorField':

                self.steppableCodeLines += '''

                    

class %s(SteppableBasePy):

    def __init__(self,_simulator,_frequency=%s):

        SteppableBasePy.__init__(self,_simulator,_frequency)

        self.visField=None

    

    def step(self,mcs):

        maxLength=0

        clearVectorField(self.dim,self.visField)        

        for x in xrange(0,self.dim.x,5):

            for y in xrange(0,self.dim.y,5):

                for z in xrange(self.dim.z):                     

                    pt=CompuCell.Point3D(x,y,z)                    

                    insertVectorIntoVectorField(self.visField,pt.x, pt.y,pt.z, pt.x, pt.y, pt.z) # vector assigned to individual pixel

''' % (steppableName, self.steppableFrequency)



            elif plotType == 'CellLevelVectorField':

                self.steppableCodeLines += '''

                    

class %s(SteppableBasePy):

    def __init__(self,_simulator,_frequency=%s):

        SteppableBasePy.__init__(self,_simulator,_frequency)

        self.visField=None



    def step(self,mcs):

        clearVectorCellLevelField(self.visField)

        for cell in self.cellList:

            if cell.type==1:

                insertVectorIntoVectorCellLevelField(self.visField,cell, cell.id, cell.id, 0.0)

''' % (steppableName, self.steppableFrequency)

    def generate_interactive_plot_steppable(self, plot_specs):
        if not plot_specs:
            return

        steppable_name = "InteractivePlotSteppable"
        if steppable_name not in self.generatedSteppableNames:
            self.generatedSteppableNames.append(steppable_name)

        self.steppableCodeLines += '''

class {steppable_name}(SteppableBasePy):
    def __init__(self, frequency={steppable_frequency}):
        SteppableBasePy.__init__(self, frequency)
        self.plot_windows = {{}}

    def start(self):
'''.format(steppable_name=steppable_name, steppable_frequency=self.steppableFrequency)

        for plot_idx, plot_spec in enumerate(plot_specs):
            plot_key = "plot_{idx}".format(idx=plot_idx)
            plot_type = plot_spec.get("plot_type", "Line")
            self.steppableCodeLines += '''
        self.plot_windows[{plot_key!r}] = self.add_new_plot_window(
            title={title!r},
            x_axis_title={x_axis_title!r},
            y_axis_title={y_axis_title!r},
            x_scale_type={x_scale!r},
            y_scale_type={y_scale!r},
            grid=True,
            config_options={{'legend': {legend}}}
        )
'''.format(
                plot_key=plot_key,
                title=plot_spec.get("title", ""),
                x_axis_title=plot_spec.get("x_axis_title", ""),
                y_axis_title=plot_spec.get("y_axis_title", ""),
                x_scale=plot_spec.get("x_scale", "linear"),
                y_scale=plot_spec.get("y_scale", "linear"),
                legend=bool(plot_spec.get("legend", True))
            )

            for series_idx, series_spec in enumerate(plot_spec.get("series", [])):
                color = ["red", "green", "blue", "magenta", "cyan", "yellow"][series_idx % 6]
                if plot_type == "Histogram":
                    self.steppableCodeLines += '''
        self.plot_windows[{plot_key!r}].add_histogram_plot({series_name!r}, color={color!r}, alpha=100)
        plot_drawing_objects = getattr(self.plot_windows[{plot_key!r}], 'plotDrawingObjects', None)
        if isinstance(plot_drawing_objects, dict) and {series_name!r} in plot_drawing_objects:
            plot_drawing_objects[{series_name!r}]['curve'].setPen({color!r})
'''.format(plot_key=plot_key, series_name=series_spec.get("name", ""), color=color)
                else:
                    line_plot_kwargs = self._format_line_plot_kwargs(plot_spec=plot_spec, series_spec=series_spec)
                    plot_style = "Dots" if series_spec.get("style") == "Dots" else "Lines"
                    self.steppableCodeLines += '''
        self.plot_windows[{plot_key!r}].add_plot({series_name!r}, style={plot_style!r}, color={color!r}, size=3{line_plot_kwargs})
'''.format(
                        plot_key=plot_key,
                        series_name=series_spec.get("name", ""),
                        plot_style=plot_style,
                        color=color,
                        line_plot_kwargs=line_plot_kwargs
                    )

        custom_y_sources = self._custom_plot_y_sources(plot_specs)
        self.steppableCodeLines += '''

    def step(self, mcs):
'''
        if custom_y_sources:
            if len(custom_y_sources) == 1:
                self.steppableCodeLines += '''
        # The plot variable {y_source} must be defined before use.
'''.format(y_source=custom_y_sources[0])
            else:
                self.steppableCodeLines += '''
        # The plot variables {y_sources} must be defined before use.
'''.format(y_sources=", ".join(custom_y_sources))

        for plot_idx, plot_spec in enumerate(plot_specs):
            plot_key = "plot_{idx}".format(idx=plot_idx)
            plot_type = plot_spec.get("plot_type", "Line")
            for series_idx, series_spec in enumerate(plot_spec.get("series", [])):
                y_source = series_spec.get("y", "")
                x_source = series_spec.get("x", "mcs")
                x_expression = "max(mcs, 1)" if plot_spec.get("x_scale") == "log" else "mcs"
                series_var = "y_value_{plot_idx}_{series_idx}".format(plot_idx=plot_idx, series_idx=series_idx)
                source_type = series_spec.get("source_type", "custom")
                if plot_type == "Histogram":
                    values_var = "hist_values_{plot_idx}_{series_idx}".format(plot_idx=plot_idx, series_idx=series_idx)
                    if source_type == "cell_type":
                        type_attr = "t_{cell_type}".format(cell_type=y_source)
                        self.steppableCodeLines += '''
        {values_var} = [cell.volume for cell in self.cell_list_by_type(getattr(self, {type_attr!r}))]
'''.format(values_var=values_var, type_attr=type_attr)
                    else:
                        self.steppableCodeLines += '''
        {values_var} = {y_source}
'''.format(values_var=values_var, y_source=y_source)
                    self.steppableCodeLines += '''
        if {values_var}:
            self.plot_windows[{plot_key!r}].add_histogram(
                plot_name={series_name!r},
                value_array={values_var},
                number_of_bins=10
            )
'''.format(plot_key=plot_key, series_name=series_spec.get("name", ""), values_var=values_var)
                    continue

                if source_type == "cell_type":
                    type_attr = "t_{cell_type}".format(cell_type=y_source)
                    self.steppableCodeLines += '''
        {series_var} = len(self.cell_list_by_type(getattr(self, {type_attr!r})))
'''.format(series_var=series_var, type_attr=type_attr)
                else:
                    self.steppableCodeLines += '''
        {series_var} = {y_source}
'''.format(series_var=series_var, y_source=y_source)

                if plot_spec.get("y_scale") == "log":
                    self.steppableCodeLines += '''
        if {series_var} > 0:
            self.plot_windows[{plot_key!r}].add_data_point({series_name!r}, {x_expression}, {series_var})
'''.format(
                        plot_key=plot_key,
                        series_name=series_spec.get("name", ""),
                        x_expression=x_expression,
                        series_var=series_var
                    )
                else:
                    self.steppableCodeLines += '''
        self.plot_windows[{plot_key!r}].add_data_point({series_name!r}, {x_expression}, {series_var})
'''.format(
                        plot_key=plot_key,
                        series_name=series_spec.get("name", ""),
                        x_expression=x_expression,
                        series_var=series_var
                    )

    @staticmethod
    def _format_line_plot_kwargs(plot_spec, series_spec):
        kwargs = []
        separate_y_axis = bool(plot_spec.get("second_y_axis") and series_spec.get("axis") == "Right")
        if separate_y_axis:
            kwargs.append("separate_y_axis=True")

        y_min = series_spec.get("y_min", "")
        if y_min != "":
            try:
                kwargs.append("y_min={}".format(float(y_min)))
            except ValueError:
                pass

        y_max = series_spec.get("y_max", "")
        if y_max != "":
            try:
                kwargs.append("y_max={}".format(float(y_max)))
            except ValueError:
                pass

        if plot_spec.get("y_scale") == "log":
            kwargs.append("y_scale_type='log'")

        if not kwargs:
            return ""
        return ", " + ", ".join(kwargs)

    @staticmethod
    def _custom_plot_y_sources(plot_specs):
        custom_y_sources = []
        for plot_spec in plot_specs:
            for series_spec in plot_spec.get("series", []):
                if series_spec.get("source_type") != "custom":
                    continue
                y_source = series_spec.get("y", "")
                if y_source and y_source not in custom_y_sources:
                    custom_y_sources.append(y_source)
        return custom_y_sources

    def generate_constraint_initializer(self):

        if "ConstraintInitializerSteppable" not in self.generatedSteppableNames:
            self.generatedSteppableNames.append("ConstraintInitializerSteppable")

            self.steppableCodeLines += '''

class ConstraintInitializerSteppable(SteppableBasePy):
    def __init__(self,frequency={steppable_frequency}):
        SteppableBasePy.__init__(self,frequency)

    def start(self):

        for cell in self.cell_list:

            cell.targetVolume = 25
            cell.lambdaVolume = 2.0
        
        '''.format(steppable_frequency=self.steppableFrequency)

    def generate_growth_steppable(self):

        self.generate_constraint_initializer()

        if "GrowthSteppable" not in self.generatedSteppableNames:
            self.generatedSteppableNames.append("GrowthSteppable")

            self.steppableCodeLines += '''
class GrowthSteppable(SteppableBasePy):
    def __init__(self,frequency={steppable_frequency}):
        SteppableBasePy.__init__(self, frequency)

    def step(self, mcs):
    
        for cell in self.cell_list:
            cell.targetVolume += 1        

        # # alternatively if you want to make growth a function of chemical concentration uncomment lines below and comment lines above        

        # field = self.field.CHEMICAL_FIELD_NAME
        
        # for cell in self.cell_list:
            # concentrationAtCOM = field[int(cell.xCOM), int(cell.yCOM), int(cell.zCOM)]

            # # you can use here any fcn of concentrationAtCOM
            # cell.targetVolume += 0.01 * concentrationAtCOM       

        ''' .format(steppable_frequency=self.steppableFrequency)

    def generate_mitosis_steppable(self):

        self.generate_growth_steppable()

        if "MitosisSteppable" not in self.generatedSteppableNames:
            self.generatedSteppableNames.append("MitosisSteppable")

            self.steppableCodeLines += '''
class MitosisSteppable(MitosisSteppableBase):
    def __init__(self,frequency={steppable_frequency}):
        MitosisSteppableBase.__init__(self,frequency)

    def step(self, mcs):

        cells_to_divide=[]
        for cell in self.cell_list:
            if cell.volume>50:
                cells_to_divide.append(cell)

        for cell in cells_to_divide:

            self.divide_cell_random_orientation(cell)
            # Other valid options
            # self.divide_cell_orientation_vector_based(cell,1,1,0)
            # self.divide_cell_along_major_axis(cell)
            # self.divide_cell_along_minor_axis(cell)

    def update_attributes(self):
        # reducing parent target volume
        self.parent_cell.targetVolume /= 2.0                  

        self.clone_parent_2_child()            

        # for more control of what gets copied from parent to child use cloneAttributes function
        # self.clone_attributes(source_cell=self.parent_cell, target_cell=self.child_cell, no_clone_key_dict_list=[attrib1, attrib2]) 
        
        if self.parent_cell.type==1:
            self.child_cell.type=2
        else:
            self.child_cell.type=1

        '''.format(steppable_frequency=self.steppableFrequency)

    def generate_death_steppable(self):

        self.generate_constraint_initializer()

        if "DeathSteppable" not in self.generatedSteppableNames:
            self.generatedSteppableNames.append("DeathSteppable")

            self.steppableCodeLines += '''
class DeathSteppable(SteppableBasePy):
    def __init__(self, frequency={steppable_frequency}):
        SteppableBasePy.__init__(self, frequency)

    def step(self, mcs):
        if mcs == 1000:
            for cell in self.cell_list:
                if cell.type==1:
                    cell.targetVolume=0
                    cell.lambdaVolume=100

        '''.format(steppable_frequency=self.steppableFrequency)

    def generate_steppable_python_script(self):

        file = open(self.steppablesPythonFileName, "w")

        header = '''from cc3d.core.PySteppables import *
import numpy as np

'''
        file.write(header)
        # writing simple demo steppable
        steppable_class = self.simulationName + "Steppable"
        steppable_frequency = self.steppableFrequency
        if self.steppableCodeLines == '':

            class_definition_line = '''class {steppable_class}(SteppableBasePy):'''.format(
                    steppable_class=steppable_class)

            steppable_body = '''

    def __init__(self, frequency={steppable_frequency}):

        SteppableBasePy.__init__(self,frequency)

    def start(self):
        """
        Called before MCS=0 while building the initial simulation
        """

    def step(self, mcs):
        """
        Called every frequency MCS while executing the simulation
        
        :param mcs: current Monte Carlo step
        """

        for cell in self.cell_list:

            print("cell.id=",cell.id)

    def finish(self):
        """
        Called after the last MCS to wrap up the simulation
        """

    def on_stop(self):
        """
        Called if the simulation is stopped before the last MCS
        """
'''.format(steppable_frequency=steppable_frequency)

            file.write(class_definition_line)

            file.write(steppable_body)

        else:
            # writing steppables according to user requests
            file.write(self.steppableCodeLines)

        file.close()
