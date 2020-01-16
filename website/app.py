from flask import Flask, render_template, url_for
import re
app = Flask(__name__)

months = {'01':'Jan','02':'Feb','03':'Mar','04':'Apr','05':'May','06':'Jun','07':'Jul','08':'Aug','09':'Sep','10':'Oct','11':'Nov','12':'Dec'}

results = [
    {"id": "1901.00003", "title": ["\nLearning Spatial Common Sense with Geometry-Aware Recurrent Networks"], "authors": ["Hsiao-Yu Fish Tung", "Ricson Cheng", "Katerina Fragkiadaki"], "abstract": [" We integrate two powerful ideas, geometry and deep visual representation\nlearning, into recurrent network architectures for mobile visual scene\nunderstanding. The proposed networks learn to \"lift\" and integrate 2D visual\nfeatures over time into latent 3D feature maps of the scene. They are equipped\nwith differentiable geometric operations, such as projection, unprojection,\negomotion estimation and stabilization, in order to compute a\ngeometrically-consistent mapping between the world scene and their 3D latent\nfeature state. We train the proposed architectures to predict novel camera\nviews given short frame sequences as input. Their predictions strongly\ngeneralize to scenes with a novel number of objects, appearances and\nconfigurations; they greatly outperform previous works that do not consider\negomotion stabilization or a space-aware latent feature state. We train the\nproposed architectures to detect and segment objects in 3D using the latent 3D\nfeature map as input--as opposed to per frame features. The resulting object\ndetections persist over time: they continue to exist even when an object gets\noccluded or leaves the field of view. Our experiments suggest the proposed\nspace-aware latent feature memory and egomotion-stabilized convolutions are\nessential architectural choices for spatial common sense to emerge in\nartificial embodied visual agents.\n"], "primary_subject": ["Computer Vision and Pattern Recognition (cs.CV)"], "subjects": ["Computer Vision and Pattern Recognition (cs.CV)"]},
    {"id": "1901.00006", "title": ["\nHydrodynamics of Fermi arcs: Bulk flow and surface collective modes"], "authors": ["E. V. Gorbar", "V. A. Miransky", "I. A. Shovkovy", "P. O. Sukhachov"], "abstract": [" The hydrodynamic description of the Fermi arc surface states is proposed. In\nview of the strong suppression of scattering on impurities, the hydrodynamic\nregime for Fermi arc states should be, in principle, plausible. By using the\nkinetic theory, the Fermi arc hydrodynamics is derived and the corresponding\neffects on the bulk flow and surface collective modes are studied. For the bulk\nflow, the key effect of the proposed Fermi arc hydrodynamics is the\nmodification of the corresponding boundary conditions. In a slab geometry, it\nis shown that, depending on the transfer rates between the surface and bulk,\nthe hydrodynamic flow of the electron fluid inside the slab could be\nsignificantly altered and even enhanced near the surfaces. As to the spectrum\nof the surface collective modes, in agreement with earlier studies, it is found\nthat the Fermi arcs allow for an additional gapless spectrum branch and a\nstrong anisotropy of the surface plasmon dispersion relations in momentum\nspace. The gapped modes are characterized by closed elliptic contours of\nconstant frequency in momentum space.\n"], "primary_subject": ["Strongly Correlated Electrons (cond-mat.str-el)"], "subjects": ["Strongly Correlated Electrons (cond-mat.str-el)", "High Energy Physics - Phenomenology (hep-ph)", "Nuclear Theory (nucl-th)"]},
    {"id": "1901.00042", "title": ["\nOn a bounded remainder set for a digital Kronecker sequence"], "authors": ["Mordechay B. Levin"], "abstract": [" Let ${\\bf x}_0,{\\bf x}_1,...$ be a sequence of points in $[0,1)^s$.\n", "A subset $S$ of $[0,1)^s$ is called a bounded remainder set if there exist\ntwo real numbers $a$ and $C$ such that, for every integer $N$, $$\n", "| {\\rm card}\\{n <N \\; | \\; {\\bf x}_{n} \\in S \\} - a N| <C . $$ Let $ ({\\bf\nx}_n)_{n \\geq 0} $ be an $s-$dimensional digital Kronecker-sequence in base $b\n\\geq 2$, ${\\bf \\gamma} =(\\gamma_1,...,\\gamma_s)$, $\\gamma_i \\in [0, 1)$ with\n$b$-adic expansion\\\\ $\\gamma_i= \\gamma_{i,1}b^{-1}+ \\gamma_{i,2}b^{-2}+...$,\n$i=1,...,s$.\n", "In this paper, we prove that $[0,\\gamma_1) \\times ...\\times [0,\\gamma_s)$ is\nthe bounded remainder set with respect to the sequence $({\\bf x}_n)_{n \\geq 0}$\nif and only if \\begin{equation} \\nonumber\n", "\\max_{1 \\leq i \\leq s} \\max \\{ j \\geq 1 \\; | \\; \\gamma_{i,j} \\neq 0 \\} <\n\\infty. \\end{equation}\n"], "primary_subject": ["Number Theory (math.NT)"], "subjects": ["Number Theory (math.NT)"]}
]

@app.route('/')
@app.route('/search')
def search():
    return render_template('search.html')

@app.route('/result')
def result():
    return render_template('result.html', title='result', results=results, months=months)

@app.route('/about')
def about():
    return render_template('about.html')

if __name__ == '__main__':
    app.run(debug=True)
