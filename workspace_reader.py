import ROOT 

file = "htt_scalefactors_UL_2016postVFP.root"

func_dictionary = {


"ID_pt_bins_inc_eta" : ["m_id_ic_embed", "m_id_ic_mc"],  # just assign the value with eta=2.4
"ID_pt_eta_bins" : ["m_id_ic_embed","m_id_ic_mc",  ],

"Iso_pt_bins_inc_eta" : ["m_iso_ic_embed","m_iso_ic_mc",  ], # just assign the value with eta=2.4
"Iso_pt_eta_bins" : ["m_iso_ic_embed", "m_iso_ic_mc"],

"AIso1_pt_bins_inc_eta" : ["m_iso_ic_embed", "m_iso_ic_mc"],  #we don't need antiisolation so much 
"AIso1_pt_eta_bins" : ["m_iso_ic_embed", "m_iso_ic_mc"],  #we don't need antiisolation so much

"AIso2_pt_bins_inc_eta" : ["m_iso_ic_embed", "m_iso_ic_mc"],  #we don't need antiisolation so much 
"AIso2_pt_eta_bins" : ["m_iso_ic_embed", "m_iso_ic_mc"],  #we don't need antiisolation so much

"Trg_pt_eta_bins" : ["m_trg_ic_embed", "m_trg_ic_mc"],

"Trg_AIso1_pt_bins_inc_eta" : ["m_trg_ic_embed", "m_trg_ic_mc"], # we don't care about antiisolation
 
"Trg_AIso2_pt_bins_inc_eta" : ["m_trg_ic_embed", "m_trg_ic_mc"], # we don't care about antiisolation

# "m_sel_trg_kit_ratio" : "m_trg_ic_embed" # 1 / ( m_sel_trg_8_ic_1_data * m_sel_trg_17_ic_2_data + m_sel_trg_8_ic_2_data * m_sel_trg_17_ic_1_data - m_sel_trg_17_ic_1_data * m_sel_trg_17_ic_2_data



}


class WorkspaceReader:

    def __init__(self, file):

        ws_file = ROOT.TFile(file, "read")
        self.ws = ws_file.Get("w")



    def get_sfs(self, pt, eta, name, emb_mc_flag):
        try: 

            argset = self.ws.argSet("m_pt,m_eta")
            argset.setRealValue("m_pt", pt)
            argset.setRealValue("m_eta", eta)

            if emb_mc_flag == "emb":
                roofunction = self.ws.function(func_dictionary[name][0])
            elif emb_mc_flag == "mc":
                roofunction = self.ws.function(func_dictionary[name][1])

            result = roofunction.getVal(argset)

            return result

        except ReferenceError:
            print("\ the following function: {} have a scale factor in the following pT-eta {}-{}bin. 1. is returned".format(name, pt, eta))
            return 1.0