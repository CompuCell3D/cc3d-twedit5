Release Notes
=============

Version 4.7.0
-------------
**2025-06-21**

New features:

- Vastly improved Simulation Wizard
    - Removed Secretion plugin option (still supported in xml and CC3D, just not in Wizard).
    - Added Wizard page for DiffusionSolverFE, ReactionDiffusionSolverFE, and SteadystateSolver.
    - When specifying ReactionDiffusionSolverFVM or legacy diffusion solvers, default xml is inserted into the project xml file.
    - The new diffusion solver page adds secretion and uptake settings to be added for each chemical field.
    - The new diffusion solver page adds the ability to specify initial conditions and boundary conditions for each chemical field.
    - Added the ability to specify MCS and voxel conversion factors stored in the section (below). This is just a placeholder for a future feature.

Bug fixes:


Version 4.6.0
-------------
**2024-06-08**

New features:

Bug fixes:



Version 4.5.0
-------------
**2022-12-09**

New features:

Bug fixes:
 - Fixes to wizard code to prevent crashes


Version 4.4.1
-------------
**2022-07-01**

New features:
 - Added better conda builders that can utilize boa (mamba-based) builder
 - Added support for all Python versions >= 3.7

Bug fixes:
 - Fixed integration between Twedit and Player

Version 4.4.0
-------------
**2022-03-26**

New features:
 - Another round of improvements to the  DeveloperZone
 - Improved  code snippets

Bug fixes:
 - Fixing some code snippets


Version 4.3.1
-------------
**2022-07-17**

New features:
 - Improved DeveloperZone

Bug fixes:
 - Fixed integration of Twedit and Player
 - Better Python Templates in Twedit+


Version 4.3.0
-------------
**2022-02-26**

New features:
 - Split code into 3 separate packages - cc3d-core, Player, Twedit

