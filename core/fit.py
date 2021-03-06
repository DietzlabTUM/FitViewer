#!/usr/bin/env python
# -*- coding: utf-8 -*-

import MDAnalysis as mda
import attr

from operator import attrgetter
from typing import List, Tuple

from core.project import Project

__authors__ = ["Elija Feigl"]
""" VIEWERTOOL:
    Design Class manageing Mdanalyis structure for a given trajectory and
    configuration file of a namd simulation.

    COMMENTS:
    16.11.2020 not covering multi-scaffold structures
"""


@attr.s
class Fit(object):
    project: Project = attr.ib()

    def __attrs_post_init__(self):
        self.u: "mda.universe" = self._get_universe()
        self.scaffold, self.staples = self._split_strands()

    def _get_universe(self) -> "mda.universe":
        top = self.project.files.psf
        trj = self.project.files.coor

        if top.exists() and trj.exists():
            u = mda.Universe(str(top), str(trj))
        else:
            raise FileNotFoundError
        return u

    def _split_strands(self) -> Tuple["mda.segment", List["mda.segment"]]:
        # NOTE: no mulitscaffold
        strands = self.u.segments
        scaffold = max(strands, key=attrgetter("residues.n_residues"))
        staples = [s for s in strands if s.segid != scaffold.segid]
        return scaffold, staples
