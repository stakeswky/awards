import ErdosProblem993.Transfer
open ErdosProblem993

-- exact elaborated statements of the headline theorems
#check @main_fin
#check @unimodal_of_isAcyclic
#check @isUnimodal_iff_finite
-- the definitions they rely on
#print IsUnimodal
#print icoeff
#print indepFinsets
#print SimpleGraph.IsIndepSet
#print SimpleGraph.IsAcyclic
-- independent axiom audit of the headline results
#print axioms main_fin
#print axioms unimodal_of_isAcyclic
#print axioms isUnimodal_iff_finite
