import ROOT 

file = "htt_scalefactors_UL_2016postVFP.root"

func_dictionary = {


# "ID_pt_bins_inc_eta" : ["m_id_ic_embed", "m_id_ic_mc"],  # just assign the value with eta=2.4
"ID_pt_eta_bins" : ["m_id_ic_embed","m_id_ic_mc",  ],

# "Iso_pt_bins_inc_eta" : ["m_iso_ic_embed","m_iso_ic_mc",  ], # just assign the value with eta=2.4
"Iso_pt_eta_bins" : ["m_iso_ic_embed", "m_iso_ic_mc"],

# "AIso1_pt_bins_inc_eta" : ["m_iso_ic_embed", "m_iso_ic_mc"],  #we don't need antiisolation so much 
# "AIso1_pt_eta_bins" : ["m_iso_ic_embed", "m_iso_ic_mc"],  #we don't need antiisolation so much

# "AIso2_pt_bins_inc_eta" : ["m_iso_ic_embed", "m_iso_ic_mc"],  #we don't need antiisolation so much 
# "AIso2_pt_eta_bins" : ["m_iso_ic_embed", "m_iso_ic_mc"],  #we don't need antiisolation so much

"Trg_pt_eta_bins" : ["m_trg_ic_embed", "m_trg_ic_mc"],

# "Trg_AIso1_pt_bins_inc_eta" : ["m_trg_ic_embed", "m_trg_ic_mc"], # we don't care about antiisolation
 
# "Trg_AIso2_pt_bins_inc_eta" : ["m_trg_ic_embed", "m_trg_ic_mc"], # we don't care about antiisolation



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

            if name in func_dictionary.keys():

                if emb_mc_flag == "emb":
                    roofunction = self.ws.function(func_dictionary[name][0])

                elif emb_mc_flag == "mc":
                    roofunction = self.ws.function(func_dictionary[name][1])

                result = roofunction.getVal(argset)

                # result = round(result, 5)  # round to 5 digits

                # print ("\n the following function: {} have a scale factor in the following bin: pt = {}, eta = {} is returned a corr factor = {}".format(name, pt, eta, result))

                return result
            elif name not in func_dictionary.keys():
                print("\n the following function: {} is not in the dictionary. 1. is returned".format(name))
                return 1.0

        except ReferenceError:
            print("\ the following function: {} have a scale factor in the following pT-eta {}-{}bin. 1. is returned".format(name, pt, eta))
            return 1.0
        
    def get_sfs_2D(self, pt, eta, name, emb_mc_flag):
        if name in func_dictionary.keys():

            if emb_mc_flag == "emb":

                hist = self.ws.obj("hist_"+func_dictionary[name][0])

            elif emb_mc_flag == "mc":
                hist = self.ws.obj("hist_"+func_dictionary[name][1])

            result = hist.GetBinContent( hist.GetXaxis().FindBin(pt) , hist.GetYaxis().FindBin(eta) )
        
            return result

            
        elif name not in func_dictionary.keys():
            return 1.0


        
            
    def get_emb_sel_sfs(self, pt_1, eta_1, pt_2, eta_binning):

        sfs = []

        for eta_2 in eta_binning:


            try: 


                argset_17_1 = self.ws.argSet("m_pt,m_eta")
                argset_17_2 = self.ws.argSet("m_pt,m_eta")

                argset_8_1 = self.ws.argSet("m_pt,m_eta")
                argset_8_2 = self.ws.argSet("m_pt,m_eta")


                argset_17_1.setRealValue("m_pt", pt_1)
                argset_17_1.setRealValue("m_eta", eta_1)


                argset_17_2.setRealValue("m_pt", pt_1)
                argset_17_2.setRealValue("m_eta", eta_1)


                argset_8_1.setRealValue("m_pt", pt_1)
                argset_8_1.setRealValue("m_eta", eta_1)


                argset_8_2.setRealValue("m_pt", pt_2)
                argset_8_2.setRealValue("m_eta", eta_2)


                roofunction_17_1 = self.ws.function("m_sel_trg_17_ic_1_data")
                roofunction_17_2 = self.ws.function("m_sel_trg_17_ic_2_data")

                roofunction_8_1 = self.ws.function("m_sel_trg_8_ic_1_data")
                roofunction_8_2 = self.ws.function("m_sel_trg_8_ic_2_data")

                efficiency_17_1 = roofunction_17_1.getVal(argset_17_1)
                efficiency_17_2 = roofunction_17_2.getVal(argset_17_2)

                efficiency_8_1 = roofunction_8_1.getVal(argset_8_1)

                efficiency_8_2 = roofunction_8_2.getVal(argset_8_2)

                print("\n efficiency 17_1 = {}, efficiency 17_2 = {}, efficiency 8_1 = {}, efficiency 8_2 = {}".format(efficiency_17_1, efficiency_17_2, efficiency_8_1, efficiency_8_2))


                result = 1 / ( efficiency_17_1 * efficiency_8_2 + efficiency_8_1 * efficiency_17_2 - efficiency_17_1 * efficiency_17_2)

                print(result)



                # return result
                sfs.append(result)


            except ReferenceError:
                # print("\ the following function: {} have a scale factor in the following pT-eta {}-{}bin. 1. is returned".format(name, pt, eta))
                # return 1.0
                sfs.append(1.0)
        return [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9 ]
        