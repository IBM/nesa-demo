# Neuro-Symbolic Agent Demo

This repository contains a demo for Neuro-Symbolic Agent (NeSA), which is specifically [Logical Optimal Action (LOA)](https://github.com/IBM/LOA).

## Setup

- Anaconda 4.10.3
- Tested on Mac and Linux

```bash
git clone --recursive git@github.com:IBM/nesa-demo.git
cd nesa-demo
conda create -n nesa-demo python=3.8
conda activate nesa-demo
conda install pytorch=1.10.0 torchvision torchaudio -c pytorch
conda install gensim==3.8.3 networkx unidecode nltk=3.6.3
pip install -U spacy
python -m spacy download en_core_web_sm
python -m nltk.downloader 'punkt'
pip install -r requirements.txt
cp -r third_party/commonsense_rl/games static/


# Download models
wget -O results.zip https://ibm.box.com/shared/static/chr1vvgb70mmt2gr1yijlsw3g7fq2pgs.zip
unzip results.zip
rm -f results.zip


# Download AMR cache file
mkdir -p cache
wget -O cache/amr_cache.pkl https://ibm.box.com/shared/static/klsvx54skc5wlf35qg3klo35ex25dbb0.pkl
```

## Execute

```bash
export AMR_SERVER_IP=localhost
export AMR_SERVER_PORT=
python app.py --release
 ```

### If you want to train the model by yourself

- commonsense-rl (DL-only method)

```bash
cd third_party/commonsense_rl/
python -u train_agent.py --agent_type knowledgeaware --game_dir ./games/twc --game_name *.ulx --difficulty_level easy --graph_type world --graph_mode evolve --graph_emb_type glove --world_evolve_type manual --initial_seed 0 --nruns 1
```

- Neuro-Symbolic Agent (LOA)

```bash
cd third_party/loa/
# follow the setup steps in README.md
python train.py
cp results/loa-twc-dleasy-np2-nt15-ps1-ks6-spboth.pkl ../../results/
```

## Citations

This repository provides code for the following paper, please cite the paper and give a star if you find the paper and code useful for your work.

- Daiki Kimura, Subhajit Chaudhury, Masaki Ono, Michiaki Tatsubori, Don Joven Agravante, Asim Munawar, Akifumi Wachi, Ryosuke Kohita, and Alexander Gray, "[LOA: Logical Optimal Actions for Text-based Interaction Games](https://aclanthology.org/2021.acl-demo.27/)", ACL-IJCNLP 2021.

  <details><summary>Details and bibtex</summary><div>

  The paper presents an initial demonstration of logical optimal action (LOA) on TextWorld (TW) Coin collector, TW Cooking, TW Commonsense, and Jericho. In this version, the human player can select an action by hand and recommendation action list from LOA with visualizing acquired knowledge for improvement of interpretability of trained rules.
  
  ```
  @inproceedings{kimura-etal-2021-loa,
      title = "{LOA}: Logical Optimal Actions for Text-based Interaction Games",
      author = "Kimura, Daiki  and  Chaudhury, Subhajit  and  Ono, Masaki  and  Tatsubori, Michiaki  and  Agravante, Don Joven  and  Munawar, Asim  and  Wachi, Akifumi  and  Kohita, Ryosuke  and  Gray, Alexander",
      booktitle = "Proceedings of the 59th Annual Meeting of the Association for Computational Linguistics and the 11th International Joint Conference on Natural Language Processing: System Demonstrations",
      month = aug,
      year = "2021",
      address = "Online",
      publisher = "Association for Computational Linguistics",
      url = "https://aclanthology.org/2021.acl-demo.27",
      doi = "10.18653/v1/2021.acl-demo.27",
      pages = "227--231"
  }
  ```
  </div></details>


## License

MIT License
