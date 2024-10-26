# html list of solvers
def get_diffusion_solv_description_html():
    diff_solver_desc = f"""
<h2>Diffusion solvers:</h2>
<h3>Diffusion Solver FE (default)</h3>
<p>
Main solver to use for solving diffusion equations. Uses Forward Euler method and handles moving boundary conditions. May be slow for large diffusion constants. In this case you may consider using a Steady State Diffusion solver.
<a href="https://compucell3dreferencemanual.readthedocs.io/en/latest/diffusion_solver.html"> More info.</a>
</p>

<h3>ReactionDiffusion</h3>
<p>
Solves coupled reaction-diffusion equations. Uses the Forward-Euler Method and allows flexibility in specifying reaction terms.
<a href="https://compucell3dreferencemanual.readthedocs.io/en/latest/reaction_diffusion_solver.html"> More info. </a> 
</p>

<h3>ReactionDiffusionFVM</h3>
<p>
Solves coupled reaction-diffusion equations. Uses the Finite Volume Method and allows flexibility in specifying reaction terms.
 <a href="https://compucell3dreferencemanual.readthedocs.io/en/latest/reaction_diffusion_solver_fvm.html">More info. </a>
</p>

<h3>SteadyStateDiffusionSolver</h3>
Solves Diffusion equation at the steady state i.e. at time= infinity. Often a good approximation for Diffusion Solver FE when dealing with large diffusion constants. However it is not a direct substitution for Diffusion Solver FE and you have to check the quality of the approximation before opting for this solver. Technically this solver solves Helmholtz Equation.
<a href="https://compucell3dreferencemanual.readthedocs.io/en/latest/steady_state_diffusion_solver.html"> More info.</a>

<h3><em>Legacy solvers:</em></h3>
<h3>FlexibleDiffusionSolverFE</h3>
Legacy solver was replaced by DiffusionSolver. Uses Finite-Euler method. We recommend you switch to Diffusion Solver FE. 
<a href="https://compucell3dreferencemanual.readthedocs.io/en/latest/flexible_diffusion_solver.html">More info</a>

<h3>FastDiffusionSolver2DFE</h3>
Legacy Solver that may have performance improvements over Diffusion Solver FE. 

<h3>KernalDiffusionSolver</h3>
Legacy Solver that provides an approximate solution to Diffusion Equations for large diffusion constants. While significantly faster than Diffusion Solver FE, it does not provide the same level of flexibility. 
<a href="https://compucell3dreferencemanual.readthedocs.io/en/latest/kernel_diffusion_solver.html"> More info.</a> """

    return diff_solver_desc