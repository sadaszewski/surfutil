#
# Author: Stanislaw Adaszewski, 2016
# License: 2-clause BSD
# Website: http://algoholic.eu
#


import nibabel.freesurfer.io as fio
from trimesh import Trimesh
from trimesh.io.export import export_mesh
from argparse import ArgumentParser
import numpy as np


def create_parser():
	parser = ArgumentParser()
	parser.add_argument('fname', type=str,
		help='Input file name')
	parser.add_argument('--outname', type=str,
		help='Output file name')
	return parser


def main():
	parser = create_parser()
	args = parser.parse_args()
	print 'fname:', args.fname
	g = fio.read_geometry(args.fname)
	m = Trimesh(g[0], g[1])
	if args.outname is None:
		# (name, ext) = os.path.splitext(args.fname)
		outname = '%s.stl' % args.fname
	else:
		outname = args.outname
	print 'outname:', outname
	export_mesh(m, outname)


if __name__ == '__main__':
	main()
