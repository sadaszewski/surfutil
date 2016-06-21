#
# Author: Stanislaw Adaszewski, 2016
# License: 2-clause BSD
# Website: http://algoholic.eu
#


import nibabel.freesurfer.io as fio
from pyevtk.vtk import VtkFile, VtkUnstructuredGrid, \
	VtkPolyData, VtkTriangle
from pyevtk.hl import _addDataToFile, \
	_appendDataToFile
from argparse import ArgumentParser
import numpy as np


def meshToVTK(path, v, f, pointData):
	assert v.shape[1] == f.shape[1] == 3
	# assert c.shape[0] == v.shape[0]
	
	offsets = np.arange(start = 3, stop = 3 * f.shape[0] + 1,
		step = 3, dtype=np.int32)
	
	cell_types = np.empty(f.shape[0], dtype=np.uint8)
	cell_types[:] = VtkTriangle.tid
	
	# connectivity = np.empty(3 * f.shape[0], dtype=np.int32)
	connectivity = np.ravel(f).astype(np.int32)
	
	(x, y, z) = (np.ravel(v[:, 0]),
		np.ravel(v[:, 1]),
		np.ravel(v[:, 2]))
	
	w = VtkFile(path, VtkUnstructuredGrid)
	w.openGrid()
	w.openPiece(ncells = f.shape[0], npoints = v.shape[0])
	
	w.openElement("Points")
	w.addData("points", (x, y, z))
	w.closeElement("Points")
	w.openElement("Cells")
	w.addData("connectivity", connectivity)
	w.addData("offsets", offsets)
	w.addData("types", cell_types)
	w.closeElement("Cells")
	
	_addDataToFile(w, cellData = None, pointData = pointData)
	
	w.closePiece()
	w.closeGrid()
	w.appendData((x, y, z))
	w.appendData(connectivity)
	w.appendData(offsets)
	w.appendData(cell_types)
	
	_appendDataToFile(w, cellData = None, pointData = pointData)
	
	w.save()
	return w.getFileName()


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
	if args.outname is None:
		outname = '%s_vtk' % args.fname
	else:
		outname = args.outname
	print 'outname:', outname
	rnd = (np.random.random((g[0].shape[0])) * 255).astype(np.uint8)
	pointData = {'Colors': (rnd, rnd, rnd)}
	meshToVTK(outname, g[0], g[1], pointData)
	


if __name__ == '__main__':
	main()
