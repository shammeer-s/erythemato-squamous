# Created by Samar on 19-05-2022
# Filename: base.py

import re

import pandas as pd


class declarations:
    def __init__(self):
        self.raw_column_string = """
                1. erythema 
                2. scaling 
                3. definite_borders 
                4. itching 
                5. koebner_phenomenon 
                6. polygonal_papules 
                7. follicular_papules 
                8. oral_mucosal_involvement 
                9. knee_and_elbow_involvement 
                10. scalp_involvement 
                11. family_history
                34. Age_(linear) 
                12. melanin_incontinence 
                13. eosinophils_in_the_infiltrate 
                14. PNL_infiltrate 
                15. fibrosis_of_the_papillary_dermis 
                16. exocytosis 
                17. acanthosis 
                18. hyperkeratosis 
                19. parakeratosis 
                20. clubbing_of_the_rete_ridges 
                21. elongation_of_the_rete_ridges 
                22. thinning_of_the_suprapapillary_epidermis 
                23. spongiform_pustule 
                24. munro_microabcess 
                25. focal_hypergranulosis 
                26. disappearance_of_the_granular_layer 
                27. vacuolisation_and_damage_of_basal_layer 
                28. spongiosis 
                29. saw_tooth_appearance_of_retes 
                30. follicular_horn_plug 
                31. perifollicular_parakeratosis 
                32. inflammatory_monoluclear_inflitrate 
                33. band_like_infiltrate 
                35. disease
                """
        self.temporary_di = {}
        self.cols = []
        self.data_col_setter()
        self.raw_data = pd.read_csv('../../input/dermatology.data', sep=",", names=self.cols)

    def data_col_setter(self):
        for i in self.raw_column_string.split("\n")[1:-1]:
            digi = ""
            for j in i:
                if j.isdigit():
                    digi = digi + j
            self.temporary_di[int(digi)] = str(" ".join(re.split("[^a-zA-Z_]*", i))).replace(" ", "")
        for i in sorted(self.temporary_di.keys()):
            self.cols.append(self.temporary_di[i])
