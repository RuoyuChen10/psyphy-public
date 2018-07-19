#############################################################################
# MIT License
#
# Copyright (c) 2018 Brandon RichardWebster
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
#############################################################################

import os, sys

import cPickle as pkl
import shutil
import uuid

import numpy as np
import psyphy.perturb as perturb
import psyphy.n2nmatch as n2n

import vggfacedec as vfd

if __name__ == '__main__':
    if len(sys.argv) < 4:
        raise Exception('missing ptype or range value')
    ptype = sys.argv[1]
    low = float(sys.argv[2])
    high = float(sys.argv[3])
    with open(os.path.join('vggface-pv.pkl'), 'rb') as f:
        sobj = pkl.load(f)

    def perturb(path, p):
        ipath = os.path.join('images-facegen', 'no-align', ptype, str(p), path.split('/')[-1])
        if p == 0 or p == 0.0:
            ipath = os.path.join('images-facegen', 'no-align', 'original', path.split('/')[-1])
        opath = '/tmp/' + str(uuid.uuid4()) + '.jpg'
        shutil.copyfile(ipath, opath)
        return opath

    output = n2n.item_response_curve_mafc(vfd.decision, perturb, sobj['imgs'], sobj['thresh'], 50, low, high)
    with open(os.path.join('vggface-irc-' + ptype + '.pkl'), 'w') as f:
        pkl.dump(output, f)
