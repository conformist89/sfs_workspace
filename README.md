# sfs_workspace
One can extract scale factors from the ROOT workspace and write it to the correction lib format. The code is based on KIT  [Tag and Probe](https://github.com/KIT-CMS/TagAndProbe) repoditory

Before the execution, one should activate CROWN's tau environment, e.g

```
source /work/${USER}/CROWN/init.sh tau

```

Execution: 

```
python3 translate_to_crosspog_json.py -e 2016postVFPUL -c muon -o output

```
