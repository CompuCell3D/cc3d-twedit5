
FONT_SIZE = "style=\"font-size:11px\";"

def get_internal_contact_plugin_description_html():
    int_contact_plugin_descr = f"""
     <p {FONT_SIZE}>
        <b>Internal Contact Plugin:</b> controls how easily sub-cells within the same compartment
      adhere to each other. The Internal Contact Plugin can help control the shape and
      arrangement of a compartmentalized cell. The standard Contact Plugin is included to
      control how clusters of cells interact with one another. The core idea here is to have different
      Internal Contact energies between subcells belonging to the same cluster and different Contact energies
      for cells belonging to different clusters. Technically subcells of a cluster are "regular"
      CompuCell3D cells (cell types). Each cell will have a 'Cluster Id' assigned to its cell attributes list.
      You will need to reassign each subcell with the same Cluster Id using CC3D python snippets: 'Cell Attributes'
      -> 'Cluster Id' and 'Cluster Id Reassignment' inserted into the simulation python steppables file. 
      </p>
      <p {FONT_SIZE}>
      The simple example below (figure and internal/contact energy matrices) shows two cell types (and 'Medium') in two cell clusters.
      For the internal contact matrix only the 'Cell_a' <-> 'Cell_b' interactions are allowed (You can change this as needed).
       Each of these cells are assigned a Cluster Id (either 'cluster_1 or 'cluster_2) to distinguish same individual 
       cell types from each other.
      </p>
    <p style="text-align: center">
       <img src=":/images/contact_internal_diagram.png">
       <table>
       <tr>
       <td>
       <table>
       <caption>Contact matrix:</caption> 
        <thead>
        <tr>
        <!-- Empty cell in corner -->
        <th></th>
        <th scope="col">Medium</th>
        <th scope="col">Cell_a</th>
        <th scope="col">Cell_b</th>
        </tr>
        </thead>
        <tbody>
        <tr>
        <th scope="row">Medium</th><td>10</td><td>10</td><td>10</td>
        </tr>
        <tr>
        <th scope="row">Cell_a</th><td>-</td><td>100</td><td>100</td>
        </tr>
        <tr>
        <th scope="row">Cell_b</th><td>-</td><td>-</td><td>100</td>
        </tr>
        </tbody>
        </table>
        </td>
       <td>
       <table>
       <tr>
       <td/>
       <td/>
       </tr>
       </table>
       </td>
        <td>
        <table>
       <caption>Internal contact matrix:</caption> 
        <thead>
        <tr>
        <!-- Empty cell in corner -->
        <th></th>
        <th scope="col">Medium</th>
        <th scope="col">Cell_a</th>
        <th scope="col">Cell_b</th>
        </tr>
        </thead>
        <tbody>
        <tr>
        <th scope="row">Medium</th><td>-</td><td>-</td><td>-</td>
        </tr>
        <tr>
        <th scope="row">Cell_a</th><td>-</td><td>-</td><td>5</td>
        </tr>
        <tr>
        <th scope="row">Cell_b</th><td>-</td><td>-</td><td>-</td>
        </tr>
        </tbody>
        </table>
        </td>
        </tr>
        </table>
    
     </p>
    <p {FONT_SIZE}>
     <a href="https://compucell3dreferencemanual.readthedocs.io/en/latest/compartments.html#compartmentalized-cells-contactinternal-plugin">Internal Contact plugin information at the CC3D Reference Manual website. </a>
      </p>
    """
    return int_contact_plugin_descr

