# NonlinearPeric

Viscoplasticity

Similar to the classic rate independent J2 plasticity, the `NonlinearPeric` class defines a J2 plasticity incorporates
viscoplatisicity using Peric's model, that is

$$
\dot\gamma(\sigma,\sigma_y)=\left\{\begin{array}{ll}\dfrac{1}{\mu}\left[\dfrac{q(\sigma)}{\sigma_y}-1\right]
^{1/\epsilon},&\Phi\ge0,\\0,&\Phi<0.\end{array}\right.
$$

In which, $$\mu$$ is viscosity related parameter, $$\epsilon$$ is rate sensitivity, larger $$\epsilon$$ represents
response to be more sensitive to rate, $$q(\sigma)=\sqrt{\dfrac{3}{2}\eta:\eta}$$ as before is the effective von Mises
stress.
