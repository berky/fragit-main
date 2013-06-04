"""
**********************************************************************
fragmentation.py

Copyright (C) 2010-2011 Mikael W. Ibsen
Some portions Copyright (C) 2011-2013 Casper Steinmann

This file is part of the FragIt project.

FragIt is free software; you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation; either version 2 of the License, or
(at your option) any later version.

FragIt is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program; if not, write to the Free Software
Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA
02110-1301, USA.
***********************************************************************/
"""
import os
import sys
import logging

import openbabel

from util import *
from config import FragItConfig


class Fragmentation(FragItConfig):

    def __init__(self, mol):
        FragItConfig.__init__(self)
        self.mol     = mol
        self.obc     = openbabel.OBConversion()
        self.pat     = openbabel.OBSmartsPattern()
        self._residue_names = []
        self._fragment_names = []
        self._fragment_charges = []
        self._fragments = []
        self._backbone_atoms = []
        self._atoms = [mol.GetAtom(i) for i in range(1,mol.NumAtoms()+1)]
        self._mergeable_atoms = []

    def beginFragmentation(self):
        self.identifyBackboneAtoms()
        self.identifyMergeableAtoms()
        self.identifyResidues()
        self.determineFormalCharges()
        self.setProtectedAtoms()

    def identifyMergeableAtoms(self):
        patterns = self.getMergePatterns()
        for pattern in patterns:
            if len(patterns[pattern]) == 0: continue
            value = self._getAtomsToProtect(patterns[pattern])
            value.sort()
            self._mergeable_atoms.extend(value)

    def doFragmentMerging(self):
        """
        Merge a specific fragment into another specific fragment.
        """
        fragments_to_merge = self.getFragmentsToMerge()
        if len(fragments_to_merge) == 0: return
        fragments = self.getFragments()
        fragments_to_merge.reverse()
        for fragment_id in fragments_to_merge:
            previous_fragment = fragment_id-1
            ifrag = fragments.pop(fragment_id)
            jfrag = fragments[previous_fragment].extend(ifrag)

        self._fragments = fragments[:]
        self._CleanMergedBonds()

    def doFragmentSpecificMerging(self):
        """
        Merge a specific fragment into all other fragments and remove it as a singular fragment.
        """
        fragments_to_merge = self.getFragmentsToMerge()


    def doFragmentCombination(self):
        fragments_to_combine = self.getCombineFragments()
        if len(fragments_to_combine) == 0: return
        fragments_to_combine.reverse()
        fragments = self.getFragments()
        combined_fragment = ravel2D([fragments.pop(id-1) for id in fragments_to_combine])
        combined_fragment.sort()
        fragments.append(combined_fragment)

        self._fragments = fragments[:]
        self._CleanMergedBonds()

    def getFragmentsToMerge(self):
        """
        Return a list of [...] representing
        """
        fragments = self.getFragments()
        fragments_to_merge = []
        # each fragment is a list of integers (one for each atom in said fragment)
        for i,fragment in enumerate(fragments):
            for sid in self._mergeable_atoms:
                if sid in fragment and i not in fragments_to_merge:
                    fragments_to_merge.append(i)
        print fragments_to_merge
        return fragments_to_merge

    def doFragmentation(self):
        self.breakBonds()
        self.determineFragments()

    def finishFragmentation(self):
        self.determineFragmentCharges()
        self.nameFragments()

    def getFragments(self):
        return self._fragments

    def getFragmentNames(self):
        return self._fragment_names

    def getAtoms(self):
        return self._atoms

    def setActiveFragments(self, active_fragments):
        if not is_list(active_fragments): raise TypeError
        self.active_fragments = active_fragments

    def setProtectedAtoms(self):
        self.applySmartProtectPatterns()

    def clearProtectionPatterns(self):
        self.protected_atoms = list()

    def applySmartProtectPatterns(self):
        patterns = self.getProtectPatterns()
        for protectpattern in patterns.keys():
            pattern = patterns[protectpattern]
            if len(pattern) == 0: continue
            self.addExplicitlyProtectedAtoms(self._getAtomsToProtect(pattern))

    def _getAtomsToProtect(self,pattern):
        self.pat.Init(pattern)
        self.pat.Match(self.mol)
        return self._listMatches(self.pat.GetUMapList())

    def _listMatches(self,matches):
        results = []
        for match in matches:
            results.extend(match)
        return results

    def determineFormalCharges(self):
        model = self.getChargeModel()
        charge_model = openbabel.OBChargeModel.FindType(model)
        if charge_model is None: raise ValueError("The charge model '%s' is not valid." % model)
        self.formalCharges = tuple([0.0 for i in range(self.mol.NumAtoms())])
        if charge_model.ComputeCharges(self.mol):
            self.formalCharges = charge_model.GetPartialCharges()
        else:
            print "Charges are not available."

    def identifyResidues(self):
        if (len(self._residue_names) > 0):
            return self._residue_names
        patterns =     {
                "WATER" : "[H]O[H]",
                "NH3+"  : "N[H3]",
                "AMINO" : "C(=O)NC",
                "SUGAR" : "C1C(CO)OC(O)C(O)C1(O)"
                }
        result = []
        for residue in patterns.keys():
            pattern = patterns[residue]
            self.pat.Init(pattern)
            self.pat.Match( self.mol )
            for atoms in self.pat.GetUMapList():
                result.append({residue : atoms})

        self._residue_names = result
        return result

    def isBondProtected(self,bond_pair):
        protected_atoms = self.getExplicitlyProtectedAtoms()
        for bond_atom in bond_pair:
            if bond_atom in protected_atoms: return True
        return False

    def breakBonds(self):
        self._BreakPatternBonds()
        self.identifyCaps()
        self._DeleteOBMolBonds()

    def _DeleteOBMolBonds(self):
        for pair in self.getExplicitlyBreakAtomPairs():
            if not self.isValidExplicitBond(pair): continue
            if self.isBondProtected(pair): continue
            self._DeleteOBMolBond(pair)

    def _DeleteOBMolBond(self,pair):
        bond = self.mol.GetBond(pair[0],pair[1])
        self.mol.DeleteBond(bond)

    def _BreakPatternBonds(self):
        breakPatterns = self.getBreakPatterns()
        for bondType in breakPatterns.keys():
            pattern = breakPatterns[bondType]
            if len(pattern) == 0: continue
            self.pat.Init(pattern)
            self.pat.Match( self.mol )
            for p in self.pat.GetUMapList():
                self.realBondBreaker(bondType, p)

    def realBondBreaker(self, bondtype, bond_pair):
        if self.isBondProtected(bond_pair):
            return
        self.addExplicitlyBreakAtomPairs([bond_pair])

    def isValidExplicitBond(self, pair):
        if pair[0] == pair[1]: raise ValueError("fragment pair must be two different atoms.")
        if self.mol.GetBond(pair[0],pair[1]) == None: raise ValueError("fragment pair must be connected.")
        return True

    def determineFragments(self):
        self.getUniqueFragments()
        self.findRemainingFragments()
        self.doSanityCheckOnFragments()

    def getUniqueFragments(self):
        result = list()
        for pair in self.getExplicitlyBreakAtomPairs():
            result.append(self.getAtomsInSameFragment(pair[1], 0))
            result.append(self.getAtomsInSameFragment(pair[0], 0))
        result = uniqifyListOfLists(result)
        self._fragments = sorted(result)

    def doSanityCheckOnFragments(self):
        frag_sizes = lenOfLists(self._fragments)
        if (max(frag_sizes) > self.getMaximumFragmentSize()):
            raise ValueError("Fragment size too big. Found %i, Max is %i" % (max(frag_sizes),self.getMaximumFragmentSize()))

    def _CleanMergedBonds(self):
        broken_bonds = self.getExplicitlyBreakAtomPairs()
        fragments = self.getFragments()
        for bond in broken_bonds:
            for fragment in fragments:
                if bond[0] in fragment and bond[1] in fragment:
                    self.popExplicitlyBreakAtomPairs(bond)

    def doFragmentGrouping(self):
        if len(self._fragments) == 0: raise ValueError("You must fragment the molecule first.")
        groupSize = self.getFragmentGroupCount()
        newfragments = []
        lastFragment = None
        grpcount = 0
        tmp = []
        for fragment in self._fragments:
            grpcount += 1
            if len(tmp) + len(fragment) > self.getMaximumFragmentSize():
                #max size is reached
                isJoinable = False
            else:
                isJoinable     = self.isJoinable(fragment, lastFragment)
            if (grpcount < groupSize and isJoinable):
                #joined to previous fragment.
                tmp += fragment
                lastFragment =  fragment
                continue
            if (isJoinable):
                #The group is now big enough
                tmp += fragment
                newfragments.append(sorted(tmp))
                #reset
                lastFragment = None
                tmp = []
                grpcount = 0
            else:
                if (len(tmp) <> 0):
                    newfragments.append(sorted(tmp))
                lastFragment     = fragment
                grpcount     = 1
                tmp         = fragment
                #raise ValueError("Maximum fragment size too small, unable to continue")
        if (tmp != []):
            newfragments.append(sorted(tmp))

        self._fragments = newfragments

    def isJoinable(self,frag1,frag2):
        if (frag2 == None): return True
        for p in self.getExplicitlyBreakAtomPairs():
            if tupleValuesInEitherList(p,frag1,frag2):
                self.popExplicitlyBreakAtomPairs(p)
                return True
        return False

    def getFragmentCharges(self):
        return self._fragment_charges

    def determineFragmentCharges(self):
        self._fragment_charges = [self.getIntegerFragmentCharge(fragment) for fragment in self._fragments]
        self.total_charge = sum(self._fragment_charges)
        self.validateTotalCharge()

    def getIntegerFragmentCharge(self, fragment):
        charge = self.getSumOfAtomicChargesInFragment(fragment)
        return int(round(charge,0))

    def getSumOfAtomicChargesInFragment(self,fragment):
        charge = 0.0
        try:
            charge = sum([self.formalCharges[atom_idx-1] for atom_idx in fragment])
        except IndexError:
            print "Fragment %s has invalid charges." % (fragment)
        return charge

    def validateTotalCharge(self):
        total_charge2 = sum(self.formalCharges)
        total_charge2 = int(round(total_charge2,0))
        if (self.total_charge != total_charge2):
            raise ValueError("Due to rounding of floats, the sum of fragment charges = %i is wrong. Total charge = %i" %(total_charge2, self.total_charge))

    def getAtomsInSameFragment(self, a1, a2 = 0):
        if not is_int(a1) or not is_int(a2): raise ValueError
        if a2 != 0: raise ValueError
        tmp = openbabel.vectorInt()
        self.mol.FindChildren(tmp, a2, a1)
        fragment = sorted(toList(tmp) + [a1])
        return fragment

    def findRemainingFragments(self):
        remainingAtoms = listDiff(range(1, self.mol.NumAtoms() + 1), ravel2D(self._fragments))
        while len(remainingAtoms) > 0:
            newfrag = self.getAtomsInSameFragment(remainingAtoms[0])
            remainingAtoms = listDiff(remainingAtoms, newfrag)
            self._fragments.append(newfrag)

    def getOBAtom(self, atom_index):
        if not is_int(atom_index): raise ValueError
        if atom_index < 1 or atom_index > self.mol.NumAtoms(): raise ValueError("Index '%i' out of range [%i,%i]" % (atom_index,1,self.mol.NumAtoms()))
        return self.mol.GetAtom(atom_index)

    def nameFragments(self):
        names = list()
        for fragment in self.getFragments():
            name = self.tryNameFragment(fragment)
            if (name == False):    names.append(None)
            else:            names.append(name)
        self._fragment_names = names
        return names

    def tryNameFragment(self, atoms):
        matched_atoms     = 0
        frag_name     = False
        residues = self.identifyResidues()
        for residue in residues:
            res_name = residue.keys()[0]
            residue_atoms = residue[res_name]
            for atom in residue_atoms:
                if (not atom in atoms):
                    full_res_match = False
                    break
                full_res_match = True
            if (not full_res_match): continue
            common_atoms = len(residue_atoms)
            if (common_atoms > matched_atoms):
                matched_atoms     = common_atoms
                frag_name     = res_name

        return frag_name

    def identifyBackboneAtoms(self):
        pattern = "N([*])C([H])C(=O)"
        self.pat.Init(pattern)
        self.pat.Match(self.mol)
        self._backbone_atoms = Uniqify(self._listMatches(self.pat.GetUMapList()))

    def getBackboneAtoms(self):
        return self._backbone_atoms

    def identifyCaps(self):
        """Identifies caps to fragments.
           NB! we use fussy-matching which will require some
               thought
        """
        self._mfcc_order = 0
        if self.getOutputFormat() == 'XYZ-MFCC':
            self._mfcc_order = self.getMFCCOrder()
            print self._mfcc_order
            if self._mfcc_order <= 0:
                raise ValueError("You must specify the order of capping.")
            self.build_caps()

    def build_caps(self):
        self._caps = []
        for pair in self.getExplicitlyBreakAtomPairs():
            self._caps.append( self.build_cap(pair) )

    def build_cap(self, pair):
        cap_atm = [self.mol.GetAtom(id) for id in pair]
        cap_ids = [a.GetIdx() for a in cap_atm]
        cap_typ = [a.GetAtomicNum() for a in cap_atm]
        order = 0
        while order < self._mfcc_order:
          order += 1
          cap_atm, cap_ids, cap_typ = self.extend_cap(cap_atm, cap_ids, cap_typ, order == self._mfcc_order)
        return (cap_atm, cap_ids, cap_typ)

    def extend_cap(self, atms, ids, typs, is_final_cap):
        """Extends the current cap with neighboring atoms.
           if this is_final_cap then atoms are hydrogens. they will
           OPTIONALLY be translated later.
        """
        atms_out = atms[:]
        ids_out  = ids[:]
        typs_out = typs[:]
        for atom in atms:
            for atomext in openbabel.OBAtomAtomIter(atom):
                if atomext in atms: continue
                atms_out.append(atomext)
                ids_out.append(atomext.GetIdx())
                if is_final_cap:
                  typs_out.append(1)
                else:
                  typs_out.append(atomext.GetAtomicNum())
        return atms_out[:], ids_out[:], typs_out[:]
