
# html Adhesion flex calc info
def get_adhesion_flex_description_html():
    adhesion_desc = f"""
<h2>AdhesionFlex plugin calculations:</h2>
<p>
We use the following formula to calculate adhesion energy in AdhesionFlex plugin:
</p>
<p>

</p>
<p>
E_total = Sum<sub><em>i,j</em>,neighbors</sub> (-Sum<sub><em>m,n</em></sub>(k<sub><em>mn</em></sub>
( AdhesionFunc(N<sub><em>m</em></sub>(i), N<sub><em>n</em></sub>(j)) )))
 * (1 - dirac delta function(cell types at i and j))
</p>
<p>
  E_total: Total adhesion energy for a given cell.
  <br>
  i, j: pixel indexes
  </br>
   m, n: adhesion molecule label
</br>
<p>
  Sum<sub><em>i,j</em>,neighbors</sub>(): Sum of adhesion energies of all neighboring cells.
  </p>
  <p>
    Sum<sub><em>m,n</em></sub>(): Sum of adhesion energies from two adhesion molecules for all pixels in neighborhood.
  </p>
  N<sub><em>m,n</em></sub>: Adhesion molecule densities in cell type of pixel where it is located.
</br>
 </br>
 k<sub><em>mn</em></sub>: Binding parameter value between two adhesion molecules
  </p>
<p>
  When cells touch each other the resultant energy is simply a “product of interactions”
  of adhesion molecules from one cell with adhesion molecules from another cell.
  </p>
    <p>
    See <a href ="https://compucell3dreferencemanual.readthedocs.io/en/latest/adhesion_flex_plugin.html">CC3D website </a>
    for further information.
    </p>
    """

    return adhesion_desc
