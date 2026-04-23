FONT_SIZE = "style=\"font-size:11px\";"

def get_contact_plugin_description_html():
    contact_plugin_descr = f""" 
  <p {FONT_SIZE}>
  <b>Contact Plugin:</b> computes the adhesion energy between neighboring cells.
  In essence, it describes how cells "stick" to each other. Contact energy is contrived.
  It is merely a way to replicate the properties of a cell's membrane,
  the bindings of the nano-structures on its surface, and its environment (the Medium).
  For more realistic interactions use AdhesionFlex plugin instead.
  </p>
   <p {FONT_SIZE}>
    Two cell types that have high contact energy will not "want to" adhere to each other.
    If possible, those cells may separate, effectively reducing the total energy to stay in
    that position. Conversely, low contact energy "encourages" cell types to bind. As contact
    energy is lowered, it also increases the surface of the contact.
    </p>
    <p {FONT_SIZE}>Contact energy is constantly re-calculated each time a cell's surface changes.
      Contact energy is defined as a matrix that compares each cell type against another cell type. The 
      neighbor order specifies the range of neighboring pixels to calculate the contact energy. Higher order is typically 
      more accurate but requires more computational effort.
    </p>
    <p {FONT_SIZE}><a href="https://compucell3dreferencemanual.readthedocs.io/en/latest/contact_plugin.html">Contact plugin information at CC3D website </a>
    </p>"""

    return contact_plugin_descr
